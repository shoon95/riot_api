from .get_puuid import PuuidParser
import requests

class NowPlayingParser(PuuidParser):
    def __init__(self):
        super().__init__()
        self.live_client_url = 'https://127.0.0.1:2999/liveclientdata/allgamedata'

    def is_now_playing(self):
        summoneId, puuid = self.get_puuid()
        response = requests.request("GET", 'https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoneId}'.format(summoneId=summoneId), headers=self.headers)
        if response.status_code == 200:
            return response
        else:
            return False
    
    def get_playing_info(self, response):
        data = response.json()
        summoner_name = [i['summonerName'] for i in data['participants']]
        summoner_id = [i['summonerId'] for i in data['participants']]
        champion_id = [i['championId'] for i in data['participants']]
        game_id = data['gameId']
        game_start_time = data['gameStartTime']
        return summoner_name, summoner_id, game_id,game_start_time, champion_id
