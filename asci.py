#!/usr/bin/env python3
"""
asci - turn a word into an ASCII picture, right in your terminal.

Works fully offline on Linux, macOS and Windows (Python 3.6+, no packages).

Usage (`asi` works the same as `asci`):
    asci cat                  -> picture of a cat
    asci cat dog fish         -> several pictures
    asci --side cat dog       -> pictures next to each other
    asci -s "hi there" cat    -> cat with a speech bubble
    asci -r                   -> random picture
    asci hello                -> no picture known? prints big banner letters
    asci -l [animals]         -> list pictures (optionally one category)
    asci -c rainbow cat       -> colored output
    asci --add dragon my.txt  -> save your own picture
    echo cat | asci           -> read words from a pipe
"""

__version__ = "1.1.0"

import argparse
import difflib
import os
import random
import sys
import textwrap

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
RAINBOW = ["31", "33", "32", "36", "34", "35"]

CATEGORIES = {
    "animals": [
        "cat", "dog", "fish", "bird", "duck", "owl", "rabbit", "bear", "cow",
        "pig", "mouse", "snake", "turtle", "butterfly", "elephant", "penguin",
        "frog", "spider", "monkey", "lion", "horse", "sheep", "chicken", "crab",
        "octopus", "whale", "shark", "bat", "bee", "snail", "fox", "panda",
        "koala", "hedgehog", "camel", "dinosaur", "giraffe",
    ],
    "food": ["apple", "pizza", "icecream", "burger", "cake", "coffee"],
    "vehicles": ["car", "rocket", "boat", "train", "plane", "bicycle"],
    "nature": ["tree", "flower", "sun", "moon", "star", "cloud", "cactus",
               "mushroom", "snowman"],
}

# Characters swapped when a picture is mirrored with --flip.
MIRROR = str.maketrans("/\\()<>[]{}bdpq", "\\/)(><][}{dbqp")


def user_art_dir():
    """Folder holding the user's own pictures (one <word>.txt per picture)."""
    if os.environ.get("ASCI_HOME"):
        return os.environ["ASCI_HOME"]
    if os.name == "nt" and os.environ.get("APPDATA"):
        return os.path.join(os.environ["APPDATA"], "asci")
    return os.path.join(os.path.expanduser("~"), ".asci")


def load_user_art():
    """Add the user's own pictures to ART. Returns their names."""
    folder = user_art_dir()
    names = []
    if not os.path.isdir(folder):
        return names
    for fname in sorted(os.listdir(folder)):
        if fname.endswith(".txt"):
            name = fname[:-4].lower()
            with open(os.path.join(folder, fname), encoding="utf-8") as f:
                ART[name] = "\n" + f.read().strip("\n") + "\n"
            names.append(name)
    return names


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


def flip(text):
    """Mirror a picture left-to-right."""
    lines = text.split("\n")
    width = max(len(l) for l in lines)
    return "\n".join(l.ljust(width)[::-1].translate(MIRROR).rstrip() for l in lines)


def frame(text):
    """Draw a box around a picture."""
    lines = text.split("\n")
    width = max(len(l) for l in lines)
    edge = "+" + "-" * (width + 2) + "+"
    return "\n".join([edge] + ["| " + l.ljust(width) + " |" for l in lines] + [edge])


def bubble(text, width=40):
    """Speech bubble with a tail pointing down at the picture."""
    lines = textwrap.wrap(text, width) or [""]
    w = max(len(l) for l in lines)
    out = [" " + "_" * (w + 2)]
    if len(lines) == 1:
        out.append("< " + lines[0].ljust(w) + " >")
    else:
        for i, l in enumerate(lines):
            if i == 0:
                left, right = "/", "\\"
            elif i == len(lines) - 1:
                left, right = "\\", "/"
            else:
                left, right = "|", "|"
            out.append(left + " " + l.ljust(w) + " " + right)
    out += [" " + "-" * (w + 2), "    \\", "     \\"]
    return "\n".join(out)


def side_by_side(blocks, gap=4):
    """Join several pictures horizontally, aligned at the bottom."""
    split = [b.split("\n") for b in blocks]
    widths = [max(len(l) for l in lines) for lines in split]
    height = max(len(lines) for lines in split)
    split = [[""] * (height - len(lines)) + lines for lines in split]
    rows = []
    for i in range(height):
        rows.append((" " * gap).join(
            split[j][i].ljust(widths[j]) for j in range(len(split))).rstrip())
    return "\n".join(rows)


def colorize(text, color):
    if not color:
        return text
    if color == "rainbow":
        return "\n".join("\033[%sm%s\033[0m" % (RAINBOW[i % len(RAINBOW)], l)
                         for i, l in enumerate(text.split("\n")))
    return "\033[%sm%s\033[0m" % (COLORS[color], text)


