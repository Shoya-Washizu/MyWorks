#githubの使い方:https://qiita.com/A__Matsuda/items/f71a935612a55d6e674e
# git add .
# git commit -m "yyyymmdd"
# git push

import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageOps
import cardmake as cm
import datetime
import os
import glob

def makepandas(NUM_CARD): #NUM_CARD...読み込み数を指定
    input_book = pd.ExcelFile("./carddata.xlsx")
    #sheet_namesメソッドでExcelブック内の各シートの名前をリストで取得できる
    input_sheet_name = input_book.sheet_names
    #lenでシートの総数を確認
    num_sheet = len(input_sheet_name)
    input_sheet= input_sheet_name[0]
    input_sheet_df = input_book.parse(input_sheet)
    return (input_sheet_df.head(NUM_CARD))

def maketimeOS():
    now = datetime.datetime.now()
    current_time = now.strftime("%y-%m-%d-%H-%M-%S")
    dir_for_output = "./outputs/" + current_time
    #dir_for_output = "./outputs/test1"

    os.makedirs(dir_for_output, exist_ok=True)
    return dir_for_output


if __name__ == "__main__": 
    N = 96 #作成枚数
    pandafile = makepandas(N)
    output_path = maketimeOS()
    print(output_path)
    for i in range (N):
        card = cm.Card(i,pandafile)
        card_fig = card.plot_img()
        print("make card {}'s fig".format(i+1))
        card_fig = card.plot_txt(card_fig)
        print("make card {}'s text".format(i+1))
        card_fig = card.plot_title(card_fig)
        card_fig.save(output_path + "/" + str(i+1) +".png")
    i = N - 1
    files = glob.glob("../materials/cards/*.png")
    for file in files:
        i += 1
        fg = Image.open(file).convert("RGBA")
        fg.save(output_path + "/" + str(i+1) +".png")
    #card_fig_for_print = cm.card_print(output_path, i+1)