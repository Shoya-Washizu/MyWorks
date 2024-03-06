import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops, ImageEnhance
import math
import glob

def paste(base, on_path): #ベース画像と載せたい画像のパスのpngを合成

    logo = Image.open(on_path)

    # base.paste(logo, (0, 0))
    base.paste(logo, (0, 0), logo)
    return base

def pastep(base, on_path, siz, place_x = 0, place_y = 0, aspect = 1): #場所とサイズを指定して合成
    img = Image.open(on_path)
    w_i, h_i = (siz, int(siz*aspect))
    img_resized = img.resize((w_i, h_i))
    base.paste(img_resized, (place_x, place_y), img_resized)
    return base

def mask_mul(base, on_path): #ベース画像と載せたい画像のパスのpngを乗算

    logo = Image.open(on_path)

    # base.paste(logo, (0, 0))
    base = ImageChops.multiply(base, logo)
    return base

def mask_alpha(base, alpha, mask): #alphaに白黒画像、maskにクリッピングする画像を入れる
    a_img = Image.open(alpha).convert("RGBA")
    m_img = Image.open(mask).convert("RGBA")
    a_img = a_img.convert('L')
    a_img = ImageOps.invert(a_img)
    m_img.putalpha(a_img)
    base.paste(m_img, (0, 0), m_img)
    return base

def mask_lit(base, enh): #画像の明るさ変更
    enhancer = ImageEnhance.Brightness(base)
    base = enhancer.enhance(enh)
    return base


def crop_center(pil_img, crop_width, crop_height): #画像の中心をトリミングする際に用いた関数
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def card_p_test(path): #なぜか背景が黒くなるのでテスト
    n = 1 #くっつけた後のファイル名用
    DPI=400
    base = Image.new("RGB", (int(8.27*DPI), int(11.69*DPI)), (255, 255, 255))
    c_img = Image.open(path + "/1.png")
    k_pth = "../materials/flames/kiritori.png"
    paste(c_img, k_pth) #切り取り専用の黒枠(1mm幅)の設定
    base.paste(c_img, (0,0), c_img)
    base.save(path + "/combined_" + str(n) +".png")


