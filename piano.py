# 1920*1200の動画からキーの入力情報配列を出力

import cv2
import numpy as np

# ----------------------------------------------------------------------------------
# key配列の作成
class Keyboard():
    # どのキーなのかと、そのキーが左、右手どちらで押されているかを管理
    def __init__(self,pos,code) -> None:
        self.pos = np.array(pos)
        # 0は押されていない,1は押されている
        self.rightOn = 0
        self.leftOn = 0
        self.code = code

# とにかく動画を1920*1200にしよう
whiteKeycode = [
    # ドレミファソラシ
    "A0","B0","C1","D1","E1","F1","G1",
    "A1","B1","C2","D2","E2","F2","G2",
    "A2","B2","C3","D3","E3","F3","G3",
    "A3","B3","C4","D4","E4","F4","G4",
    "A4","B4","C5","D5","E5","F5","G5",
    "A5","B5","C6","D6","E6","F6","G6",
    "A6","B6","C7","D7","E7","F7","G7",
    "A7","B7","C8"
]

blackKeycode = [
    # ドレファソシ
    "A0#","C1#","D1#","F1#","G1#",
    "A1#","C2#","D2#","F2#","G2#",
    "A2#","C3#","D3#","F3#","G3#",
    "A3#","C4#","D4#","F4#","G4#",
    "A4#","C5#","D5#","F5#","G5#",
    "A5#","C6#","D6#","F6#","G6#",
    "A6#","C7#","D7#","F7#","G7#",
    "A7#"
]

white_search_pos_Xlist1 = np.arange(17, 978, 37)
white_search_pos_Xlist2 = np.arange(978,1940,37)
white_search_pos_Xlist = np.concatenate([white_search_pos_Xlist1, white_search_pos_Xlist2], 0)

black_search_pos_Xlist = np.array([
        # シ,ド,レ,ファ,ソ
         42,
        105,  152,  216,  257,  300,
        364,  410,  475,  516,  558,
        623,  668,  733,  774,  816,
        881,  928,  991, 1033, 1075,
       1139, 1185, 1250, 1291, 1334,
       1399, 1443, 1508, 1549, 1592,
       1657, 1702, 1766, 1808, 1849])

# md = 1
white_search_pos_Ylist = np.repeat([1100],len(white_search_pos_Xlist))
white_search_pos_list = np.stack([white_search_pos_Xlist, white_search_pos_Ylist], 1)

whiteKeyList = []
for i,key in enumerate(whiteKeycode):
    whiteKeyList.append(Keyboard(white_search_pos_list[i],key))

black_search_pos_Ylist = np.repeat([1000],len(black_search_pos_Xlist))
black_search_pos_list = np.stack([black_search_pos_Xlist, black_search_pos_Ylist], 1)
black_search_pos_list = np.sort(black_search_pos_list,axis=0)

blackKeyList = []
for i,key in enumerate(blackKeycode):
    blackKeyList.append(Keyboard(black_search_pos_list[i],key))

keyList = np.concatenate([whiteKeyList, blackKeyList], 0)
# ------------------------------------------------------------------------------------

leftKeyPushofFrame = [0] * 88
rightKeyPushofFrame = [0] * 88

# =====================================================================================
song = 'kieteshimaisoudesu'
# =====================================================================================
path = f'/Users/yusuke/data/{song}.mov'

# path = '/Users/yusuke/data/a.mov'
capture = cv2.VideoCapture(path)

#左手でONになるとき
left = [[7,12],
        [180,230],
        [130,250]]
#右手でONになるとき
right = [[112,120],
         [180,230],
         [130,250]]

font = cv2.FONT_HERSHEY_SIMPLEX
display_pos_of_y = 900

b = np.arange(0,36,1)
w = np.arange(0,52,1)

leftKeyPush = []
rightKeyPush = []

# # 動画サイズ取得
# width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
# #フレームレート取得
# fps = capture.get(cv2.CAP_PROP_FPS)

