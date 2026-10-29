#!/usr/bin/env python3
"""
asci - turn a word into an ASCII picture, right in your terminal.

Works fully offline on Linux, macOS and Windows (Python 3.6+, no packages).

Usage (`asi` works the same as `asci`):
    asci cat              -> picture of a cat
    asci cat dog fish     -> several pictures
    asci hello            -> no picture known? prints big banner letters
    asci --list           -> show every word that has a picture
    asci --color red cat  -> colored output
    asci --banner cat     -> force big banner letters
"""

__version__ = "1.0.0"

import argparse
import difflib
import os
import sys

# --------------------------------------------------------------------------
# Picture library (all offline). Keys are lowercase words.
# --------------------------------------------------------------------------
ART = {
    "cat": r"""
   /\_/\
  ( o.o )
   > ^ <
  /     \
 (|     |)
  (_____)_/
""",
    "dog": r"""
   / \__
  (    @\___
  /         O
 /   (_____/
/_____/   U
""",
    "fish": r"""
       ___
   ___/   \___    /|
  /  o        \__/ |
 <    )))        < |
  \___     ___/  \ |
      \___/       \|
""",
    "bird": r"""
     ___
   _/ o \_
  <  ,__,  \
   \(    )  \___
    \\__//  ___/
     || ||
    _||_||_
""",
    "duck": r"""
    __
  <(o )___
   ( ._> /
    `---'
""",
    "owl": r"""
   ,___,
   (O,O)
   /)_)
  --"-"--
""",
    "rabbit": r"""
  (\(\
  ( -.-)
  o_(")(")
""",
    "bear": r"""
  _      _
 (c).--.(c)
  / o  o \
  \  (_)  /
  /'-..-'\
 (  |  |  )
  \_|__|_/
""",
    "cow": r"""
         (__)
         (oo)
  /-------\/
 / |     ||
*  ||----||
   ^^    ^^
""",
    "pig": r"""
    ^    ^
   / \__/ \
  (  o  o  )
   \ (oo) /__________
    '----'           )~
     |  ________   |
     |_|        |_|_|
""",
    "mouse": r"""
  ()-().----.          .
   \"/` ___  ;________.'
    ` ^^   ^^
""",
    "snake": r"""
           ____
          / . .\
          \  ---<
           \  /
   ________/ /
 -=:___________/
""",
    "turtle": r"""
      _____     ____
    /      \  |  o |
   |        |/ ___\|
   |_________/
   |_|_| |_|_|
""",
    "butterfly": r"""
  __     __
 /  \ | /  \
|    \|/    |
 \___ O ___/
 /    |    \
|    /|\    |
 \__/   \__/
""",
    "elephant": r"""
     __     __
    /  \~~~/  \
   (   (o o)   )
    \__ (  ) __/
       \|  |
   ____/   |
  |  __  __ |
  |_|  ||  |_|
""",
    "penguin": r"""
    _~_
   (o o)
  /  V  \
 /(  _  )\
   ^^ ^^
""",
    "frog": r"""
   @..@
  (----)
 ( >__< )
 ^^ ~~ ^^
""",
    "spider": r"""
   / _ \
 \_\(_)/_/
  _//o\\_
   /   \
""",
    "monkey": r"""
     .--.
   _/ .. \_
  ( |  ^  | )
   \  \_/  /
    '-...-'
""",
    "lion": r"""
    \\\|||///
  \\  .-.-.  //
 --  ( o o )  --
  //  \ ^ /  \\
    ///|||\\\
""",
    "heart": r"""
  ***     ***
 *****   *****
******* *******
 *************
   *********
     *****
       *
""",
    "star": r"""
       /\
______/  \______
 '.          .'
   '.      .'
   /   .  .  \
  /  .'  '.   \
 /.'        '. \
""",
    "house": r"""
       /\
      /  \
     /    \
    /______\
    | []   |
    |   __ |
    |__|  ||
""",
    "tree": r"""
       &&&
     &&&&&&&
   &&&&&&&&&&&
    &&&&&&&&&
      \ | /
       |||
       |||
     __|||__
""",
    "flower": r"""
     _ _
   _(_)_(_)_
  (_)  @  (_)
    (_)_(_)
       |
     \ | /
      \|/
""",
    "sun": r"""
     \   |   /
      .-'-.
 --- (     ) ---
      `-.-'
     /   |   \
""",
    "moon": r"""
    _.._
  .' .-'`
 /  /
 |  |
 \  \
  '._'-._
     ```
""",
    "car": r"""
       ______
   ___/__|___\___
  |  _       _   |
  '-(_)-----(_)--'
""",
    "rocket": r"""
     /\
    /  \
   |    |
   | () |
   |    |
  /|    |\
 /_|____|_\
    /\/\
""",
    "boat": r"""
        |\
        | \
        |  \
        |___\
  \--------------/
   \____________/
 ~~~~~~~~~~~~~~~~~~
""",
    "coffee": r"""
    ( (
     ) )
  ........
  |      |]
  \      /
   `----'
""",
    "cake": r"""
     , , ,
     | | |
  .-'-'-'-'-.
  |~~~~~~~~~|
  |  HAPPY  |
  '---------'
""",
    "computer": r"""
  .------------.
  |  >_        |
  |            |
  '------------'
     __|  |__
    [________]
""",
    "skull": r"""
    _____
   /     \
  | () () |
   \  ^  /
    |||||
""",
    "ghost": r"""
   .-.
  (o o)
  | O \
   \   \
    `~~~'
""",
    "umbrella": r"""
     .-^-.
   /_/_\_\
       |
       |
     \_|
""",
    "smile": r"""
   .-''''-.
  /  o  o  \
 |    __    |
  \  \__/  /
   '-....-'
""",
    "robot": r"""
    [___]
   |o   o|
   |  _  |
  [|_____|]
   /     \
  |_|   |_|
""",
    # ---- more animals ----
    "horse": r"""
                 ,/|
               _/ o \
   ___________/  ___/
  /             /
 / |  _______  |
   | |       | |
   | |       | |
   ^ ^       ^ ^
""",
    "sheep": r"""
      .-~~-.~~-.
  __ (          )
 /o \(          )
 \__/ (  .-~~-. )
       ||      ||
       ""      ""
""",
    "chicken": r"""
     ,,
    (o )>
   //\ \
  //  \ \___
  \\___     )
   \___\__/
      | |
     _| |_
""",
    "crab": r"""
  (\/)    (\/)
   \/ o  o \/
  .-(  __  )-.
 /  /      \  \
""",
    "octopus": r"""
     ___
   .'   '.
  (  o o  )
   \  ^  /
  //|| ||\\
 // || || \\
""",
    "whale": r"""
        ' .
         :
    _____:______      __
  /              \___/ /
 |  o                 <
  \_________________/\ \
 ~~~~~~~~~~~~~~~~~~~~~~~~
""",
    "shark": r"""
        |\
        | \
 _______|  \____
<  o            >---<
 '--------------'
 ~~~~~~~~~~~~~~~~~~~
""",
    "bat": r"""
  /\          /\
 /  \_(\_/)_/  \
/      (o.o)     \
\___/\_/   \_/\__/
""",
    "bee": r"""
     \_/
  ,-( oo)-,
 ( ((|||)) )>
  `-(___)-'
""",
    "snail": r"""
   @  @
    \/    .---.
   (oo)__/ .-. \
    \___  ( @ ) |
        \__'-'_/___
""",
    "fox": r"""
  /\   /\
 //\\_//\\
 \_     _/
  / * * \
  \_\O/_/
   /   \
""",
    "panda": r"""
   _       _
  (_)-----(_)
   / @   @ \
  |    v    |
   \  ---  /
   /'-----'\
  (_)     (_)
""",
    "koala": r"""
  @@       @@
 @@@@.---.@@@@
  @@ o   o @@
     \ _ /
     (___)
""",
    "hedgehog": r"""
     .|||||||||.
    |||||||||||||
   /. `|||||||||||
  o__,_||||||||||'
""",
    "camel": r"""
          __
   _.--._/ o\
  /  ^^^     '-.
 / /  ^^^  \___/
   |  |  |  |
   ^  ^  ^  ^
""",
    "dinosaur": r"""
               __
              / _)
     _.----._/ /
    /         /
 __/ (  | (  |
/__.-'|_|--|_|
""",
    "giraffe": r"""
    ^^
   (oo)__
    \  /
     ||
     ||
  ___||____
 /  o   o  \
 |____o____|
  ||     ||
  ||     ||
""",
    # ---- food ----
    "apple": r"""
       ,
    ,--./,-.
   /        \
  |          |
   \        /
    `._,._,'
""",
    "pizza": r"""
   _....._
 .'  o  o '.
(  o    o   )
 \ o   o   /
  \   o   /
   \ o   /
    \   /
     \ /
""",
    "icecream": r"""
    .-"-.
   /  .  \
  (  . .  )
   '-...-'
    \###/
     \#/
      V
""",
    "burger": r"""
   .-'''''-.
  / . . . . \
 |~~~~~~~~~~~|
 |###########|
 |~~~~~~~~~~~|
  '---------'
""",
    # ---- vehicles ----
    "train": r"""
      ___  ____
  ___|_|_|__|__|___
 |  [] []  []  [] |
 |________________|
  (O)(O)    (O)(O)
""",
    "plane": r"""
            __
            \ \_____
         ###[==_____>
            /_/
""",
    "bicycle": r"""
         __o
       _`\<,_
      (*)/ (*)
""",
    # ---- objects ----
    "crown": r"""
   *    *    *
  /\   /\   /\
 /  \_/  \_/  \
|  o   o   o   |
|______________|
""",
    "sword": r"""
       /\
       ||
       ||
       ||
       ||
    o==[]==o
       ||
       ()
""",
    "trophy": r"""
  ___________
 (|  WIN!   |)
  \         /
   '.     .'
     |   |
    _|___|_
   [_______]
""",
    "gift": r"""
     _   _
    ( \ / )
 ____\_V_/____
|      |      |
|______|______|
|      |      |
|      |      |
|______|______|
""",
    "balloon": r"""
   .---.
  /     \
 |       |
  \     /
   '._.'
     |
     (
      )
     (
""",
    "cloud": r"""
     .--.
  .-(    ).
 (___.__)__)
""",
    "snowman": r"""
     _===_
    (o . o)
    ( : : )
   (  : :  )
    '-----'
""",
    "castle": r"""
  |>>>          |>>>
  |             |
 _|_   _   _   _|_
|   |_| |_| |_|   |
|                 |
|       ___       |
|      |   |      |
|______|___|______|
""",
    "mail": r"""
 ________________
|\              /|
| \            / |
|  \__________/  |
|                |
|________________|
""",
    "lock": r"""
    .---.
   /  _  \
  |  / \  |
 .-----------.
 |    (o)    |
 |     |     |
 '-----------'
""",
    "key": r"""
  .--.
 /.-. '----------.
 \'-' .--"--""-"-'
  '--'
""",
    "bulb": r"""
    .---.
   /     \
  |  ~ ~  |
   \  ~  /
    |===|
    |===|
     \_/
""",
    "music": r"""
      |\
      | \
      |  |
      |
   .-.|
  (   )
   '-'
""",
    "anchor": r"""
     ___
    (   )
     | |
  ___| |___
 |___   ___|
     | |
 \   | |   /
  \__| |__/
    '---'
""",
    "diamond": r"""
   ________
  /_/____\_\
  \ \    / /
   \ \  / /
    \ \/ /
     \  /
      \/
""",
    "mushroom": r"""
    .-'~~~'-.
  .'  o   o  '.
 /   o   o  o  \
'-.___________.-'
      |   |
      |   |
     (_____)
""",
    "cactus": r"""
      _
     | |  _
  _  | | | |
 | | | |_| |
 | |_|  ___/
  \___ |
      | |
   ___|_|___
""",
    "pumpkin": r"""
       _
   .--' '--.
  / /\   /\ \
 |  ^^   ^^  |
 |   \/\/\/  |
  \         /
   '-.___.-'
""",
    "candle": r"""
     )
    (_)
    |=|
    | |
    | |
  __|_|__
""",
    "bomb": r"""
      ,--.
     ;    *
   .-'-.
  /     \
 |       |
  \     /
   '---'
""",
    "camera": r"""
   ___
 _/[_]\________
|    .---.  o |
|   ( ( ) )   |
|    '---'    |
'-------------'
""",
    "tv": r"""
  \   /
   \ /
 .--'--------.
 | .-------. |o
 | |       | |o
 | '-------' |
 '-----------'
""",
    "phone": r"""
  .-----.
  | ___ |
  ||   ||
  ||___||
  |  o  |
  '-----'
""",
    "book": r"""
   _______  _______
  /       \/       \
 | ~~~~~~  | ~~~~~~ |
 | ~~~~~~  | ~~~~~~ |
 | ~~~~~~  | ~~~~~~ |
  \_______/\_______/
""",
    "pencil": r"""
 ___________________
|___|_______________|\
|___|_______________|/
""",
    "clock": r"""
    .-----.
  .'  12   '.
 /     |     \
| 9    o--  3 |
 \           /
  '.   6   .'
    '-----'
""",
    "glasses": r"""
  ___       ___
 /   \_____/   \
|  o  |   |  o  |
 \___/     \___/
""",
    "guitar": r"""
          |=|
          |=|
          |=|
       .-'   '-.
      /   ( )   \
      \   ===   /
      /         \
      '.______.'
""",
}

