import random as rnd
import string
import json

symbols = '@-_.'


def random_password(length, charset=string.ascii_letters + string.digits + symbols):
    return ''.join(rnd.choices(charset, k=length))


def random_human_like_password(min_len=8, max_len=20):
    prob_word, prob_symbol, prob_number, prob_char = 0.7, 0.15, 0.5, 0.3
    password = []
    if rnd.random() < prob_word:
        words = json.load(open('Human_like_password_generator/data/words.json', 'rb'))
        password.append(rnd.choice(words['words']))
    if rnd.random() < prob_symbol:
        password.append(rnd.choice(symbols))
    if rnd.random() < prob_number:
        for i in range(rnd.choices((1, 2), (90, 10))[0]):
            password.append(str(rnd.randint(0, 2000)))
    if rnd.random() < prob_char:
        password.append(rnd.choice(string.ascii_letters))
    rnd.shuffle(password)
    password = ''.join(password)
    if len(password) > max_len:
        return password[:max_len]
    if len(password) < min_len:
        return password + random_human_like_password(min_len - len(password), max_len - len(password))
    return password




def generate_password():
    while True:
        yield random_human_like_password()
