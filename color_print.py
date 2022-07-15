"""
Following Module helps to print colored text on console
"""
from colorama import Fore, Back


# printing text in RED 
def print_red(to_print):
    print(f"{Fore.RED}{Back.WHITE}{to_print}{Back.RESET}{Fore.RESET}")
    

# printing text in YELLOW
def print_yellow(to_print):
    print(f"{Fore.YELLOW}{Back.WHITE}{to_print}{Back.RESET}{Fore.RESET}")


# printing text in GREEN
def print_green(to_print):
    print(f"{Fore.GREEN}{Back.WHITE}{to_print}{Back.RESET}{Fore.RESET}")

