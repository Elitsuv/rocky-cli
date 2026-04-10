"""
rky/commands.py
Advanced Toolset with custom arguments and system routers.
"""

import datetime
import webbrowser
import time
import sys
from rky.personality import format_response, format_question, unknown_command, load_user_profile, save_user_profile, C
from rky.brain import brain

def cmd_know_me():
    print(format_question("What is your designation, friend? (Enter name):"))
    name = input("> ").strip()
    print(format_question("What is your primary scientific focus? (e.g., Coding, Physics, Exams):"))
    focus = input("> ").strip()
    
    profile = {"name": name, "focus": focus}
    save_user_profile(profile)
    return format_response(f"Memory updated. You are {name}. We will conquer {focus} together. Amaze!")

def cmd_status():
    return format_response("Ship status: OPTIMAL.\nAstrophage containment: STABLE.\nAll systems: We are go for science.")

def cmd_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return format_response(f"Local human time: {now}.\nRocky uses stellar cycles. Conversion: approximate.")

# ── ADVANCED TODOS ──────────────────────────────
def cmd_todo(args: str):
    args = args.strip()
    
    if not args or args == "list":
        if not brain.todos:
            return format_response("Zero tasks pending. Highly illogical. Add some.")
        tasks = "\n".join(f"  [{i+1}] {t}" for i, t in enumerate(brain.todos))
        return format_response(f"Pending Missions:\n{tasks}\n\n  {C['DIM']}Use 'todo rm [number]' to complete.{C['RESET']}")
        
    if args.startswith("add "):
        task = args[4:].strip()
        brain.todos.append(task)
        brain.save_memory()
        brain.state[1] = min(10.0, brain.state[1] + 2.0)
        return format_response(f"Task logged to memory. Get to work on: {task}")
        
    if args.startswith("rm ") or args.startswith("remove "):
        try:
            idx = int(args.split()[1]) - 1
            if 0 <= idx < len(brain.todos):
                removed = brain.todos.pop(idx)
                brain.save_memory()
                return format_response(f"Task complete: '{removed}'. Good human efficiency! Fist my bump!")
            else:
                return format_response("Invalid task number. Check 'todo list'.")
        except:
            return format_response("Need a number to remove. (e.g., 'todo rm 1')")
            
    return format_response("Unknown todo command. Use 'todo list', 'todo add [task]', or 'todo rm [number]'.")

# ── ADVANCED WATER ──────────────────────────────
def cmd_water(args: str):
    args = args.strip()
    if args == "status":
        dryness = int(brain.state[2])
        return format_response(f"Current Dehydration Vector: {dryness}/10.\n(10 is critical failure. Drink before 10).")
    
    brain.state[2] = 0.0 
    return format_response("Hydration logged. Internal fluids restored to 100%. Good human.")

# ── CUSTOM POMODORO ──────────────────────────────
def cmd_pomodoro(args: str):
    try:
        # Check if user provided a custom time, else default to 25
        minutes = int(args.strip()) if args.strip().isdigit() else 25
        total_seconds = minutes * 60
        
        brain.state[1] = 10.0 
        brain.state[0] = 0.0 
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
        return format_response(f"Time is up! {minutes} minutes of science complete. Rest now. Amaze!")
        
    except KeyboardInterrupt:
        sys.stdout.write("\r\033[2K\033[?25h")
        brain.state[0] += 5.0 
        brain.state[1] -= 5.0
        return format_response("Focus aborted. Do not let Stratt find out. Distraction levels rising.")

# ── WEB & LORE ──────────────────────────────
def cmd_open_youtube(): webbrowser.open("https://youtube.com"); return format_response("YouTube launched.")
def cmd_open_google(): webbrowser.open("https://google.com"); return format_response("Google launched.")
def cmd_astrophage(): return format_response("Astrophage — microbe from Venus.\nDanger: EXTINCTION-CLASS.")
def cmd_taumoeba(): return format_response("Taumoeba — natural predator of Astrophage.\nStatus: SOLUTION.")
def cmd_help():
    help_text = """
    ── SYSTEM ────────────────────────────────────
      status          Ship overview
      know me         Reset your user profile
      time            Current Earth metrics

    ── NEURAL DRIVE (BRAIN) ──────────────────────
      todo add [x]    Add a mission objective
      todo rm [num]   Remove completed objective
      todo list       View pending missions
      water           Log hydration
      water status    Check dehydration vector
      focus [mins]    Start timer (e.g., 'focus 50')

    ── INTERACTION ───────────────────────────────
      youtube         Open YouTube
      clear           Clear screen
      exit            Shut down Rocky
    """
    return format_response(help_text, add_flair=False)

# ── DYNAMIC ROUTER ──────────────────────────────
def execute(user_input: str) -> str:
    brain.process_input(user_input)
    clean = user_input.strip().lower()
    
    # Route dynamic commands (they take arguments)
    if clean.startswith("todo"):
        return cmd_todo(clean[4:])
    if clean.startswith("focus") or clean.startswith("pomodoro"):
        return cmd_pomodoro(clean.replace("focus", "").replace("pomodoro", ""))
    if clean.startswith("water"):
        return cmd_water(clean[5:])
        
    # Route static commands
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