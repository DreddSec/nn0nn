from colorama import Fore, Style, init
from pyfiglet import Figlet
init(autoreset=True)

SPIDER = r"""
               ...o..          ...   ..
            ...',,..;: .,,    ...   ..  .........
           ..:,......':. l 'oxl,'. '.  ..... . ...
          ...;;;;,'....c.,'Oxo,..',. ..  .        ...
        . .,,'.....,,',,c:xkdl;,,,'.........  .
        .,,. ..  ....,,:lxOkc:..',;'..    ... .      ..
      .;,.   ..',;;;;;;,o:ddo.,..'.'..      .....     ..
      ,.   .'l;.. ,;..  .''.',      ..       ...
     ..    .d..  .o...       .       .        .'.
     .    .l.... ., ..               .          ..
         .l..... ;.                  ..           .
        .o;      o                   ..           ..
        :.      .c                    .            .
        :       l,                    ..            .
        '      .l.                    ..            ..
        '       ,.                    ..             .
        .        '                     '
                 ,                     .
                 .                    ..
                  .                   ..
                  .


 """

VERSION = "v1.0.0"


fig = Figlet(font='banner')
TAGLINE = fig.renderText("Sh4d0w Spid3r")

def banner():
    print(Fore.RED + SPIDER)
    print(Fore.WHITE + Style.BRIGHT + "        nn0nn  " + Fore.RED + f"  {VERSION}")
    print(Fore.BLACK + Style.BRIGHT + f"        {TAGLINE}\n")

def info(msg):  print(Fore.CYAN   + f"  [*] {msg}")
def ok(msg):    print(Fore.GREEN  + f"  [+] {msg}")
def warn(msg):  print(Fore.YELLOW + f"  [!] {msg}")
def error(msg): print(Fore.RED    + f"  [-] {msg}")
def dim(msg):   print(Fore.BLACK  + Style.BRIGHT + f"      {msg}")
