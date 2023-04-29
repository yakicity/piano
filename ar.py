import cv2
import mediapipe as mp

import TileManager
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# 内蔵カメラから入力
cap = cv2.VideoCapture(0)
# 外付けカメラから入力
# cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

height = 720
cap.set(3,1280)
cap.set(4,height)
fps = cap.get(cv2.CAP_PROP_FPS)


# landmarkの繋がり表示用
landmark_line_ids = [4,8,12,16,20] #親、人、中、薬、子

ylimit = height - 100



def drawTile(img):
    for tile in tileManager.tilelist:
        x,y = tile.pos
        w,h = tile.size
        cv2.rectangle(img,tile.pos,(x+w, y + tile.long),tile.tilecolor,cv2.FILLED)
    return img

def drawTileAtHandPos(img):
    for i,tile in enumerate(tileManager.tileAtHandPosList):
        x,y = tile.pos
        w,h = tile.size

        if tile.touch:
            cv2.rectangle(img,tile.pos,(x+w, y+h),(0,255,0),cv2.FILLED)
        elif tile.answer:
            cv2.rectangle(img,tile.pos,(x+w, y+h),(111,172,64),cv2.FILLED)
        else:
            cv2.rectangle(img,tile.pos,(x+w, y+h),tile.tilecolor,cv2.FILLED)
    return img



maxcount = 10000
count = 0
frame = 0
level = 1


# key=フレーム
# 要素＝[何フレーム連続で,どこのキーが押されたか]のリスト
# キーは0-87で白鍵は0-51、黒鍵は52-87

leftpath = 'obenkyoshitoiteyo_short_left.txt'
rightpath = 'obenkyoshitoiteyo_short_right.txt'

with open(leftpath) as f:
    left = f.read()
import ast
leftKeyPushDict = ast.literal_eval(left)


with open(rightpath) as f:
    right = f.read()
import ast
rightKeyPushDict = ast.literal_eval(right)





tileManager = TileManager.TileManager(ylimit,False)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        if count > maxcount:
            break
        success, img = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        img_h, img_w, _ = img.shape     # サイズ取得
        print(img_h, img_w)
        img.flags.writeable = False
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img)
        # 検出された手の骨格をカメラ画像に重ねて描画
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


        tileManager.updateTileMustPushedList()

        # if(tileManager.isStop()):
        #     pass
        # else:
        #     if count % level == 0:
        #         frame = count / level
        #     else:
        #         count += 1
        #         continue
        #     oldTilelist = tileManager.tilelist
        #     tileManager.appendAllTile(frame,leftKeyPushDict,rightKeyPushDict)
        #     tileManager.updateAllTile(ylimit)

        if count % level == 0:
            frame = count / level
        else:
            count += 1
            continue
        oldTilelist = tileManager.tilelist
        tileManager.appendAllTile(frame,leftKeyPushDict,rightKeyPushDict)
        tileManager.updateAllTile(ylimit)

        img = drawTile(img)
        img = drawTileAtHandPos(img)

        # すべての押されている情報をクリア
        tileManager.clearTileTouch()

        # 手の位置をもとに押されている情報を更新
        if results.multi_hand_landmarks:
            # このfor一回目のループで右、二回目で左を回す
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                for tile in tileManager.tileMustPushedList:
                    x,y = tile.pos
                    w,h = tile.size
                    for line_id in landmark_line_ids:
                        lm = hand_landmarks.landmark[line_id]
                        lm_pos_x,lm_pos_y = int(lm.x * img_w), int(lm.y * img_h)
                        if x < lm_pos_x < x + w and y < lm_pos_y < y+h:
                            tile.touch = True

        cv2.imshow('MediaPipe Hands', img)
        if cv2.waitKey(1) == 13:
            break
        count += 1
cap.release()