while True:
    # カメラ/動画の画像を1フレーム分取得
    ret, img = capture.read()
    if not ret:
        print("capture error!!")
        break
    # 特にmacで全画面で録画したものは、初めは2940*1912なので大きさを変更する必要あり
    img = cv2.resize(img, (1920, 1200))
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 右手、左手でキーが押されているかを毎フレームごとに管理する配列
    leftKeyPushofFrame = [0] * 88
    rightKeyPushofFrame = [0] * 88

    for i,key in enumerate(keyList):
        search_posx,search_posy = key.pos
        cv2.circle(img,center=(search_posx,search_posy),radius=0,color=(0,0,255),thickness=3)
        text = ''
        # 左手
        if(imghsv[search_posy,search_posx,0] >= left[0][0] and
           imghsv[search_posy,search_posx,0] <= left[0][1] and
           imghsv[search_posy,search_posx,1] >= left[1][0] and
           imghsv[search_posy,search_posx,1] <= left[1][1] and
           imghsv[search_posy,search_posx,2] >= left[2][0] and
           imghsv[search_posy,search_posx,2] <= left[2][1]):
            text = 'ON'
            key.leftOn = 1
            leftKeyPushofFrame[i] = 1
            # print(" left  ",imghsv[search_posy,search_posx,0],imghsv[search_posy,search_posx,1],imghsv[search_posy,search_posx,2])
        # 右手がおされている
        elif(imghsv[search_posy,search_posx,0] >= right[0][0] and
           imghsv[search_posy,search_posx,0] <= right[0][1] and
           imghsv[search_posy,search_posx,1] >= right[1][0] and
           imghsv[search_posy,search_posx,1] <= right[1][1] and
           imghsv[search_posy,search_posx,2] >= right[2][0] and
           imghsv[search_posy,search_posx,2] <= right[2][1]):
            text = 'ON'
            key.rightOn = 1
            rightKeyPushofFrame[i] = 1
            # print(" right  ",imghsv[search_posy,search_posx,0],imghsv[search_posy,search_posx,1],imghsv[search_posy,search_posx,2])
        # 白鍵も黒鍵もおされていない
        else:
            key.leftOn = 0
            # print(" none  ",imghsv[search_posy,search_posx,0],imghsv[search_posy,search_posx,1],imghsv[search_posy,search_posx,2])

        cv2.putText(img,text,(search_posx-20,display_pos_of_y),font,1,(0,255,0),4,cv2.LINE_AA) #フレームに表示

    leftKeyPush.append(leftKeyPushofFrame)
    rightKeyPush.append(rightKeyPushofFrame)

    cv2.putText(img,text,(search_posx-20,display_pos_of_y),font,1,(0,255,0),4,cv2.LINE_AA) #フレームに表示
    # カメラの映像を表示する
    cv2.imshow('camera', img)

    # qキーを押したら処理を終了する
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# いろいろ閉じる
capture.release()
cv2.waitKey(1)
cv2.destroyAllWindows()
cv2.waitKey(1)

# --------------------------------------------------------------------------------------

# 各フレームでどのキーが押されたか
leftKeyPush_np = np.array(leftKeyPush)
rightKeyPush_np = np.array(rightKeyPush)

# 各フレームで押されているキーのみをまとめてみた
leftKeyPushKeyPerFrame = [np.where(i == 1)[0].tolist()  for i in leftKeyPush_np]
rightKeyPushKeyPerFrame = [np.where(i == 1)[0].tolist()  for i in rightKeyPush_np]

# 各キーごと、いつ押されたか
leftKeyPushPerKey = leftKeyPush_np.T
rightKeyPushPerKey = rightKeyPush_np.T

# 各キーごと、押されたフレームのみをまとめた
leftKeyPushFramePerKey= [(np.where(i == 1))[0] for i in leftKeyPushPerKey]
rightKeyPushFramePerKey= [(np.where(i == 1))[0] for i in rightKeyPushPerKey]