def enable_windows_ansi():
    """Turn on ANSI color support in the Windows console."""
    if os.name == "nt":
        os.system("")


def print_list(category, custom):
    groups = dict(CATEGORIES)
    listed = {n for names in CATEGORIES.values() for n in names}
    groups["objects"] = sorted(n for n in ART if n not in listed and n not in custom)
    if custom:
        groups["custom"] = custom
    if category != "all":
        if category not in groups:
            sys.exit("Unknown category '%s'. Choose from: %s"
                     % (category, ", ".join(groups)))
        groups = {category: groups[category]}
    for name, items in groups.items():
        print("%s (%d):" % (name.upper(), len(items)))
        print(textwrap.fill(", ".join(sorted(items)), 76,
                            initial_indent="  ", subsequent_indent="  "))
        print()
    if category == "all":
        print("%d pictures. Aliases also work, e.g. kitty, puppy, bike, airplane."
              % len(ART))


def add_art(name, path):
    name = name.lower()
    if not name.replace("-", "").isalnum():
        sys.exit("Name must be letters, numbers or '-': %s" % name)
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        sys.exit("Cannot read %s: %s" % (path, e))
    folder = user_art_dir()
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, name + ".txt"), "w", encoding="utf-8") as f:
        f.write(text)
    print("Added '%s'. Try: asci %s" % (name, name))


def remove_art(name):
    path = os.path.join(user_art_dir(), name.lower() + ".txt")
    if not os.path.exists(path):
        sys.exit("'%s' is not one of your own pictures (built-ins can't be removed)."
                 % name)
    os.remove(path)
    print("Removed '%s'." % name)


def main():
    parser = argparse.ArgumentParser(
        prog="asci",
        description="Show an ASCII picture for a word (works offline). "
                    "`asi` is the same command.",
        epilog="examples:  asci cat | asci -s 'hello!' dog | asci --side cat dog "
               "| asci -r -c rainbow | asci -l animals")
    parser.add_argument("words", nargs="*", help="word(s) to draw, e.g. cat")
    parser.add_argument("-l", "--list", nargs="?", const="all", metavar="CATEGORY",
                        help="list pictures (optionally one category: animals, "
                             "food, vehicles, nature, objects, custom)")
    parser.add_argument("-r", "--random", action="store_true",
                        help="show a random picture")
    parser.add_argument("-s", "--say", metavar="TEXT",
                        help="add a speech bubble above the picture")
    parser.add_argument("-c", "--color", choices=sorted(COLORS) + ["rainbow"],
                        help="color the output")
    parser.add_argument("-f", "--flip", action="store_true",
                        help="mirror the picture left-to-right")
    parser.add_argument("--border", action="store_true",
                        help="draw a box around each picture")
    parser.add_argument("--side", action="store_true",
                        help="show several pictures next to each other")
    parser.add_argument("--no-label", action="store_true",
                        help="don't print the name under the picture")
    parser.add_argument("-b", "--banner", action="store_true",
                        help="print big banner letters instead of a picture")
    parser.add_argument("--add", nargs=2, metavar=("NAME", "FILE"),
                        help="save your own picture from a text file")
    parser.add_argument("--remove", metavar="NAME",
                        help="delete one of your own pictures")
    parser.add_argument("-v", "--version", action="version",
                        version="asci " + __version__)
    args = parser.parse_args()

    if args.add:
        return add_art(*args.add)
    if args.remove:
        return remove_art(args.remove)

    custom = load_user_art()

    if args.list:
        return print_list(args.list.lower(), custom)

    words = list(args.words)
    if args.random:
        words.append(random.choice(sorted(ART)))
    if not words:
        if sys.stdin.isatty():
            try:
                words = input("Enter a word: ").split()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        else:
            words = sys.stdin.read().split()
        if not words:
            return

    color = None
    if args.color and sys.stdout.isatty() and not os.environ.get("NO_COLOR"):
        enable_windows_ansi()
        color = args.color

    if args.banner:
        blocks = [banner(" ".join(words))]
    else:
        blocks = []
        for word in words:
            art, name, guessed = lookup(word)
            if art:
                if guessed:
                    print("(showing '%s' for '%s')" % (name, word), file=sys.stderr)
                block = art.strip("\n")
                if args.flip:
                    block = flip(block)
                if not args.no_label:
                    block += "\n  " + name.upper()
            else:
                block = banner(word)
            blocks.append(block)

    if args.border:
        blocks = [frame(b) for b in blocks]
    if args.say:
        blocks[0] = bubble(args.say) + "\n" + blocks[0]

    if args.side and len(blocks) > 1:
        print(colorize(side_by_side(blocks), color))
    else:
        print("\n\n".join(colorize(b, color) for b in blocks))


if __name__ == "__main__":
    main()
