# asci

Type a word, get an ASCII picture in your terminal. Works **offline** on Linux, macOS and Windows.
It's a single Python file with no dependencies.

```
$ asci cat
   /\_/\
  ( o.o )
   > ^ <
  /     \
 (|     |)
  (_____)_/
  CAT
```

## Install

**Linux / macOS (system-wide, with sudo):**

```sh
curl -fsSL https://raw.githubusercontent.com/wetpant000/asci/main/install.sh | sudo sh
```

or from a clone of this repo:

```sh
git clone https://github.com/wetpant000/asci.git
cd asci
sudo sh install.sh
```

**Any OS with pip (including Windows):**

```sh
pip install asci
```

Both install two commands, `asci` and `asi`, which do the same thing.

## Usage

```sh
asci cat                 # picture of a cat
asi dog fish rocket      # several pictures
asci --color green tree  # colors: red green yellow blue magenta cyan white
asci hello               # no picture for this word? prints big letters
asci --banner hi         # always print big letters
asci --list              # every word with a picture
```

There are 90 pictures, including cat, dog, panda, dinosaur, whale, pizza, rocket, castle, guitar and pumpkin.
Related words like `kitty`, `puppy`, `bike` and `airplane` work, and so do plurals and small typos.

## Uninstall

```sh
sudo sh uninstall.sh     # or: pip uninstall asci
```

## Add your own picture

Add an entry to the `ART` dictionary in `asci.py`:

```python
"word": r"""
  your art here
""",
```

## License

MIT