# 各キーごと、連続で押されたフレームごと配列にする
leftContinuousKeyPushFramePerKey = []
for leftKeyPushFrame in leftKeyPushFramePerKey:
    leftContinuousKeyPushFrame = []
    if len(leftKeyPushFrame) == 0:
        leftContinuousKeyPushFramePerKey.append(leftContinuousKeyPushFrame)
        continue
    else:
        tmp = [leftKeyPushFrame[0]]
        for i in range(len(leftKeyPushFrame)-1):
            if leftKeyPushFrame[i+1] - leftKeyPushFrame[i] == 1:
                tmp.append(leftKeyPushFrame[i+1])
            else:
                if len(tmp) > 0:
                    leftContinuousKeyPushFrame.append(tmp)
                tmp = []
                tmp.append(leftKeyPushFrame[i+1])
        leftContinuousKeyPushFrame.append(tmp)
        leftContinuousKeyPushFramePerKey.append(leftContinuousKeyPushFrame)

rightContinuousKeyPushFramePerKey = []
for rightKeyPushFrame in rightKeyPushFramePerKey:
    rightContinuousKeyPushFrame = []
    if len(rightKeyPushFrame) == 0:
        rightContinuousKeyPushFramePerKey.append(rightContinuousKeyPushFrame)
        continue
    else:
        tmp = [rightKeyPushFrame[0]]
        for i in range(len(rightKeyPushFrame)-1):
            if rightKeyPushFrame[i+1] - rightKeyPushFrame[i] == 1:
                tmp.append(rightKeyPushFrame[i+1])
            else:
                if len(tmp) > 0:
                    rightContinuousKeyPushFrame.append(tmp)
                tmp = []
                tmp.append(rightKeyPushFrame[i+1])
        rightContinuousKeyPushFrame.append(tmp)
        rightContinuousKeyPushFramePerKey.append(rightContinuousKeyPushFrame)

# [何フレーム目から、何フレームの間連続で押された、どのキーが]の配列
leftContinuousKeyPush =  [[[i[0],len(i),keyIndex] for i in leftContinuousKeyPushFrame]for keyIndex,leftContinuousKeyPushFrame in enumerate(leftContinuousKeyPushFramePerKey) if len(leftContinuousKeyPushFrame) > 0]
rightContinuousKeyPush =  [[[i[0],len(i),keyIndex] for i in rightContinuousKeyPushFrame]for keyIndex,rightContinuousKeyPushFrame in enumerate(rightContinuousKeyPushFramePerKey) if len(rightContinuousKeyPushFrame) > 0]

# フレームが辞書のキー。4: [[8, 62], [8, 64]]　= 4フレーム目から８フレーク連続で62キーと64キーが押される
leftContinuousKeyPush_dict = {}
rightContinuousKeyPush_dict = {}

for i in leftContinuousKeyPush:
    for j in i:
        if j[0] in leftContinuousKeyPush_dict:
            leftContinuousKeyPush_dict[j[0]].append([j[1],j[2]])
        else:
            leftContinuousKeyPush_dict[j[0]] = [[j[1],j[2]]]

for i in rightContinuousKeyPush:
    for j in i:
        if j[0] in rightContinuousKeyPush_dict:
            rightContinuousKeyPush_dict[j[0]].append([j[1],j[2]])
        else:
            rightContinuousKeyPush_dict[j[0]] = [[j[1],j[2]]]

leftContinuousKeyPush_dict = dict(sorted(leftContinuousKeyPush_dict.items()))
rightContinuousKeyPush_dict = dict(sorted(rightContinuousKeyPush_dict.items()))

# with open(f'ar_{song}_left.txt', mode='w') as f:
#     f.write(str(leftContinuousKeyPush_dict))
# with open(f'ar_{song}_right.txt', mode='w') as f:
#     f.write(str(rightContinuousKeyPush_dict))
# with open(f'dl_{song}_left.txt', mode='w') as f:
#     f.write(str(leftKeyPushKeyPerFrame))
# with open(f'dl_{song}_right.txt', mode='w') as f:
#     f.write(str(rightKeyPushKeyPerFrame))

#  print(leftContinuousKeyPush_dict)

