import requests
import json

from . import cipher
from . import utils


class Client:
    BID = '000000000000000000000NFBR'
    AID = 'browser'
    AVER = '1.2.0'

    def __init__(self, loginid, password):
        self.loginid = loginid
        self.password = password
        self.u1 = None

    def get_u1(self):
        if self.u1:
            return self.u1

        login_url = 'https://jumpbookstore.com/top_login.html'
        payload = {
            'request': 'logon',
            'redirectTo': 'http://jumpbookstore.com/',
            'LOGINID': self.loginid,
            'PASSWORD': self.password
        }
        with requests.session() as s:
            s.post(login_url, data=payload)
            self.u1 = s.cookies['u1']
        return self.u1

    def get_li(self, cid):
        # see contentsLicense in bookshelf_1.2.5_2018-10-05.js
        endpoint = f'https://store.s-bookstore.jp/api4js/v1/c/{cid}/li'
        params = {
            'S': self.get_u1(),
            'BID': self.BID,
            'AID': self.AID,
            'AVER': self.AVER,
            'FORMATS': 'epub_brws,epub_brws_fixedlayout,epub_brws_omf',
            'W': '720',
            'H': '1280'
        }
        res = requests.get(endpoint, params=params)
        return json.loads(res.text)

    def gea(self, cid):
        endpoint = f'https://store.s-bookstore.jp/api4js/v1/c/{cid}'
        params = {
            'BID': self.BID,
            'AID': self.AID,
            'AVER': self.AVER,
            'FORMATS': 'epub_brws,epub_brws_fixedlayout,epub_brws_omf',
        }
        res = requests.get(endpoint, params=params)
        return json.loads(res.text)

    def get_si(self):
        # see getAccountShelfInfo in bookshelf_1.2.5_2018-10-05.js
        endpoint = 'https://store.s-bookstore.jp/api4js/v1/a/si'
        params = {
            'S': self.get_u1(),
            'BID': self.BID,
            'AID': self.AID,
            'AVER': self.AVER,
            'CLIENT_TIME': str(utils.get_time())
        }
        res = requests.get(endpoint, params=params)
        return json.loads(res.text)

    def get_contents_license(self, cid):
        data = self.get_li(cid)
        decrypted_license = cipher.decrypt_license(
            self.BID,
            self.get_u1(),
            data['license']
        )
        return json.loads(decrypted_license)
