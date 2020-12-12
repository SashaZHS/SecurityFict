import random as rnd




def generate_password():
    while True:
        yield rnd.randint(0,10)