import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if os.name == "nt":
    os.system("")

from rky.commands import execute
from rky.personality import format_response, load_user_profile

C = {
    "ROCKY":  "\033[38;5;130m",
    "DIM":    "\033[2m",
    "RESET":  "\033[0m",
}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_welcome_banner():
    # Simplified, sleek banner
    print(f"\n{C['ROCKY']}██████╗  ██████╗  ██████╗██╗  ██╗██╗   ██╗")
    print(f"██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝╚██╗ ██╔╝")
    print(f"██████╔╝██║   ██║██║     █████╔╝  ╚████╔╝ ")
    print(f"██╔══██╗██║   ██║██║     ██╔═██╗   ╚██╔╝  ")
    print(f"██║  ██║╚██████╔╝╚██████╗██║  ██╗   ██║   ")
    print(f"╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝   {C['RESET']}")
    
    print(f"  {C['DIM']}Project Hail Mary — Astrophage Drive Online{C['RESET']}\n")
    print(f"  Type {C['ROCKY']}help{C['RESET']} for commands. Type {C['ROCKY']}exit{C['RESET']} to shut down.\n")

def interactive_mode():
    clear_screen()
    print_welcome_banner()

    # First boot check
    profile = load_user_profile()
    if not profile:
        print(execute("know me"))

    while True:
        try:
            user_input = input(f"{C['ROCKY']}rocky>{C['RESET']} ").strip()

            if not user_input:
                continue

            cmd = user_input.lower()

            if cmd in ["exit", "quit", "shutdown"]:
                print(format_response("Sleep time now. Goodbye, friend."))
                sys.exit(0)

            if cmd == "clear":
                clear_screen()
                print_welcome_banner()
                continue

            response = execute(cmd)
            if response:
                print(response)

        except KeyboardInterrupt:
            print(format_response("Interrupt detected. Sleep time now. Goodbye."))
            sys.exit(0)

if __name__ == "__main__":
    arguments = sys.argv[1:]
    if arguments:
        user_command = " ".join(arguments).strip().lower()
        response = execute(user_command)
        if response:
            print(response)
    else:
        interactive_mode()