# Other words that should show one of the pictures above.
ALIASES = {
    "kitty": "cat", "kitten": "cat", "meow": "cat",
    "puppy": "dog", "doggy": "dog", "woof": "dog",
    "bunny": "rabbit", "hare": "rabbit",
    "teddy": "bear",
    "rat": "mouse",
    "tortoise": "turtle",
    "love": "heart",
    "home": "house",
    "rose": "flower",
    "ship": "boat",
    "tea": "coffee", "cup": "coffee", "mug": "coffee",
    "birthday": "cake",
    "pc": "computer", "laptop": "computer",
    "happy": "smile", "smiley": "smile", "face": "smile",
    "bot": "robot",
    "pony": "horse", "lamb": "sheep",
    "hen": "chicken", "rooster": "chicken",
    "dino": "dinosaur", "trex": "dinosaur",
    "ice": "icecream", "ice-cream": "icecream",
    "hamburger": "burger",
    "airplane": "plane", "aeroplane": "plane", "jet": "plane",
    "bike": "bicycle", "cycle": "bicycle",
    "king": "crown", "queen": "crown",
    "present": "gift",
    "letter": "mail", "email": "mail",
    "padlock": "lock",
    "light": "bulb", "lightbulb": "bulb", "idea": "bulb",
    "note": "music", "song": "music",
    "gem": "diamond",
    "halloween": "pumpkin",
    "mobile": "phone", "smartphone": "phone",
    "television": "tv",
    "time": "clock", "watch": "clock",
    "specs": "glasses",
}