def card_print(path,num): #9枚ごとの画像を作る
    p = 0 #ファイルの位置はこれに従う
    n = 1 #くっつけた後のファイル名用
    DPI = 400
    x = 32
    c_img = Image.open(path + "/1.png")
    w, h = c_img.size
    w = w - x
    h = h - x
    base = Image.new("RGB", (int(8.27*DPI), int(11.69*DPI)), (255, 255, 255))
    w_b, h_b = base.size
    for i in range(num):
        c_img = Image.open(path + "/"+str(i+1)+".png")
        k_pth = "../materials/flames/kiritori.png"
        paste(c_img, k_pth) #切り取り専用の黒枠(1mm幅)の設定
        X = (w_b - 3*w) // 2
        Y = (h_b - 3*h) // 2 #中央に配置するようにしたほうがいいならします←しました
        base.paste(c_img, (X + (p//3)*w, Y + (p%3)*h), c_img)
        p += 1
        if p == 9 or i == num - 1:
            base.save(path + "/combined_" + str(n) +".png")
            print("combined card {} to {}".format(n*9-8, n*9))
            n += 1
            p = 0
            base = Image.new("RGB", (int(8.27*DPI), int(11.69*DPI)), (255, 255, 255))

class Card():

    def __init__(self, ID, df):
        #以下、変数（調整可能）___________
        NUM_WORLD_CARD = 109
        NUM_MIRACLE_CARD = 23
        #_______________________________
        self.CardNo = df.at[ID, "Num_ID"]
        self.CardID = int(df.at[ID, "CardID"])
        self.name = df.at[ID, "name"]
        if pd.isna(self.name):
            self.name = " "
        self.card_class = df.at[ID, "class"]
        self.ctype1 = df.at[ID, "ctype1"]
        if pd.isna(self.ctype1) == False:
            #self.flame_path = "../materials/flames/flame_" + self.ctype1 + ".png"
            self.flame_path = "../materials/flame_c/flame_" + self.ctype1 + ".png"
        else:
            self.flame_path = "../materials/flames/flame_" + self.card_class + ".png" #神話と奇跡の枠

        self.ctype2 = df.at[ID, "ctype2"]
        if self.card_class == "world" or self.card_class == "tree":
            if pd.isna(self.ctype2) == False:
                #self.flame2_path = "../materials/flames/flame_half_" + self.ctype2 + ".png"
                self.flame2_path = "../materials/flame_c/flame_half_" + self.ctype2 + ".png"
                self.flame2i_path = "../materials/cost/f2_1_" + self.ctype2 + ".png"
                self.flame1i_path = "../materials/cost/f2_2_" + self.ctype1 + ".png"
            else:
                self.flame1i_path = "../materials/cost/f1_" + self.ctype1 + ".png"
        
        self.type1 = df.at[ID, "type1"]
        if pd.isna(self.type1):
            self.type1_path = "../materials/cost/down_null.png"
        else:
            self.type1_path = "../materials/cost/down_" + self.type1 + ".png"
            self.cost1 = int(df.at[ID, "cost1"])
            self.cost1_path = "../materials/cost/down_" + str(self.cost1) + ".png"
        if self.card_class == "miracle":
            self.cost1 = int(df.at[ID, "cost1"])

        self.type2 = df.at[ID, "type2"]
        if pd.isna(self.type2):
            self.type2_path = "../materials/cost/mid_null.png"
        else:
            self.type2_path = "../materials/cost/mid_" + self.type2 + ".png"
            self.cost2 = int(df.at[ID, "cost2"])
            self.cost2_path = "../materials/cost/mid_" + str(self.cost2) + ".png"

        self.type3 = df.at[ID, "type3"]
        if pd.isna(self.type3):
            self.type3_path = "../materials/cost/up_null.png"
        else:
            self.type3_path = "../materials/cost/up_" + self.type3 + ".png"
            self.cost3 = int(df.at[ID, "cost3"])
            self.cost3_path = "../materials/cost/up_" + str(self.cost3) + ".png"

        card_img_paths=[]
        if self.card_class == "world": #世界カード
            card_img_paths = glob.glob("../materials/pictures/"+ str(int(str(self.CardID)[1:])) + "_*")
        elif self.card_class == "miracle":
            card_img_paths = glob.glob("../materials/pictures/E"+ str(int(str(self.CardID)[1:])) + "_*")
        elif self.card_class == "mytho":
            card_img_paths = glob.glob("../materials/icons/mytho_icons/0" + str(self.CardNo)[1:]+".png")

        if len(card_img_paths) != 0:
            self.card_fig_path = card_img_paths[0]
        else:
            self.card_fig_path = "../materials/pictures/null.png"
        self.text = df.at[ID, "text"]
        self.text2 = df.at[ID, "text_2"]
        self.cardtype = df.at[ID, "kouka1"]
        self.cardtype2 = df.at[ID, "kouka2"]
        if self.card_class == "world" or self.card_class == "tree":
            self.cardtype_path = "../materials/flame_c/kouka_" + self.cardtype + ".png"
            if pd.isna(self.cardtype2) == False:
                self.cardtype2_path = "../materials/flame_c/kouka_half_" + self.cardtype2 + ".png"
        self.opt1 = df.at[ID, "opt1"]
        self.opt2 = df.at[ID, "opt2"]

    def plot_img(self): #base
        paste_list = []
        mask_list = [] #乗算レイヤーのマスク用
        if self.card_class == "world":
            base = Image.open("../materials/flames/base.png")
            base = self.plot_picture(base)
            base = paste(base, self.cardtype_path)
            if pd.isna(self.cardtype2) == False:
                base = paste(base, self.cardtype2_path)
            #base = paste(base, "../materials/flames/base.png")
            base = paste(base, self.flame_path)
            #base = mask_alpha(base,"../materials/flames/flame_mask.png",self.flame_path)
            #if self.ctype1 != "none" and self.ctype1 != "all":
            #    base = paste(base, self.flame1i_path)
            if pd.isna(self.ctype2) == False:
                base = paste(base, self.flame2_path)
                #base = mask_alpha(base,"../materials/flames/flame_half_mask.png",self.flame2_path)
                base = paste(base, self.flame2i_path)
                base = paste(base, self.flame1i_path)
            else:
                base = paste(base, self.flame1i_path) #重なった部分が隠れてしまう問題を修正
            #base = paste(base, "../materials/flames/flame_effect.png")
            base = paste(base, self.type1_path)
            base = paste(base, self.cost1_path)
            base = paste(base, self.type2_path)
            if pd.isna(self.type2) == False:
                base = paste(base, self.cost2_path)
            base = paste(base, self.type3_path)
            if pd.isna(self.type3) == False:
                base = paste(base, self.cost3_path)
            if pd.isna(self.opt1) == False:
                plsx = 150
                base = pastep(base, "../materials/icons/"+ self.cardtype + "_" + self.opt1 + ".png", 160, 115, 1080-plsx)
                if self.cardtype == "rinsetu":
                    #base = pastep(base, "../materials/icons/wbeside_2.png", 100, 205, 1180-plsx)
                    base = pastep(base, "../materials/icons/wbeside_ic.png", 100, 820, 230)
                if self.cardtype == "spirit":
                    #base = pastep(base, "../materials/icons/spirit.png", 100, 205, 1180-plsx)
                    base = pastep(base, "../materials/icons/spirit_ic.png", 100, 815, 230)
            if pd.isna(self.opt2) == False:
                base = pastep(base, "../materials/icons/"+ self.cardtype2 + "_" + self.opt2 + ".png", 160, 115, 1080)
                if self.cardtype2 == "rinsetu":
                    #base = pastep(base, "../materials/icons/wbeside_2.png", 100, 205, 1180)
                    base = pastep(base, "../materials/icons/wbeside_ic.png", 100, 820, 230)
                if self.cardtype2 == "spirit":
                    #base = pastep(base, "../materials/icons/spirit.png", 100, 205, 1180)
                    base = pastep(base, "../materials/icons/spirit_ic.png", 100, 815, 230)
            #if pd.isna(self.ctype2) == False:
            #    base = mask_mul(base, "../materials/flames/eff_world_40_2.png")
            #else:
            base = mask_mul(base, "../materials/flames/eff_world_40.png")
            base = mask_lit(base, 1.2)
            
        elif self.card_class == "miracle":
            base = Image.open("../materials/flames/flame_miracle.png")
            base = self.plot_picture(base)
            base = paste(base, "../materials/flames/flame_miracle.png")
            base = paste(base, "../materials/flames/flame_effect.png")
            base = paste(base, "../materials/cost/vp_"+str(self.cost1)+".png")
            
        elif self.card_class == "tree": #世界樹の周りのカード（画像以外を簡易的に作成）
            base = Image.open("../materials/flames/base.png")
            # base = paste(base, self.cardtype_path)
            #base = mask_alpha(base,"../materials/flames/flame_tree_mask.png",self.flame_path)
            base = paste(base, "../materials/flames/tree_" + self.ctype1 + ".png")
            base = paste(base, self.flame1i_path)
            base = mask_mul(base, "../materials/flames/eff_tree_40.png")
            base = mask_lit(base, 1.2)
        # if self.card_class == "world":
        #     base = Image.open("../materials/flames/base.png")
        #     base = self.plot_picture(base)
        #     base = paste(base, self.cardtype_path)
        #     if pd.isna(self.cardtype2) == False:
        #         base = paste(base, self.cardtype2_path)
        #     base = paste(base, "../materials/flames/base.png")
        #     base = paste(base, self.flame_path)
        #     if self.ctype1 != "none" and self.ctype1 != "all":
        #         base = paste(base, self.flame1i_path)
        #     if pd.isna(self.ctype2) == False:
        #         base = paste(base, self.flame2_path)
        #         base = paste(base, self.flame2i_path)
        #     base = paste(base, "../materials/flames/flame_effect.png")
        #     base = paste(base, self.type1_path)
        #     base = paste(base, self.cost1_path)
        #     base = paste(base, self.type2_path)
        #     if pd.isna(self.type2) == False:
        #         base = paste(base, self.cost2_path)
        #     base = paste(base, self.type3_path)
        #     if pd.isna(self.type3) == False:
        #         base = paste(base, self.cost3_path)
        #     mask_list.append("../materials/flames/eff_world_40.png")
        # elif self.card_class == "miracle":
        #     base = Image.open("../materials/flames/flame_miracle.png")
        #     base = self.plot_picture(base)
        #     base = paste(base, "../materials/flames/flame_miracle.png")
        #     base = paste(base, "../materials/flames/flame_effect.png")
        #     base = paste(base, "../materials/cost/vp_"+str(self.cost1)+".png")

        elif self.card_class == "mytho":
            base = Image.open("../materials/flames/flame_mytho.png")
            base = pastep(base, self.card_fig_path , 280, 520, 600)
            base = pastep(base, "../materials/icons/mytho_icons/col.png" , 280, 735, 600)
            base = pastep(base, "../materials/icons/mytho_icons/point_" + str(int(self.opt1)) + ".png" , 280, 950, 600)
        for i in paste_list:
            base = paste(base, i)
        for i in mask_list:
            base = mask_mul(base, i)
        #base = mask_lit(base, 1.2)
        return base
    
    def plot_txt(self, base): #baseにはplot_imgで作成した画像が入る

        #以下、変数（調整可能）___________
        iconcor = [["VP", "vp"], ["精霊", "spirit"], ["プレイ時","play_2"], ["配置", "put"], ["1枚捨てる", "disc"], ["1枚引く", "draw"], ["永続", "ever_2"], ["n枚引く", "mdraw"], ["n枚捨てる", "mdisc"], ["移動", "mv"], ["浸透", "penet"], ["再配置", "reput"], ["VP", "vp"], ["隣接", "wbeside_2"], ["精霊（出）", "woutmv"], ["精霊（入）", "winmv"], ["浸透時", "wpenet"], ["配置時", "wput"]] #キーワード能力とアイコンの対応
        iconhalf = []
        #iconhalf = ["VP"] #アイコンのうち半分のサイズにするもの
        if self.card_class == "world" or self.card_class == "tree": #世界カードにおける設定
            icon_size = 65 #アイコンのサイズ
            half_icon_size = 55
            Y1 = 850 #縦方向の位置指定
            n_x = 120 #文字の右の余白
            n_x_2 = 360 #文字の左の余白（精霊や隣接の時）
            fontsize = 50
            space = 20 #行間
            space_x_t = 5 #文字間を詰める場合のpixel数
            space_x_i = 0 #アイコンにおける文字詰め
            space_x_hi = 0 #ハーフアイコンにおける文字詰め
            space_y = -15#アイコンが文字に対して相対的にずれてしまうのでその補正用
        elif self.card_class == "miracle":
            icon_size = 60 #アイコンのサイズ
            half_icon_size = 60
            Y1 = 720
            n_x = 120 #文字の左右の余白
            X = n_x
            fontsize = 60 #フォントサイズ
            space = 20 #行間
            space_x_t = 7 #文字間を詰める場合のpixel数
        elif self.card_class == "mytho":
            icon_size = 80 #アイコンのサイズ
            half_icon_size = 75
            Y1 = 290
            n_x = 190 #文字の左右の余白
            X = n_x
            fontsize = 80 #フォントサイズ
            space = 20 #行間
            space_x_t = 7 #文字間を詰める場合のpixel数
            space_x_i = 0 #アイコンにおける文字詰め
            space_x_hi = 0 #ハーフアイコンにおける文字詰め
            space_y = int(-icon_size*20/80) #アイコンが文字に対して相対的にずれてしまうのでその補正用
        Y2 = Y1+(icon_size+space)*2+20 #2段落に分けることになったので．
        #______________________________

        txt = list(self.text)
        for i in range(2):
            if i == 0:
                txt = list(self.text)
                Y = Y1
            else:
                if pd.isna(self.text2):
                    break
                txt = list(self.text2)
                Y = Y2
            flag = 0
            flag_b = 0
            txt_ = []
            icon_list = []
            icontxt_tmp =[]
            for t in txt:
                if t == "＞": #アイコン部分の終了処理
                    icontxt = ''.join(icontxt_tmp)
                    f2 = 0
                    for ic_ in range(len(iconcor)):
                        if iconcor[ic_][0] == icontxt:
                            f2 = 1
                            icon_list.append(iconcor[ic_][1])
                    
                    if f2 == 0:
                        print("error:No icons in list")
                    icontxt_tmp = []
                    flag = 0
                    for ic_ in iconhalf:
                        if icontxt == ic_:
                            txt_.append("◇") #サイズを半分にするアイコンを◇で代用
                            flag_b = 1
                    if flag_b == 1:
                        flag_b = 0
                    else:
                        txt_.append("◆") #アイコンが入る部分は◆で表す

                elif flag == 1: #アイコン部分の中身の読み取り処理
                    icontxt_tmp.append(t)
                elif t == "＜": #アイコン部分の開始（フラグを立てる）
                    flag = 1
                else: #平文
                    txt_.append(t)
            w, h = base.size
            if self.card_class == "world":
                if i == 0 and self.cardtype == "usual":
                    X = n_x
                else:
                    X = n_x_2
            else:
                X = n_x
            X_2 = w - n_x
            draw = ImageDraw.Draw(base)
            font = ImageFont.truetype('C:/Users/eag1e/AppData/Local/Microsoft/Windows/Fonts/KleeOne-SemiBold.ttf', fontsize)
            #font = ImageFont.truetype('C:/Users/eag1e/AppData/Local/Microsoft/Windows/Fonts/Mushin.ttf', fontsize)
            # draw.text((X, Y), '◆カードを1枚捨てた場合、\n捨てたカードと同じ属性を含む\nカード1枚に◆x3', '#FFFFFF',spacing=space, font=font, anchor='ma')
            point_x = X
            point_y = Y
            img_i = 0
            tmp_t = ""
            for t in txt_:
                px_1, py_1, px_2, py_2 = draw.textbbox((point_x,point_y), t, font = font, anchor = "la")
                if point_x == X: #左端の場合は字詰めの分ずれるので別に処理
                    if t == "◆":
                        px_2 = point_x + icon_size
                    if t == "◇":
                        px_2 = point_x + half_icon_size
                else: #アイコンの前後の字詰めの処理
                    if t == "◆":
                        px_2 = point_x + space_x_t - space_x_i + icon_size
                        py_1 = point_y + space_x_t - space_x_i + icon_size
                    if t == "◇":
                        px_2 = point_x + space_x_t - space_x_hi + half_icon_size
                        py_1 = point_y + space_x_t - space_x_hi - half_icon_size
                
                if px_2 > X_2 or t == "□": #右端に到達するか改行記号（□）がある
                    if t != "．"and t != "，" and t != "◇" and t != "）": #段落下げ
                        point_x = X
                        px_2 = X+(px_2-px_1)
                        point_y = point_y + icon_size + space
                if t == "◆": #アイコンの描画処理
                    img_pass = "../materials/icons/" + icon_list[img_i] + ".png"
                    img_i += 1
                    img = Image.open(img_pass)
                    w_i, h_i = (icon_size, icon_size)
                    img_resized = img.resize((w_i, h_i))
                    if point_x == X:
                        base.paste(img_resized, (point_x, point_y-icon_size+fontsize-space_y), img_resized)
                    else:
                        point_x += space_x_t - space_x_i
                        base.paste(img_resized, (point_x, point_y-icon_size+fontsize-space_y), img_resized)
                    point_x += icon_size - space_x_i
                elif t == "◇": #ハーフサイズアイコンの描画処理
                    img_pass = "../materials/icons/" + icon_list[img_i] + ".png"
                    img_i += 1
                    img = Image.open(img_pass)
                    w_i, h_i = (half_icon_size, half_icon_size)
                    img_resized = img.resize((w_i, h_i))
                    if point_x == X:
                        base.paste(img_resized, (point_x, point_y-half_icon_size+fontsize-space_y), img_resized)
                    else:
                        point_x += space_x_t - space_x_hi
                        base.paste(img_resized, (point_x, point_y-half_icon_size+fontsize-space_y), img_resized)
                    point_x += half_icon_size - space_x_hi
                elif t == "｝": #太字の描画処理（フォントを変更する）
                    font = ImageFont.truetype('C:/Users/eag1e/AppData/Local/Microsoft/Windows/Fonts/KleeOne-SemiBold.ttf', fontsize)
                    point_y += -15
                elif t == "｛": #太字の描画処理（フォントを変更する）
                    font = ImageFont.truetype('C:/Users/eag1e/AppData/Local/Microsoft/Windows/Fonts/Mamelon-5-Hi-Regular.ttf', fontsize)
                    point_y += 15
                elif t != "□": #それ以外の文字の描画処理
                    draw.text((point_x,point_y), t, '#000000', font = font, anchor = "la")
                    point_x = px_2 - space_x_t
    
        return base

    def plot_title(self, base):
        #以下、変数（調整可能）___________
        if self.card_class != "mytho":
            X= 595 #横方向の位置指定（中央）
            Y= 94 #縦方向の位置指定（上）
            fontsize_max = 65 #フォントサイズ
            wide_max = 640
            fontsize_ruby = 25 #ルビのサイズ
            space_ruby = 0
            fontsize_no = 35 #カード番号のフォントサイズ
            no_x = 815 #カード番号を書くときのx座標
            no_y = 160
            col_t = "#342d00"
        else:
            X= 693 #横方向の位置指定（中央）
            Y= 170 #縦方向の位置指定（上）
            fontsize_max = 120 #フォントサイズ
            wide_max = 900
            fontsize_ruby = 45 #ルビのサイズ
            space_ruby = 5
            fontsize_no = 40 #カード番号のフォントサイズ
            no_x = 1120 #カード番号を書くときのx座標
            no_y = 240
            col_t = "#093d0b"
        #fonturl, spacex_t, pitch_y = 'C:/Users/eag1e/AppData/Local/Microsoft/Windows/Fonts/KleeOne-SemiBold.ttf', 10, 0
        fonturl, spacex_t, pitch_y = 'C:/Users/eag1e/AppData/Local/Microsoft/Windows/Fonts/Mamelon-5-Hi-Regular.ttf', 9, 20
        #fonturl, spacex_t, pitch_y = 'C:/Users/eag1e/AppData/Local/Microsoft/Windows/Fonts/Makinas-4-Flat.ttf', 12, 20
        #fonturl, spacex_t, pitch_y = 'C:/Users/eag1e/AppData/Local/Microsoft/Windows/Fonts/Kinkakuji-Normal.ttf', 10, 20
        #fonturl, spacex_t, pitch_y = 'C:/Users/eag1e/AppData/Local/Microsoft/Windows/Fonts/AkazukinPop.ttf', 8, 10
        #_______________________________

        txt_list = [] #ex.["イ"，"セ"，"リ"，"ウ"，"ム"，"の"，"【"，"光"，"芒"，"】"]
        txt_tmp = [] #ex.["イ"，"セ"，"リ"，"ウ"，"ム"，"の"，"光"，"芒"]
        hur_yomi = [] #ex.こうぼう
        #hur_kanji = [] #ex.光芒
        hur_yomi_tmp = []
        #hur_kanji_tmp = []
        flag = 0
        for t in self.name: #ex.イセリウムの【光芒（こうぼう）】
            if flag == 2:
                if t == "）": #読みの終了処理
                    hur_yomi.append(''.join(hur_yomi_tmp))
                    hur_yomi_tmp = []
                    flag = 0
                else:
                    hur_yomi_tmp.append(t)

            elif flag == 1: #【】の中の漢字部分
                if t == "（": #読みの開始処理
                    flag = 2
                    #hur_kanji.append(''.join(hur_kanji_tmp)) #読ませたい漢字のリストに入れる
                    #hur_kanji_tmp = []
                else: 
                    #hur_kanji_tmp.append(t)
                    txt_list.append(t)
                    txt_tmp.append(t)
            elif t == "【": #フリガナ部分の開始処理
                txt_list.append(t)
                flag = 1
            elif t == "】": #平文と「】」
                txt_list.append(t)
            else:
                txt_list.append(t)
                txt_tmp.append(t)

        i = 50
        txt_len = len(txt_tmp)
        wide_max += (txt_len - 1) * spacex_t
        Y += pitch_y
        txt_ = ''.join(txt_tmp) #ex.イセリウムの光芒
        draw = ImageDraw.Draw(base)
        while draw.textbbox((X,Y), txt_, font = ImageFont.truetype(fonturl, i), anchor = "mm")[2] - draw.textbbox((X,Y), txt_, font = ImageFont.truetype(fonturl, i), anchor = "mm")[0]< wide_max and i < fontsize_max: i += 2
        point_x = draw.textbbox((X,Y), txt_, font = ImageFont.truetype(fonturl, i), anchor = "mm")[0] + ((txt_len - 1) * spacex_t) // 2
        point_y = draw.textbbox((X,Y), txt_, font = ImageFont.truetype(fonturl, i), anchor = "mm")[1] 
        font = ImageFont.truetype(fonturl, i-2)
        ruby_num = 0
        for t in txt_list:
            px_1, py_1, px_2, py_2 = draw.textbbox((point_x,point_y), t, font = font, anchor = "la")
            if t == "【" :
                ruby_x_1 = px_1
            elif t == "】":
                ruby_x_2 = px_1 + spacex_t
                yomi = " " + hur_yomi[ruby_num] + " "
                y_len = len(yomi)
                ruby_x = [ruby_x_1 + (ruby_x_2 - ruby_x_1)*i/(y_len-1) for i in range(y_len)]
                for i in range(y_len):
                    r = yomi[i]
                    draw.text((ruby_x[i],py_1-space_ruby), r, col_t, font = ImageFont.truetype(fonturl, fontsize_ruby), anchor = "ms")
                ruby_num += 1
            else:
                draw.text((point_x,point_y), t, col_t, font = font, anchor = "la")
                point_x = px_2 - spacex_t
        #draw.text((no_x,no_y), "No." + str(self.CardID), col_t, font = ImageFont.truetype(fonturl, fontsize_no), anchor = "la")
        fonturl = 'C:/Users/eag1e/AppData/Local/Microsoft/Windows/Fonts/Kinkakuji-Normal.ttf'
        draw.text((no_x,no_y), str(self.CardNo), col_t, font = ImageFont.truetype(fonturl, fontsize_no), anchor = "la")

        if self.card_class == "mytho":
            base = base.rotate(90, expand=True)
        return base
    
    def plot_picture(self, base):
        #以下、変数（調整可能）___________
        #X= 63 #横方向の位置指定（左上）
        #Y= 229 #縦方向の位置指定（左上）
        X = 68
        Y = 176+503-485
        PX = 855 #写真の横幅
        PY = 485 #写真の縦幅
        #_______________________________
        pict = Image.open(self.card_fig_path).convert("RGBA")
        w, h = pict.size
        
        if w / h < PX / PY: #画像が縦長（hが大きい）場合
            magn =  PX / w
        else:
            magn = PY / h
        pict_r = pict.resize((int(w*magn+1),int(h*magn+1))) #端数が余らずだとめんどくさいので。
        pict_paste = crop_center(pict_r, PX, PY)
        im_a = Image.open('../materials/icons/alpha_figure_n.png')
        im_a = im_a.convert('L').resize(pict_paste.size)
        im_a = ImageOps.invert(im_a)
        pict_paste.putalpha(im_a)
        base.paste(pict_paste, (X, Y), pict_paste)
        return base