import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
import requests
import json
import time

class PuuidParser():
    def __init__(self):
        self.user_id = config.ID
        self.url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{ID}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Charset': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://developer.riotgames.com',
            'X-Riot-Token': 'RGAPI-c93fdce4-475c-4651-a0a9-f1d424747c83'
            }

    def get_puuid(self):
        response = requests.request("GET", self.url.format(ID=self.user_id), headers=self.headers)
        data = response.json()
        return data['id'], data['puuid']
#         return data
# user_id = PuuidParser()
# print(user_id.get_puuid())
