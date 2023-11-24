import random

def rand_free_or_taken():
    rand = random.random()
    if rand > 0.5:
        return True
    return False