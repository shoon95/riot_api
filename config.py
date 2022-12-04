import os
import pandas as pd
import openpyxl
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_DIR = os.path.join(ROOT_DIR, 'result')
DATA_DIR = os.path.join(ROOT_DIR, 'data')

file = [i for i in os.listdir(DATA_DIR) if 'xlsx' in i]
while True:
    try:
        id = pd.read_excel(os.path.join(DATA_DIR, file[0]))
        break
    except:
        print('엑셀이 열려있습니다. config id')
ID = id.loc[0,'ID']
if os.listdir(RESULT_DIR):
    while True:
        try:
            game_ids = pd.read_excel(os.path.join(RESULT_DIR, os.listdir(RESULT_DIR)[0]))
            game_ids = game_ids.loc[:, '게임id']
            game_ids = list(game_ids)
            if len(game_ids)==0:
                game_ids = None
            break
        except:
            print('엑셀이 열려있습니다. config result')
else:
    game_ids = None