from util.colors import YELLOW, BLUE, RED, ESC

def error(msg, *, end="\n"):
    print(f"- {RED}[ERROR]{ESC} {msg}", end=end)

def warn(msg, *, end="\n"):
    print(f"- {YELLOW}[ERROR]{ESC} {msg}", end=end)

def info(msg, *, end="\n"):
    print(f"- {BLUE}[INFO]{ESC} {msg}", end=end)