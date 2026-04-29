import threading
import time
import json
from rky.personality import format_response, C

MEMORY = "memory.json"
_STATE_DIR = os.path.join(os.path.expanduser("~"), ".rocky")
os.makedirs(_STATE_DIR, exist_ok=True)
_STATE_FILE = os.path.join(_STATE_DIR, MEMORY)

HYDRATION = "hydration"
FOCUS = "focus"
DISTRACTION = "distraction"
MOMENTUM = "momentum"

class RockyBrain:
    def __init__(self):
        self.active = True
        self._tick = 0
        self._psi = {HYDRATION: 0.6, FOCUS: 0.5, DISTRACTION: 0.0, MOMENTUM: 0.0}
        self.quests = self._load_memory()
        self.focus_timer_active = False

    def _load_memory(self):
        if os.path.exists(_STATE_FILE):
            try:
                with open(_STATE_FILE, "r") as f:
                    return json.load(f).get("todos", [])
            except:
                return []
        return []

    def save_memory(self):
        try:
            with open(_STATE_FILE, "w") as f:
                json.dump({"todos": self.quests}, f, indent=4)
            return True
        except:
            return False

    def get_state(self):
        return {
            "hydration": self._psi[HYDRATION],
            "focus": self._psi[FOCUS],
            "distraction": self._psi[DISTRACTION],
            "momentum": self._psi[MOMENTUM]
        }

    def process_input(self, text: str):
        words = text.lower().split()
        if "youtube" in words:
            self._psi[FOCUS] = max(0.0, self._psi[FOCUS] - 0.2)
            self._psi[DISTRACTION] = min(1.0, self._psi[DISTRACTION] + 0.3)

    def log_drink(self):
        self._psi[HYDRATION] = min(1.0, self._psi[HYDRATION] + 0.5)

    def get_all_quests(self):
        return self.quests

    def get_active_quests(self):
        return [q for q in self.quests if not q.get("complete", False)]

    def add_quest(self, qid: str, data: dict):
        quest = {"id": qid, **data}
        self.quests.append(quest)
        self.save_memory()

    def complete_quest(self, qid: str) -> bool:
        for q in self.quests:
            if q["id"] == qid and not q.get("complete", False):
                q["complete"] = True
                self._psi[MOMENTUM] = min(1.0, self._psi[MOMENTUM] + 0.2)
                self.save_memory()
                return True
        return False

    def start_focus_timer(self, minutes: int):
        self.focus_timer_active = True

    def end_focus_timer(self):
        self.focus_timer_active = False

    def status_summary(self) -> str:
        h_bar = int(self._psi[HYDRATION] * 10)
        f_bar = int(self._psi[FOCUS] * 10)
        return (f"  Hydration:   [{'█' * h_bar}{'░' * (10 - h_bar)}]\n"
                f"  Focus:       [{'█' * f_bar}{'░' * (10 - f_bar)}]")

    def start_heartbeat(self):
        t = threading.Thread(target=self._pulse, daemon=True)
        t.start()
        self._heartbeat_thread = t

    def _pulse(self):
        while self.active:
            time.sleep(90)
            self._tick += 1
            self._psi[HYDRATION] -= 0.05
            
            if self._psi[HYDRATION] <= 0.3:
                message = "Hydration levels critical! Drink H2O immediately."
                self._interrupt_console(message)
            elif self.get_active_quests() and random.random() > 0.7:
                task = random.choice(self.get_active_quests())
                message = f"Task pending: '{task['name']}'. Why is this not complete? Human efficiency is low."
                self._interrupt_console(message)

    def _interrupt_console(self, message):
        formatted = format_response(message, add_flair=False)
        sys.stdout.write(f"\033[2K\r\n{formatted}{C['ROCKY']}rocky>{C['RESET']} ")
        sys.stdout.flush()

brain = RockyBrain()