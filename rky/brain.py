import threading
import time
import json
from datetime import datetime
from pathlib import Path
import numpy as np

DIM = ["focus", "distraction", "hydration", "momentum", "fatigue"]
FOCUS = 0
DISTRACTION = 1
HYDRATION = 2
MOMENTUM = 3
FATIGUE = 4

_STATE_DIR = Path.home() / ".rocky"
_STATE_FILE = _STATE_DIR / "brain_state.json"

_A = np.array([
    [ 0.97, -0.05,  0.02,  0.03, -0.06],
    [ 0.02,  0.95, -0.01, -0.04,  0.05],
    [ 0.00,  0.00,  0.96,  0.00,  0.00],
    [ 0.04, -0.03,  0.01,  0.94, -0.03],
    [-0.01,  0.02, -0.01, -0.02,  0.97],
], dtype=np.float64)

_REST = np.array([0.50, 0.30, 0.60, 0.40, 0.30], dtype=np.float64)
_SIGMA = np.diag([0.005, 0.006, 0.002, 0.004, 0.003])

CONTROL_INPUTS: dict[str, np.ndarray] = {
    "focus_start":    np.array([ 0.12, -0.10,  0.00,  0.08, -0.02]),
    "focus_end":      np.array([-0.05,  0.04,  0.00, -0.03,  0.06]),
    "drink_water":    np.array([ 0.03, -0.02,  0.18,  0.02, -0.03]),
    "todo_add":       np.array([ 0.04, -0.01,  0.00,  0.06,  0.00]),
    "todo_done":      np.array([ 0.06, -0.05,  0.00,  0.10, -0.02]),
    "distraction":    np.array([-0.08,  0.14,  0.00, -0.05,  0.03]),
    "encourage":      np.array([ 0.05, -0.06,  0.00,  0.07, -0.04]),
    "break":          np.array([-0.04, -0.02,  0.02, -0.03, -0.08]),
    "quest_complete": np.array([ 0.08, -0.09,  0.00,  0.12, -0.05]),
    "idle":           np.zeros(5),
}

