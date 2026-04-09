import random
import json
import os

C = {
    "ROCKY":   "\033[38;5;130m",      
    "QUEST":   "\033[38;5;208m",      
    "ANSWER":  "\033[38;5;196m",     
    "DIM":     "\033[2m",             
    "RESET":   "\033[0m",             
}

FLAIR_LINES = [
    "Amaze! Amaze! Amaze!",
    "Fist my bump!",
    "We do science now!",
    "Logic is good. Panic is not.",
    "Question → hypothesis → test. Always.",
    "Bad space magic. But we fix.",
    "Human brain: surprisingly good.",
    "I understand now. Mostly.",
    "Astrophage: bad. Science: good.",
    "You are good human. Rocky certain.",
    "Yes yes yes!",
]

UNKNOWN_RESPONSES = [
    "Not understand. Say again?",
    "Command not in memory banks. Try 'help'.",
    "Hm. Unknown input. Rocky confused.",
    "Question is unclear. Rephrase, friend?",
]

USER_PROFILE_FILE = os.path.join(os.path.dirname(__file__), "..", "user_profile.json")

def load_user_profile():
    if os.path.exists(USER_PROFILE_FILE):
        try:
            with open(USER_PROFILE_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_user_profile(profile):
    try:
        os.makedirs(os.path.dirname(USER_PROFILE_FILE), exist_ok=True)
        with open(USER_PROFILE_FILE, "w") as f:
            json.dump(profile, f, indent=4)
        return True
    except:
        return False

def get_user_name():
    profile = load_user_profile()
    return profile.get("name", "Human")

def format_response(message: str, add_flair: bool = True) -> str:
    """Wraps a message in Rocky's visual style with user's name."""
    user_name = get_user_name()
    lines = message.strip().splitlines()
    
    formatted = f"\n{C['ROCKY']}◆ Rocky to {user_name}:{C['RESET']} "

    if len(lines) == 1:
        formatted += f"{C['ANSWER']}{lines[0]}{C['RESET']}"
    else:
        formatted += f"\n"
        for line in lines:
            if line.strip():
                formatted += f"  {C['ANSWER']}{line.strip()}{C['RESET']}\n"

    if add_flair:
        flair = random.choice(FLAIR_LINES)
        formatted += f"\n  {C['DIM']}✦ {flair}{C['RESET']}"

    formatted += "\n"
    return formatted

def format_question(question: str) -> str:
    """Format a question prompt in orange to show curiosity."""
    return f"{C['QUEST']}❓ {question}{C['RESET']}"

def unknown_command() -> str:
    return format_response(random.choice(UNKNOWN_RESPONSES))