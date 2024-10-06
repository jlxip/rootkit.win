"""rootkit.web connection entrypoint"""

RED = "\033[1;31m"
GREEN = "\033[1;32m"
MAGENTA = "\033[1;35m"
CYAN = "\033[1;36m"
RESET = "\033[0m"
BANNER = f"""{RED}                     __{RESET}{CYAN}  __   _ __{RESET}{GREEN}           _{RESET}
{RED}   _________  ____  / /_{RESET}{CYAN}/ /__(_) /{RESET}{GREEN}__      __(_)___{RESET}
{RED}  / ___/ __ \\/ __ \\/ __{RESET}{CYAN}/ //_/ / __{RESET}{GREEN}/ | /| / / / __ \\{RESET}
{RED} / /  / /_/ / /_/ / /_{RESET}{CYAN}/ ,< / / /_{RESET}{MAGENTA}_{RESET}{GREEN}| |/ |/ / / / / /{RESET}
{RED}/_/   \\____/\\____/\\__{RESET}{CYAN}/_/|_/_/\\__{RESET}{MAGENTA}(_){RESET}{GREEN}__/|__/_/_/ /_/{RESET}"""


def main() -> None:
    """Beginning of connection"""
    print(BANNER)
    print()
    print('Log in (or "anonymous")')
    user = input("User: ")
    if user != "anonymous":
        pwd = input("Password: \033[8m")
        # TODO
        print("\033[28mIncorrect password")
        return

    print("\nYou have logged in as anonymous\n")