class RockyBrain:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._psi: np.ndarray = _REST.copy()
        self._tick: int = 0
        self._session_start = datetime.now()
        self._heartbeat_thread = None
        self._running = False
        self._last_drink = datetime.now()
        self._focus_start = None
        self._focus_minutes: int = 0
        self._events: list[dict] = []
        self._proactive_queue: list[str] = []
        self._quests: dict = {}
        self._load_state()

    def _load_state(self) -> None:
        try:
            _STATE_DIR.mkdir(parents=True, exist_ok=True)
            if not _STATE_FILE.exists(): return
            
            data = json.loads(_STATE_FILE.read_text(encoding="utf-8"))
            psi = np.array(data.get("psi", _REST.tolist()), dtype=np.float64)
            if psi.shape != (5,): return
            
            last_ts = data.get("timestamp")
            if last_ts:
                elapsed_minutes = (datetime.now() - datetime.fromisoformat(last_ts)).total_seconds() / 60
                for _ in range(min(int(elapsed_minutes), 120)):
                    psi = np.clip(_A @ psi + 0.002 * (_REST - psi), 0.0, 1.0)
                    
            self._psi = np.clip(psi, 0.0, 1.0)
            self._quests = data.get("quests", {})
            self._events = data.get("events", [])[-100:]
        except Exception:
            pass 

    def _save_state(self) -> None:
        try:
            _STATE_DIR.mkdir(parents=True, exist_ok=True)
            tmp = _STATE_FILE.with_suffix(".tmp")
            tmp.write_text(json.dumps({
                "psi": self._psi.tolist(),
                "timestamp": datetime.now().isoformat(),
                "quests": self._quests,
                "events": self._events[-100:],
            }, indent=2), encoding="utf-8")
            tmp.replace(_STATE_FILE)
        except Exception:
            pass

    def _tick_psi(self, control_key: str = "idle") -> None:
        u = CONTROL_INPUTS.get(control_key, CONTROL_INPUTS["idle"])
        noise = np.random.multivariate_normal(np.zeros(5), _SIGMA)
        homeostasis = 0.005 * (_REST - self._psi)
        self._psi = np.clip(_A @ self._psi + u + noise + homeostasis, 0.0, 1.0)

    def _heartbeat_loop(self) -> None:
        while self._running:
            time.sleep(60)
            if not self._running: break
            with self._lock:
                self._tick += 1
                self._tick_psi("idle")
                self._save_state()
                self._check_proactive_alerts()

    def _check_proactive_alerts(self) -> None:
        now = datetime.now()
        mins_since_drink = (now - self._last_drink).total_seconds() / 60

        if self._psi[HYDRATION] < 0.35 and mins_since_drink > 45:
            self._proactive_queue.append("\n\033[38;5;130m🪨 Rocky:\033[0m Hydration critical. Drink water. Science needs a functional brain.\n")
            self._last_drink = now

        if self._psi[FATIGUE] > 0.72:
            self._proactive_queue.append("\n\033[38;5;130m🪨 Rocky:\033[0m Fatigue signal high. Short break is logical. You return sharper. I wait.\n")

        if self._psi[DISTRACTION] > 0.68:
            self._proactive_queue.append("\n\033[38;5;130m🪨 Rocky:\033[0m Distraction elevated. Try 'focus 25' to recalibrate. We have mission.\n")

        session_mins = int((now - self._session_start).total_seconds() / 60)
        if session_mins > 0 and session_mins % 90 == 0:
            self._proactive_queue.append(f"\n\033[38;5;130m🪨 Rocky:\033[0m {session_mins} minutes active. You are doing science. Very good.\n")

    def start_heartbeat(self) -> None:
        if self._running: return
        self._running = True
        t = threading.Thread(target=self._heartbeat_loop, daemon=True, name="rocky-heartbeat")
        t.start()
        self._heartbeat_thread = t

    def stop_heartbeat(self) -> None:
        self._running = False

    def apply_control(self, key: str) -> None:
        with self._lock:
            self._tick_psi(key)
            self._events.append({
                "t": datetime.now().isoformat(),
                "event": key,
                "psi": self._psi.tolist(),
            })
            if len(self._events) > 150:
                self._events = self._events[-150:]
            self._save_state()

    def process_input(self, text: str) -> None:
        text = text.lower()
        if any(word in text for word in ["youtube", "movie", "bored", "social"]):
            self.apply_control("distraction")
        elif any(word in text for word in ["code", "matrixmind", "jee", "physics", "math", "chemistry"]):
            self.apply_control("encourage")
        elif "tired" in text or "sleep" in text:
            self.apply_control("break")
        else:
            self.apply_control("idle")

    def get_state(self) -> dict:
        with self._lock:
            return {dim: float(round(self._psi[i], 3)) for i, dim in enumerate(DIM)}

    def get_proactive_message(self) -> str | None:
        with self._lock:
            return self._proactive_queue.pop(0) if self._proactive_queue else None

    def focus_score(self) -> float:
        with self._lock:
            w = np.array([0.40, -0.25, 0.15, 0.25, -0.20])
            raw = float(np.dot(w, self._psi))
            return round(max(0.0, min(1.0, raw + 0.30)), 3)

    def status_summary(self) -> str:
        with self._lock:
            C_R, C_G, C_D, C_RST = "\033[38;5;130m", "\033[38;5;48m", "\033[2m", "\033[0m"
            bars = [
                ("Focus     ", self._psi[FOCUS]),
                ("Clarity   ", 1.0 - self._psi[DISTRACTION]),
                ("Hydration ", self._psi[HYDRATION]),
                ("Momentum  ", self._psi[MOMENTUM]),
                ("Stamina   ", 1.0 - self._psi[FATIGUE]),
            ]
            lines = [f"  {C_D}── Neural State Vector Ψ ──────────────────{C_RST}"]
            for label, val in bars:
                filled = int(val * 22)
                bar = f"{C_G}" + "█" * filled + f"{C_D}" + "░" * (22 - filled) + f"{C_RST}"
                lines.append(f"  {C_R}{label}{C_RST} [{bar}] {int(val * 100):>3}%")

            score = self.focus_score()
            session_mins = int((datetime.now() - self._session_start).total_seconds() / 60)
            lines.append(f"\n  Focus Score : {C_R}{score:.2f}{C_RST}  |  Session : {C_R}{session_mins}m{C_RST}  |  Tick #{C_D}{self._tick}{C_RST}")
            return "\n".join(lines)

    def start_focus_timer(self, minutes: int) -> None:
        with self._lock:
            self._focus_start = datetime.now()
            self._focus_minutes = minutes
            self.apply_control("focus_start")

    def end_focus_timer(self) -> int:
        with self._lock:
            if self._focus_start is None: return 0
            elapsed = int((datetime.now() - self._focus_start).total_seconds() / 60)
            self._focus_start = None
            self.apply_control("focus_end")
            return elapsed

    def is_in_focus(self) -> bool:
        with self._lock:
            return self._focus_start is not None

    def get_focus_remaining(self) -> int:
        with self._lock:
            if self._focus_start is None: return 0
            elapsed = (datetime.now() - self._focus_start).total_seconds() / 60
            return max(0, int(self._focus_minutes - elapsed))

    def log_drink(self) -> None:
        with self._lock:
            self._last_drink = datetime.now()
            self.apply_control("drink_water")

    def get_context_question(self) -> str | None:
        with self._lock:
            if len(self._events) < 5: return None
            recent = [e["event"] for e in self._events[-15:]]
            dist_n = recent.count("distraction")
            done_n = recent.count("todo_done")
            enc_n = recent.count("encourage")
            focus_n = recent.count("focus_start")

            if dist_n >= 3: return "Rocky observe: distraction event logged 3+ times. Is environment the problem? Try 'focus 25'."
            if done_n >= 5: return "Rocky compute: high task completion rate. Are you near a milestone? Log it: 'todo add milestone'."
            if enc_n >= 2 and focus_n < 1: return "Rocky detect: encouragement requested, but no focus active. Ryland Grace also felt this way. He started anyway."
        return None

    def get_active_quests(self) -> list:
        with self._lock:
            return [{**q, "id": qid} for qid, q in self._quests.items() if not q.get("complete", False)]

    def get_all_quests(self) -> list:
        with self._lock:
            return [{**q, "id": qid} for qid, q in self._quests.items()]

    def add_quest(self, quest_id: str, quest: dict) -> None:
        with self._lock:
            self._quests[quest_id] = quest
            self._save_state()

    def complete_quest(self, quest_id: str) -> bool:
        with self._lock:
            if quest_id in self._quests and not self._quests[quest_id].get("complete"):
                self._quests[quest_id]["complete"] = True
                self._quests[quest_id]["completed_at"] = datetime.now().isoformat()
                self._save_state()
                self.apply_control("quest_complete")
                return True
        return False

brain = RockyBrain()