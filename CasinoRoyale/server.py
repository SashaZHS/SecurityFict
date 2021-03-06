import requests as rq

class Mode:
    lcg = 'Lcg'
    mt = 'Mt'
    better_mt = 'BetterMt'


class Server:
    def __init__(self, user_id, mode=Mode.lcg):
        self.account = {
            "id": user_id,
            "money": 0,
            "deletionTime": ""
        }
        self.mode = mode
        self.__create_link = 'http://95.217.177.249/casino/createacc?id={}'
        self.__play_link = 'http://95.217.177.249/casino/play{}?id={}&bet={}&number={}'
        self.history = []

    def info(self):
        return {
            'account': self.account,
            'mode': self.mode,
            'history': self.history
        }

    def __repr__(self):
        return self.info().__str__()

    def clear_history(self):
        self.history = []

    def create_user(self):
        self.clear_history()
        user = rq.get(self.__create_link.format(self.account['id'])).json()
        if 'error' in user:
            print(user['error'])
            return
        self.account = user
        print('created user {}'.format(self.account['id']))

    def play(self, bet, number, print_data=True):
        try:
            res = rq.get(self.__play_link.format(self.mode, self.account['id'], bet, number)).json()
            if 'error' in res:
                print('ERROR: {}'.format(res['error']))
                return
            self.history.append(int(res['realNumber']))
            self.account = res['account']
            if print_data:
                print('''{}! Your balance: {};
                         Your Number = {};
                         Real Number = {};'''.format(res['message'], self.account['money'], number, res['realNumber']))
            return res['realNumber']
        except Exception as e:
            print('No valid input data')
            raise e
