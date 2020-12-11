import CasinoRoyale.server as Casino
import CasinoRoyale.algoritm_random as alg
import random
import sys

user_id = random.randint(111, 9999999999)
print('user_id = {}'.format(user_id))


def create_user(casino):
    casino.create_user()
    return casino


def test_crack(model, casino, name):
    original_stdout = sys.stdout
    f = open('CasinoRoyale/result_{}.txt'.format(name), 'w')
    print(casino.account)
    i = 0
    sys.stdout = f
    print("TASK3!\nGAME ON!!!!")

    while 9 < int(casino.account['money']) < 1_000_000:
        nxt = model.next()
        try:
            casino.play(bet=int(casino.account['money']) // 10, number=nxt, print_data=True)
        except:
            break
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
    while True:
        try:
            print(lcg._crack(casino.history[-10:],count_of_parameters=2))
            break
        except Exception as e:
            print(e)
            [casino.play(bet=1, number=1, print_data=False) for i in range(10)]
            continue
    lcg.state = casino.play(bet=1, number=1, print_data=False)
    test_crack(lcg, casino, 'task1')
    casino.play(bet=casino.account['money'] - 1000, number=1, print_data=False)
    
    
def task2(casino):
    casino.mode = Casino.Mode.mt
    mt = alg.Mt()
    mt._crack(mt, casino.account['deletionTime'])
    test_crack(mt, casino, 'task2')
    casino.play(bet=casino.account['money'] - 1000, number=1, print_data=False)


def start():
    print('Creating User')
    casino = Casino.Server(user_id, Casino.Mode.lcg)
    casino = create_user(casino)
    print(casino)
