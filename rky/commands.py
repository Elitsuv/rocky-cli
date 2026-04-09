import datetime
import random
import webbrowser
import time
import sys
from rky.personality import format_response, format_question, unknown_command, load_user_profile, save_user_profile

def cmd_know_me():
    print(format_question("What is your designation, friend? (Enter name):"))
    name = input("> ").strip()
    print(format_question("What is your primary scientific focus? (e.g., Coding, Physics, Exams):"))
    focus = input("> ").strip()
    
    profile = {"name": name, "focus": focus}
    save_user_profile(profile)
    return format_response(f"Memory updated. You are {name}. We will conquer {focus} together. Amaze!")

def cmd_status():
    return format_response(
        "Ship status: OPTIMAL.\n"
        "Astrophage containment: STABLE.\n"
        "All systems: We are go for science."
    )

def cmd_pomodoro():
    try:
        minutes = 25
        seconds = minutes * 60
        print(format_response(f"Focus mode active. {minutes} Earth minutes of uninterrupted science. Go!"))
        
        for remaining in range(seconds, 0, -1):
            sys.stdout.write(f"\r\033[38;5;208m⏳ Time remaining: {remaining // 60:02d}:{remaining % 60:02d}\033[0m ")
            sys.stdout.flush()
            time.sleep(1)
            
        sys.stdout.write("\r" + " " * 40 + "\r") # Clear line
        return format_response("Time is up! Good focus. Brain needs rest now. Fist my bump!")
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        return format_response("Focus interrupted. We stop science for now.")


def cmd_open_youtube():
    webbrowser.open("https://youtube.com")
    return format_response("YouTube launched. Rocky recommends science documentaries.")

def cmd_open_google():
    webbrowser.open("https://google.com")
    return format_response("Google launched. Gather data. Form hypothesis.")

def cmd_open_email():
    webbrowser.open("mailto:")
    return format_response("Communication interface opened. Send signals to Earth.")

def cmd_astrophage():
    return format_response(
        "Astrophage — microbe from Venus.\n"
        "Feeds on solar energy. Danger level: EXTINCTION-CLASS.\n"
        "Weakness: Tau Ceti e has the answer."
    )

def cmd_taumoeba():
    return format_response(
        "Taumoeba — microorganism found on planet Adrian.\n"
        "Function: natural predator of Astrophage.\n"
        "Status: SOLUTION TO HUMANITY'S EXTINCTION. Yes yes yes!"
    )

def cmd_grace():
    return format_response(
        "Dr. Ryland Grace — human.\n"
        "Saved my life. I saved his. Best friend. Confirmed."
    )

def cmd_help():
    help_text = """
    ── SYSTEM ────────────────────────────────────
      status          Ship overview
      know me         Set your user profile
      time / date     Current Earth metrics

    ── PRODUCTIVITY ──────────────────────────────
      focus mode      Start 25-minute Pomodoro timer
      youtube         Open YouTube
      google          Open Google Search
      email           Open Mail client

    ── LORE ──────────────────────────────────────
      astrophage      What is it?
      taumoeba        The solution
      grace           About Ryland Grace

    ── INTERACTION ───────────────────────────────
      clear           Clear screen
      exit            Shut down Rocky
    """
    return format_response(help_text, add_flair=False)

COMMAND_MAP: dict = {
    "status": cmd_status,
    "know me": cmd_know_me,
    "focus mode": cmd_pomodoro,
    "pomodoro": cmd_pomodoro,
    "youtube": cmd_open_youtube,
    "google": cmd_open_google,
    "email": cmd_open_email,
    "astrophage": cmd_astrophage,
    "taumoeba": cmd_taumoeba,
    "grace": cmd_grace,
    "help": cmd_help,
}

def execute(user_input: str) -> str:
    clean = user_input.strip().lower()
    if clean in COMMAND_MAP:
        return COMMAND_MAP[clean]()
    
    for key in sorted(COMMAND_MAP, key=len, reverse=True):
        if key in clean:
            return COMMAND_MAP[key]()

    return unknown_command()