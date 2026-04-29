import datetime
import webbrowser
import time
import sys
from rky.personality import format_response, format_question, unknown_command, load_user_profile, save_user_profile, C
from rky.brain import brain
from rky.voice import voice_assistant

def cmd_know_me():
    print(format_question("What is your designation, friend? (Enter name):"))
    name = input("> ").strip()
    print(format_question("What is your primary scientific focus? (e.g., Coding, Physics, Exams):"))
    focus = input("> ").strip()
    
    profile = {"name": name, "focus": focus}
    save_user_profile(profile)
    return format_response(f"Memory updated. You are {name}. We will conquer {focus} together. Amaze!")

def cmd_status():
    bars = brain.status_summary()
    msg = f"Ship status: OPTIMAL.\nAstrophage containment: STABLE.\nAll systems: We are go for science.\n\n{bars}"
    return format_response(msg, add_flair=False)

def cmd_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return format_response(f"Local human time: {now}.\nRocky uses stellar cycles. Conversion: approximate.")

def cmd_todo(args: str):
    args = args.strip()
    
    if not args or args == "list":
        quests = brain.get_active_quests()
        if not quests:
            return format_response("Zero tasks pending. Highly illogical. Add some.")
        tasks = "\n".join(f"  [{q['id']}] {q['name']}" for q in quests)
        return format_response(f"Pending Missions:\n{tasks}\n\n  {C['DIM']}Use 'todo rm [id]' to complete.{C['RESET']}")
        
    if args.startswith("add "):
        name = args[4:].strip()
        qid = str(int(time.time()))[-4:] 
        brain.add_quest(qid, {"name": name, "complete": False})
        return format_response(f"Task logged to memory. Get to work on: [{qid}] {name}")
        
    if args.startswith("rm ") or args.startswith("remove ") or args.startswith("done "):
        try:
            qid = args.split()[1]
            if brain.complete_quest(qid):
                return format_response(f"Task [{qid}] complete. Good human efficiency! Fist my bump!")
            else:
                return format_response(f"Task ID [{qid}] not found. Check 'todo list'.")
        except IndexError:
            return format_response("Need an ID to remove. (e.g., 'todo rm 1234')")
            
    return format_response("Unknown todo command. Use 'todo list', 'todo add [task]', or 'todo rm [id]'.")

def cmd_water(args: str):
    args = args.strip()
    if args == "status":
        hydration = brain.get_state()["hydration"]
        pct = int(hydration * 100)
        return format_response(f"Current Hydration Vector: {pct}%.\n(Warning triggers below 35%. Drink water).")
    
    brain.log_drink()
    return format_response("Hydration logged. Internal fluids restored. Good human.")

def cmd_pomodoro(args: str):
    try:
        minutes = int(args.strip()) if args.strip().isdigit() else 25
        total_seconds = minutes * 60

        brain.start_focus_timer(minutes)
        print(format_response(f"Initiating Astrophage Drive Focus. {minutes} Earth minutes. No distractions."))
        
        sys.stdout.write("\033[?25l")
        
        for remaining in range(total_seconds, 0, -1):
            mins, secs = divmod(remaining, 60)
            
            progress = int((1 - (remaining / total_seconds)) * 40)
            bar = "█" * progress + "░" * (40 - progress)
            
            timer_text = f"\r  {C['QUEST']}FOCUS ENGAGED{C['RESET']} | {C['ROCKY']}{bar}{C['RESET']} | {mins:02d}:{secs:02d} "
            
            sys.stdout.write(timer_text)
            sys.stdout.flush()
            time.sleep(1)
            
        sys.stdout.write("\r\033[2K") 
        sys.stdout.write("\033[?25h") 
        
        brain.end_focus_timer()
        return format_response(f"Time is up! {minutes} minutes of science complete. Rest now. Amaze!")
        
    except KeyboardInterrupt:
        sys.stdout.write("\r\033[2K\033[?25h")
        # Tell the brain we aborted
        brain.end_focus_timer()
        return format_response("Focus aborted. Do not let Stratt find out. Distraction levels rising.")

def cmd_open_youtube(): 
    webbrowser.open("https://youtube.com")
    return format_response("YouTube launched. Warning: Distraction vector increasing.")

def cmd_open_google(): 
    webbrowser.open("https://google.com")
    return format_response("Google launched.")

def cmd_astrophage(): 
    return format_response("Astrophage — microbe from Venus.\nDanger: EXTINCTION-CLASS.")

def cmd_taumoeba(): 
    return format_response("Taumoeba — natural predator of Astrophage.\nStatus: SOLUTION.")

def cmd_voice(args: str):
    args = args.strip().lower()
    if args in ["on", "enable"]:
        voice_assistant.enabled = True
        return format_response("Voice mode enabled. I will speak to you now.")
    elif args in ["off", "disable"]:
        voice_assistant.enabled = False
        return format_response("Voice mode disabled. Silence is golden.")
    else:
        status = "ON" if voice_assistant.enabled else "OFF"
        return format_response(f"Voice mode is currently {status}. Use 'voice on' or 'voice off'.")

def cmd_help():
    help_text = """
    ── SYSTEM ────────────────────────────────────
      status          Ship overview & Neural Vectors
      know me         Reset your user profile
      time            Current Earth metrics

    ── NEURAL DRIVE (BRAIN) ──────────────────────
      todo add [x]    Add a mission objective
      todo rm [id]    Remove completed objective
      todo list       View pending missions
      water           Log hydration
      water status    Check dehydration vector
      focus [mins]    Start timer (e.g., 'focus 50')

    ── INTERACTION ───────────────────────────────
      youtube         Open YouTube
      clear           Clear screen
      voice [on/off]  Toggle voice output
      exit            Shut down Rocky
    """
    return format_response(help_text, add_flair=False)

def execute(user_input: str) -> str:
    brain.process_input(user_input)
    
    clean = user_input.strip().lower()

    if clean.startswith("todo"):
        return cmd_todo(clean[4:])
    if clean.startswith("focus") or clean.startswith("pomodoro"):
        return cmd_pomodoro(clean.replace("focus", "").replace("pomodoro", ""))
    if clean.startswith("water"):
        return cmd_water(clean[5:])
    if clean.startswith("voice"):
        return cmd_voice(clean[5:])
        
    COMMAND_MAP = {
        "status": cmd_status,
        "know me": cmd_know_me,
        "time": cmd_time,
        "youtube": cmd_open_youtube,
        "google": cmd_open_google,
        "astrophage": cmd_astrophage,
        "taumoeba": cmd_taumoeba,
        "help": cmd_help,
    }
    
    if clean in COMMAND_MAP: return COMMAND_MAP[clean]()
    for key in sorted(COMMAND_MAP, key=len, reverse=True):
        if key in clean: return COMMAND_MAP[key]()

    return unknown_command()