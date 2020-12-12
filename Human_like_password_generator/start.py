import time
import datetime as dt
from Human_like_password_generator.generate_password import generate_password
import pandas as pd
from base64 import b64encode
import hashlib
import bcrypt
import uuid


def hashing_md5(count, gen_pswd):
    df = pd.DataFrame(columns=['hash'])
    df.hash = [gen_pswd.__next__() for i in range(count)]

    def hash_one_psw(data):
        print(data)
        return b64encode(hashlib.md5(bytes(data, encoding='ascii')).digest()).decode()

    df.hash = df.apply(lambda x: hash_one_psw(x.hash), axis=1)
    df.to_csv('Human_like_password_generator/data/hashing/hash_md5.csv')
    print('hashes saved')


def hashing_bcrypt(count, gen_pswd):
    df = pd.DataFrame(columns=['hash'])
    df.hash = [gen_pswd.__next__() for i in range(count)]
    i = 0

    def hash_one_psw(data):
        print(data)
        salt = bcrypt.gensalt(rounds=4)
        return bcrypt.hashpw(bytes(data.hash, encoding='ascii'), salt).decode()

    df.hash = df.apply(lambda x: hash_one_psw(x), axis=1)
    df.to_csv('Human_like_password_generator/data/hashing/hash_bcrypt.csv')
    print('hashes saved')


def hashing_sha1(count, gen_pswd):
    df = pd.DataFrame(columns=['hash'])
    df.hash = [gen_pswd.__next__() for i in range(count)]

    def hash_one_psw(data):
        salt = uuid.uuid4().hex
        return b64encode(hashlib.sha1(bytes(data.hash + salt, encoding='ascii')).digest()).decode()

    df.hash = df.apply(lambda x: hash_one_psw(x), axis=1)
    df.to_csv('Human_like_password_generator/data/hashing/hash_sha1.csv')
    print('hashes saved')


def start():
    count = 100000
    print('{}: Create password generator'.format(
        dt.datetime.now().strftime("%H:%M:%S")))
    gen_pasword = generate_password()
    # print('{}: hashing md5'.format(dt.datetime.now().strftime("%H:%M:%S")))
    # hashing_md5(count, gen_pasword)
    # time.sleep(10)
    #
    # print('{}: hashing sha1'.format(dt.datetime.now().strftime("%H:%M:%S")))
    # hashing_sha1(count, gen_pasword)
    # time.sleep(10)

    print('{}: hashing bcrypt'.format(dt.datetime.now().strftime("%H:%M:%S")))
    hashing_bcrypt(count, gen_pasword)
