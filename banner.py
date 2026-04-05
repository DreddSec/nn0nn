from colorama import Fore, Style, init
init(autoreset=True)

SPIDER = r"""
       /^\                /^\
      / : \______________/ : \
     /  :  \            /  :  \
    / .:::. \          / .:::. \
   /  :::::  \________/  :::::  \
  / .:::::::.  \  /  / .:::::::.  \
 /  ::::::::  (    ) ::::::::  \
            \  \__/  /
             \_|  |_/
              |    |
           ( (      ) )
           ( (  ()  ) )
              \ '' /
               \--/
"""

EYES = r"""
              [* *]
               \-/
"""

VERSION = "v1.0.0"
TAGLINE = "passive recon & surface mapper"

def banner():
    print(Fore.RED + SPIDER)
    print(Fore.WHITE + Style.BRIGHT + "        nn0nn  " + Fore.RED + f"  {VERSION}")
    print(Fore.BLACK + Style.BRIGHT + f"        {TAGLINE}\n")

def info(msg):  print(Fore.CYAN   + f"  [*] {msg}")
def ok(msg):    print(Fore.GREEN  + f"  [+] {msg}")
def warn(msg):  print(Fore.YELLOW + f"  [!] {msg}")
def error(msg): print(Fore.RED    + f"  [-] {msg}")
def dim(msg):   print(Fore.BLACK  + Style.BRIGHT + f"      {msg}")
