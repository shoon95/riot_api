import os, sys
import time
import config
from modules.get_live_data import LiveDataParser
import pandas as pd


if __name__ == '__main__':
    while True:
        data_parser = LiveDataParser()
        data_parser.get_parser()
        if data_parser.flag==1:
            while True:
                try:
                    if config.game_ids:
                        print(1)
                        origin_data = pd.read_excel(os.path.join(config.RESULT_DIR, os.listdir(config.RESULT_DIR)[0]))
                        origin_data = origin_data.iloc[:,1:]
                        data = data_parser.get_live_data()
                        data = pd.concat([origin_data, data], axis=0)
                        config.game_ids = data.loc[:, '게임id']
                        config.game_ids = list(config.game_ids)
                        data.to_excel(os.path.join(config.RESULT_DIR, 'result.xlsx'))
                        print('데이터가 저장 되었습니다.')
                        time.sleep(10)
                        break
                    else:
                        print(2)
                        data = data_parser.get_live_data()
                        data.to_excel(os.path.join(config.RESULT_DIR, 'result.xlsx'))
                        config.game_ids = data.loc[:, '게임id']
                        config.game_ids = list(config.game_ids)
                        print('데이터가 저장 되었습니다.')
                        time.sleep(10)
                        break
                except:
                    print('엑셀이 열려있습니다. return')
        else:
            time.sleep(10)