# --------------------------------------------------------------------------
# Fallback banner font (5 rows high) for words with no picture.
# --------------------------------------------------------------------------
FONT = {
    "A": [" ### ", "#   #", "#####", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#### ", "#   #", "#### "],
    "C": [" ####", "#    ", "#    ", "#    ", " ####"],
    "D": ["#### ", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#### ", "#    ", "#####"],
    "F": ["#####", "#    ", "#### ", "#    ", "#    "],
    "G": [" ####", "#    ", "#  ##", "#   #", " ### "],
    "H": ["#   #", "#   #", "#####", "#   #", "#   #"],
    "I": ["#####", "  #  ", "  #  ", "  #  ", "#####"],
    "J": ["#####", "   # ", "   # ", "#  # ", " ##  "],
    "K": ["#   #", "#  # ", "###  ", "#  # ", "#   #"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#####"],
    "M": ["#   #", "## ##", "# # #", "#   #", "#   #"],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", " ### "],
    "P": ["#### ", "#   #", "#### ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "# # #", "#  # ", " ## #"],
    "R": ["#### ", "#   #", "#### ", "#  # ", "#   #"],
    "S": [" ####", "#    ", " ### ", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", " ### "],
    "V": ["#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "# # #", "## ##", "#   #"],
    "X": ["#   #", " # # ", "  #  ", " # # ", "#   #"],
    "Y": ["#   #", " # # ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "   # ", "  #  ", " #   ", "#####"],
    "0": [" ### ", "#  ##", "# # #", "##  #", " ### "],
    "1": ["  #  ", " ##  ", "  #  ", "  #  ", " ### "],
    "2": [" ### ", "#   #", "  ## ", " #   ", "#####"],
    "3": ["#### ", "    #", " ### ", "    #", "#### "],
    "4": ["#   #", "#   #", "#####", "    #", "    #"],
    "5": ["#####", "#    ", "#### ", "    #", "#### "],
    "6": [" ### ", "#    ", "#### ", "#   #", " ### "],
    "7": ["#####", "   # ", "  #  ", " #   ", " #   "],
    "8": [" ### ", "#   #", " ### ", "#   #", " ### "],
    "9": [" ### ", "#   #", " ####", "    #", " ### "],
    " ": ["   ", "   ", "   ", "   ", "   "],
    "!": ["#", "#", "#", " ", "#"],
    "?": [" ### ", "#   #", "  ## ", "     ", "  #  "],
    ".": [" ", " ", " ", " ", "#"],
    "-": ["    ", "    ", "####", "    ", "    "],
}

COLORS = {
    "red": "31", "green": "32", "yellow": "33", "blue": "34",
    "magenta": "35", "cyan": "36", "white": "37",
}


def banner(text):
    """Render text in big block letters."""
    rows = ["", "", "", "", ""]
    for ch in text.upper():
        glyph = FONT.get(ch, FONT["?"])
        for i in range(5):
            rows[i] += glyph[i] + " "
    return "\n".join(r.rstrip() for r in rows)


def lookup(word):
    """Find a picture for a word. Returns (art, matched_name, guessed)."""
    w = word.lower().strip()
    candidates = [w]
    if w.endswith("es"):
        candidates.append(w[:-2])
    if w.endswith("s"):
        candidates.append(w[:-1])
    for c in candidates:
        if c in ART:
            return ART[c], c, False
        if c in ALIASES:
            return ART[ALIASES[c]], ALIASES[c], False
    # Typo tolerance, e.g. "elefant" -> "elephant"
    close = difflib.get_close_matches(w, list(ART) + list(ALIASES), n=1, cutoff=0.75)
    if close:
        name = ALIASES.get(close[0], close[0])
        return ART[name], name, True
    return None, None, False


def enable_windows_ansi():
    """Turn on ANSI color support in the Windows console."""
    if os.name == "nt":
        os.system("")


def main():
    parser = argparse.ArgumentParser(
        description="Show an ASCII picture for a word (works offline).")
    parser.add_argument("words", nargs="*", help="word(s) to draw, e.g. cat")
    parser.add_argument("-l", "--list", action="store_true",
                        help="list all words that have a picture")
    parser.add_argument("-b", "--banner", action="store_true",
                        help="always print big banner letters instead of a picture")
    parser.add_argument("-c", "--color", choices=sorted(COLORS),
                        help="color the output")
    parser.add_argument("-v", "--version", action="version",
                        version="asci " + __version__)
    args = parser.parse_args()

    if args.list:
        print("Pictures available:\n  " + ", ".join(sorted(ART)))
        print("\nAlso understood:\n  " + ", ".join(
            "%s->%s" % (k, v) for k, v in sorted(ALIASES.items())))
        return

    if not args.words:
        try:
            line = input("Enter a word: ")
        except (EOFError, KeyboardInterrupt):
            return
        args.words = line.split()
        if not args.words:
            return

    start, end = "", ""
    if args.color and sys.stdout.isatty():
        enable_windows_ansi()
        start, end = "\033[%sm" % COLORS[args.color], "\033[0m"

    if args.banner:
        print(start + banner(" ".join(args.words)) + end)
        return

    for word in args.words:
        art, name, guessed = lookup(word)
        if art:
            if guessed:
                print("(showing '%s' for '%s')" % (name, word))
            print(start + art.strip("\n") + end)
            print("  " + name.upper())
        else:
            print(start + banner(word) + end)
        print()


if __name__ == "__main__":
    main()
