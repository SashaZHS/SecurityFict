import CasinoRoyale.server as Casino
import CasinoRoyale.algoritm_random as alg
import random
import sys


def create_user(casino):
    casino.create_user()
    return casino


def test_crack(model, casino, name, file=False):
    original_stdout = sys.stdout
    f = open('CasinoRoyale/result_{}.txt'.format(name), 'w')
    print(casino.account)
    if file:
        sys.stdout = f
    print("{}!\nGAME ON!!!!".format(name.upper()))
    if '1' in name:
        nxt = model.next()
        while 9 < int(casino.account['money']) < 1_000_000:
            last_money = casino.account['money']
            try:
                casino.play(bet=int(casino.account['money']) // 10, number=nxt, print_data=True)
                if last_money < casino.account['money']:
                    nxt = model.next()
            except Exception as e:
                nxt = model.next()
    else:
        while 9 < int(casino.account['money']) < 1_000_000:
            nxt = model.next()
            try:
                casino.play(bet=int(casino.account['money']) // 10, number=nxt, print_data=True)
            except Exception as e:
                break
    if casino.account['money'] > 1_000_000:
        print("!!!You WIN!!!")
    else:
        print("!!!You LOSE!!!")
    print("Your Money: {}".format(casino.account['money']))
    f.close()
    sys.stdout = original_stdout
    print(casino.account)


def task1(user_id):
    print('Creating User {}'.format(user_id))
    casino = Casino.Server(user_id)
    casino = create_user(casino)
    casino.mode = Casino.Mode.lcg
    lcg = alg.Lcg()
    lcg.m = 2 ** 32
    while True:
        try:
            print(lcg._crack(casino.history[-10:], count_of_parameters=2))
            break
        except Exception as e:
            print(e)
            [casino.play(bet=1, number=1, print_data=False) for i in range(10)]
            continue
    lcg.state = casino.play(bet=1, number=1, print_data=False)
    test_crack(lcg, casino, 'task1', True)


def task2(user_id):
    print('Creating User {}'.format(user_id))
    casino = Casino.Server(user_id)
    casino = create_user(casino)
    casino.mode = Casino.Mode.mt
    mt = alg.Mt()
    mt._crack(mt, casino.account['deletionTime'])
    test_crack(mt, casino, 'task2', True)


def task3(user_id):
    print('Creating User {}'.format(user_id))
    casino = Casino.Server(user_id)
    casino = create_user(casino)
    casino.mode = Casino.Mode.better_mt
    states = [casino.play(1, i, False) for i in range(624)]
    better_mt = alg.BetterMt()
    better_mt._crack(states)
    test_crack(better_mt, casino, 'task3', file=True)


def start():
    # print(casino)
    task1(random.randint(111, 9999999999))
    task2(random.randint(111, 9999999999))
    task3(random.randint(111, 9999999999))
