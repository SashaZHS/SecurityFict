import CasinoRoyale.server as Casino
import CasinoRoyale.algoritm_random as alg
import random
import sys


user_id = random.randint(111, 9999999999)
print('user_id = {}'.format(user_id))


def task1(casino):
    casino.create_user()
    print(casino)
    lcg = alg.Lcg()
    lcg.m = 2 ** 32
    while True:
        try:
            print(lcg._crack_unknown_multiplier(casino.history[-10:]))
            break
        except Exception as e:
            print(e)
            [casino.play(bet=1, number=1, print_data=False) for i in range(11)]
            continue
    lcg.state = casino.play(bet=1, number=1, print_data=False)
    print(casino.account)
    i = 0
    print("GAME ON!!!!")
    nxt = lcg.next()
    while 9 < int(casino.account['money']) < 1_000_000:
        last_money = int(casino.account['money'])
        i += 1
        print(i)
        try:
            casino.play(bet=int(casino.account['money']) // 10, number=nxt, print_data=True)
            if last_money < casino.account['money']:
                nxt = lcg.next()
        except:
            nxt = lcg.next()
    if casino.account['money']>1_000_000:
        print("☻♥♥You WIN♥♥☻")
    else:
        print("♠♠♠You LOSE♠♠♠")
    print("Your Money: {}".format(casino.account['money']))


def start():
    print('Creating User')
    casino = Casino.Server(user_id, Casino.Mode.lcg)
    task1(casino)
