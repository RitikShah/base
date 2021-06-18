import random


def randcolor():
    return (
        round((random.randrange(0, 255) + 255) / 2),
        round((random.randrange(0, 255) + 255) / 2),
        round((random.randrange(0, 255) + 255) / 2),
    )
