import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from utils.get_now_playing import NowPlayingParser
import time
from datetime import datetime
import requests
import pandas as pd

class LiveDataParser():
    def __init__(self):
        self.now_playing = ''
        self.is_now_playing = ''
        self.game_ids = config.game_ids
        self.flag = 1

    def get_parser(self):
        print(3)
        self.now_playing = NowPlayingParser()
        print(4)
        self.is_now_playing = self.now_playing.is_now_playing()
        print(5)
        while True:
            print('요청 중')
            if self.is_now_playing:
                self.summoner_name, self.summoner_id, self.game_id, self.get_start_time, self.champion_id = self.now_playing.get_playing_info(self.is_now_playing)
                if self.game_ids and self.game_id in self.game_ids:
                    print('게임 이미 수집되었습니다')
                    self.flag = 0
                    break
                else:
                    self.data_1 = {}
                    self.data_2 = {}
                    time.sleep(5)
                    break
            else:
                time.sleep(5)
                self.flag = 0
                print('게임을 시작하지 않았습니다.')
                self.is_now_playing = self.now_playing.is_now_playing()

    def get_live_data(self):
        data = requests.get('https://127.0.0.1:2999/liveclientdata/allgamedata', verify=False)
        data = data.json()

        self.data_1['ID'] = self.summoner_id
        self.data_1['이름'] = self.summoner_name
        self.data_1['날짜'] = [datetime.now()]*len(self.data_1['이름'])
        self.data_1['게임 시작 시간'] = [self.get_start_time]*len(self.data_1['이름'])
        self.data_1['게임id'] = [self.game_id]*len(self.data_1['이름'])
        data_1 = pd.DataFrame(self.data_1)
        
        all_players = data['allPlayers']
        self.data_2['챔피언'] = [player['championName'] for player in all_players]
        self.data_2['이름'] = [player['summonerName'] for player in all_players]
        self.data_2['팀'] = [player['team'] for player in all_players]
        self.data_2['스펠 1'] = [player['summonerSpells']['summonerSpellOne']['displayName'] for player in all_players]
        self.data_2['스펠 2'] = [player['summonerSpells']['summonerSpellTwo']['displayName'] for player in all_players]
        self.data_2['룬1'] = [player['runes']['keystone']['displayName'] for player in all_players]
        self.data_2['룬2'] = [player['runes']['primaryRuneTree']['displayName'] for player in all_players]
        self.data_2['룬3'] = [player['runes']['secondaryRuneTree']['displayName'] for player in all_players]
        
        events = data['events']
        self.data_2['퍼스트블러드'] = [event['Recipient'] for event in events['Events'] if event['EventName'] == 'FirstBlood']*len(self.data_2['이름'])
        while True:
            if self.data_2['퍼스트블러드']:
                data_2 = pd.DataFrame(self.data_2)
                merged_data = pd.merge(data_1, data_2, on='이름', how='left')
                break
            else:
                
                time.sleep(60)
                try:
                    data = requests.get('https://127.0.0.1:2999/liveclientdata/allgamedata', verify=False)
                    data = data.json()
                    events = data['events']
                    self.data_2['퍼스트블러드'] = [event['Recipient'] for event in events['Events'] if event['EventName'] == 'FirstBlood']*len(self.data_2['이름'])
                    print('퍼스트 블러드가 아직 나오지 않았습니다.')
                except:
                    print('게임이 종료 되었습니다.')

        return merged_data


