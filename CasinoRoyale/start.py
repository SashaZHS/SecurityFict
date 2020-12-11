import CasinoRoyale.server as Casino
import CasinoRoyale.algoritm_random as alg
import random
import sys

user_id = random.randint(111, 9999999999)
print('user_id = {}'.format(user_id))


def create_user(casino):
    casino.create_user()
    return casino


def crack(model, casino, **kwargs):
    while True:
        try:
            print(model._crack(casino.history[-10:], **kwargs))
            break
        except Exception as e:
            print(e)
            [casino.play(bet=1, number=1, print_data=False) for i in range(10)]
            continue
    return model, casino


def test_crack(model, casino, name):
    original_stdout = sys.stdout
    f = open('CasinoRoyale/result_{}.txt'.format(name), 'w')
    print(casino.account)
    i = 0
    sys.stdout = f
    print("TASK3!\nGAME ON!!!!")
    nxt = model.next()
    while 9 < int(casino.account['money']) < 1_000_000:
        last_money = int(casino.account['money'])
        i += 1
        print('step {}'.format(i))
        try:
            casino.play(bet=int(casino.account['money']) // 10, number=nxt, print_data=True)
            if last_money < casino.account['money']:
                nxt = model.next()
        except:
            nxt = model.next()
    if casino.account['money'] > 1_000_000:
        print("!!!You WIN!!!")
    else:
        print("!!!You LOSE!!!")
    print("Your Money: {}".format(casino.account['money']))
    f.close()
    sys.stdout = original_stdout


def task1(casino):
    casino.mode = Casino.Mode.lcg
    lcg = alg.Lcg()
    lcg.m = 2 ** 32
    lcg, casino = crack(lcg, casino, count_of_parameters=2)
    lcg.state = casino.play(bet=1, number=1, print_data=False)
    test_crack(lcg,casino, 'task1')
    casino.play(bet=casino.account['money']-1000, number=1, print_data=False)



def task2():
    print('I will only 4 houres sleep today. Now we are testing branches.')


def start():
    print('Creating User')
    casino = Casino.Server(user_id, Casino.Mode.lcg)
    casino = create_user(casino)
    print(casino)
    task1(casino)
    print(casino)
