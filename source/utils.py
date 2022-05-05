import random
# from source import random


def roll(mod: int) -> int:
    return random.randint(0, mod-1)
