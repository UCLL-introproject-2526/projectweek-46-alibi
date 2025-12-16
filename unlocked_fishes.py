

FILE_PATH = "textbestanden/unlocked_fishes.txt"


def load_unlocked_fishes():
   
    try:
        with open(FILE_PATH, "r") as f:
            fishes = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        fishes = []

    if "vis1" not in fishes:
        fishes.insert(0, "vis1")

    return fishes


def save_unlocked_fishes(unlocked_fishes):
    """
    Slaat de lijst van unlocked vissen op in het tekstbestand.
    """
    with open(FILE_PATH, "w") as f:
        for fish in unlocked_fishes:
            f.write(fish + "\n")
