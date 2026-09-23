"""Banner rendering."""

from colorama import Fore, Style


BANNER = rf"""
{Fore.CYAN}   ______      __       __             
  / ____/___  / /______/ /_  ____ _      
 / / __/ __ \/ __/ ___/ __ \/ __ `/      
/ /_/ / /_/ / /_/ /__/ / / / /_/ /       
\____/\____/\__/\___/_/ /_/\__,_/        
{Style.BRIGHT}{Fore.MAGENTA}Advanced Username & Email OSINT Tool{Style.RESET_ALL}
{Fore.YELLOW}Use responsibly. Adult platforms require --adult opt-in.{Style.RESET_ALL}
"""


def print_banner():
    print(BANNER)
