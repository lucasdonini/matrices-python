import os, sys

def clear_terminal() -> None:
    if sys.stdout.isatty():
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n')