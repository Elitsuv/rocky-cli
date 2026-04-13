import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if os.name == "nt":
    os.system("")

from rky.commands import execute
from rky.personality import format_response, load_user_profile
from rky.brain import brain

C = {
    "ROCKY":  "\033[38;5;130m",
    "GREEN":  "\033[38;5;48m",
    "DIM":    "\033[2m",
    "RESET":  "\033[0m",
    "CYAN":   "\033[38;5;51m",
}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def animate_processing():
    """Rocky scurries to fetch the data."""
    sys.stdout.write("\033[?25l")
    frames = [
        (f"  [{C['GREEN']}*{C['ROCKY']}██{C['GREEN']}*{C['ROCKY']}]  ", " // | \\\\ "),
        (f"  [{C['GREEN']}*{C['ROCKY']}██{C['GREEN']}*{C['ROCKY']}]  ", " \\\\ | // ")
    ]
    print("\n\n") 
    for i in range(15): 
        f1, f2 = frames[i % 2]
        pad = " " * (i * 3) 
        sys.stdout.write(f"\033[2A\r{pad}{C['ROCKY']}{f1}{C['RESET']}\033[K\n")
        sys.stdout.write(f"\r{pad}{C['ROCKY']}{f2}{C['RESET']} {C['DIM']}computing...{C['RESET']}\033[K\n")
        sys.stdout.flush()
        time.sleep(0.04)
        
    sys.stdout.write("\033[2A\r\033[K\n\r\033[K\033[?25h") 

def print_welcome_banner():
    print(f"\n{C['ROCKY']}██████╗  ██████╗  ██████╗██╗  ██╗██╗   ██╗")
    print(f"██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝╚██╗ ██╔╝")
    print(f"██████╔╝██║   ██║██║     █████╔╝  ╚████╔╝ ")
    print(f"██╔══██╗██║   ██║██║     ██╔═██╗   ╚██╔╝  ")
    print(f"██║  ██║╚██████╔╝╚██████╗██║  ██╗   ██║   ")
    print(f"╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝   {C['RESET']}")
    print(f"  {C['DIM']}Project Hail Mary — Astrophage Drive Online{C['RESET']}\n")
    
    print(f"  {C['CYAN']}── QUICK START GUIDE ─────────────────────────────{C['RESET']}")
    print(f"  {C['ROCKY']}todo add [task]{C['RESET']}   Log a new mission")
    print(f"  {C['ROCKY']}focus [mins]{C['RESET']}      Start deep work timer (e.g., 'focus 50')")
    print(f"  {C['ROCKY']}help{C['RESET']}              View all ship systems")
    print(f"  {C['ROCKY']}exit{C['RESET']}              Shut down Rocky")
    print(f"  {C['CYAN']}──────────────────────────────────────────────────{C['RESET']}\n")

def interactive_mode():
    clear_screen()
    print_welcome_banner()

    profile = load_user_profile()
    if not profile:
        print(execute("know me"))

    brain.start_heartbeat()

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
                
            animate_processing()

            response = execute(cmd)
            if response:
                print(response)

        except KeyboardInterrupt:
            print(format_response("Interrupt detected. Sleep time now. Goodbye."))
            sys.exit(0)

def main():
    arguments = sys.argv[1:]
    if arguments:
        user_command = " ".join(arguments).strip().lower()
        response = execute(user_command)
        if response:
            print(response)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()