import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if os.name == "nt":
    os.system("")

from rky.commands import execute
from rky.personality import format_response, load_user_profile

C = {
    "ROCKY":  "\033[38;5;130m",
    "GREEN":  "\033[38;5;48m",
    "DIM":    "\033[2m",
    "RESET":  "\033[0m",
}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def animate_rocky():
    """A fast 2-frame ASCII animation of Rocky processing input."""
    frames = [
        (f"  [{C['GREEN']}*{C['ROCKY']}██{C['GREEN']}*{C['ROCKY']}]  ", " // | \\\\ "),
        (f"  [{C['GREEN']}*{C['ROCKY']}██{C['GREEN']}*{C['ROCKY']}]  ", " \\\\ | // ")
    ]
    
    # Hide the blinking terminal cursor
    sys.stdout.write("\033[?25l")
    
    # Print two blank lines to make room for Rocky
    print("\n\n") 
    
    # Shorter distance (25) and faster sleep (0.04) so it's snappy!
    for i in range(25): 
        f1, f2 = frames[i % 2]
        pad = " " * (i * 2) # Multiply by 2 to make him move across the screen faster
        
        sys.stdout.write(f"\033[2A\r{pad}{C['ROCKY']}{f1}{C['RESET']}\033[K\n")
        sys.stdout.write(f"\r{pad}{C['ROCKY']}{f2}{C['RESET']}\033[K\n")
        sys.stdout.flush()
        time.sleep(0.04)
        
    # Clear the animation lines after he's done walking to keep the chat clean
    sys.stdout.write("\033[2A\r\033[K\n\r\033[K") 
    
    # Show cursor again
    sys.stdout.write("\033[?25h")

def print_welcome_banner():
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
                
            # Rocky scurries to process your command!
            animate_rocky()

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