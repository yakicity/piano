import numpy as np

whiteTilePosX = {
    "mac":np.array([
         17,   54,   91,  128,  165,  202,  239,  276,  313,  350,  387,
        424,  461,  498,  535,  572,  609,  646,  683,  720,  757,  794,
        831,  868,  905,  942,  978, 1015, 1052, 1089, 1126, 1163, 1200,
       1237, 1274, 1311, 1348, 1385, 1422, 1459, 1496, 1533, 1570, 1607,
       1644, 1681, 1718, 1755, 1792, 1829, 1866, 1903]),
    "windows":np.array([
          0,   25,   49,   74,   99,  123,  148,  173,  197,  222,  247,
        271,  296,  321,  345,  370,  395,  419,  444,  469,  493,  518,
        543,  567,  592,  617,  641,  665,  690,  715,  739,  764,  789,
        813,  838,  863,  887,  912,  937,  961,  986, 1011, 1035, 1060,
       1085, 1109, 1134, 1159, 1183, 1208, 1233, 1257]),
    "external":np.array([
          0,   25,   49,   74,   99,  123,  148,  173,  197,  222,  247,
        271,  296,  321,  345,  370,  395,  419,  444,  469,  493,  518,
        543,  567,  592,  617,  641,  665,  690,  715,  739,  764,  789,
        813,  838,  863,  887,  912,  937,  961,  986, 1011, 1035, 1060,
       1085, 1109, 1134, 1159, 1183, 1208, 1233, 1257])
}

blackTilePosX = {
    "mac":np.array([
         42,  105,  152,  216,  257,  300,  364,  410,  475,  516,  558,
        623,  668,  733,  774,  816,  881,  928,  991, 1033, 1075, 1139,
       1185, 1250, 1291, 1334, 1399, 1443, 1508, 1549, 1592, 1657, 1702,
       1766, 1808, 1849]),
    "windows":np.array([
         18,   60,   91,  134,  161,  190,  232,  263,  306,  334,  362,
        405,  435,  478,  506,  534,  577,  608,  650,  678,  706,  749,
        780,  823,  850,  879,  922,  952,  995, 1022, 1051, 1094, 1124,
       1167, 1195, 1222]),
    "external":np.array([
         18,   60,   91,  134,  161,  190,  232,  263,  306,  334,  362,
        405,  435,  478,  506,  534,  577,  608,  650,  678,  706,  749,
        780,  823,  850,  879,  922,  952,  995, 1022, 1051, 1094, 1124,
       1167, 1195, 1222])
}

whiteTileWidth = {"mac":33,"windows":23,"external":23}
blackTileWidth = {"mac":25,"windows":17,"external":17}



whiteTileAtHandHeight = {"mac":160,"windows":100,"external":100}
blackTileAtHandHeight = {"mac":100,"windows":60,"external":60}


dy = 8

class Tile():
    def __init__(self,posXIndex,long=1,ypos=0,right=False,camera="mac") -> None:
        if posXIndex < 52:
            self.pos = [whiteTilePosX[camera][posXIndex],ypos]
            self.size = [whiteTileWidth[camera],long*dy]
            if right:
                # 右手白鍵
                self.tilecolor = (255,144,30)
            if not right:
                # 左手白鍵
                self.tilecolor = (180,105,255)
        else:
            self.pos = [blackTilePosX[camera][posXIndex-52],ypos]
            self.size = [blackTileWidth[camera],long*dy]
            if right:
                # 右手黒鍵
                self.tilecolor = (255,0,0)
            if not right:
                # 左手黒鍵
                self.tilecolor = (0,0,255)
        # self.pos = [xpos,0]
        self.long = 0
        # 自分は何番目のタイルか
        self.index = posXIndex

class TileAtHandPos(Tile):
    def __init__(self,posXIndex,ylimit,camera="mac") -> None:
        # ylimitとはピアノタイル一番下の位置。ylimit-long*dyなので、つまりそこから上にlong*dy伸ばす
        super().__init__(posXIndex,ypos=ylimit-whiteTileAtHandHeight[camera],camera=camera)
        # 白鍵
        if posXIndex < 52:
            self.size = [whiteTileWidth[camera], whiteTileAtHandHeight[camera]]
            self.tilecolor = (255,255,255)
        else:
            self.size = [blackTileWidth[camera], blackTileAtHandHeight[camera]]
            self.tilecolor = (0,0,0)
        # 鍵盤がたたかれているか
        self.touch = False
        # 鍵盤がたたかれるべきか
        self.answer = False





class TileManager:
    def __init__(self,ylimit,camera="mac") -> None:
        self.omitTileList = []
        self.omitWhiteTileSum = 0
        self.omitBlackTileSum = 0
        self.camera = camera
      # 下にある鍵盤のリスト
        self.tileAtHandPosList = [TileAtHandPos(posXIndex=i,ylimit=ylimit,camera=self.camera) for i in range(88) if i not in self.omitTileList]
        self.tilelist = []
        # 押すべきタイル（tileAtHandPosList）のインデックス
        self.tileAnswerActiveList = []
        # 押されるべきタイルのリストを作成し、それらが押されるまで
        self.tileMustPushedList = []



    def appendAllTile(self,frame,leftKeyPushDict,rightKeyPushDict):
        # ylimit:手元鍵盤のしたの位置

        if frame in leftKeyPushDict:
            for i in leftKeyPushDict[frame]:
                if i[1] not in self.omitTileList:
                    self.tilelist.append(Tile(posXIndex=i[1],long=i[0],ypos=0,right = False,camera=self.camera))
        if frame in rightKeyPushDict:
            for i in rightKeyPushDict[frame]:
                if i[1] not in self.omitTileList:
                    self.tilelist.append(Tile(posXIndex=i[1],long=i[0],ypos=0,right = True,camera=self.camera))

    def calcOmitIndex(self,tileIndex):
        if tileIndex < 52:
            omitIndex = tileIndex - self.omitWhiteTileSum
        else:
            omitIndex = tileIndex - self.omitWhiteTileSum - self.omitBlackTileSum
        return omitIndex

    def updateAllTile(self,ylimit):
        for i,tile in enumerate(self.tilelist):
            x,y = tile.pos
            w,h = tile.size

            # タイルがで始めてから移動する
            if(tile.pos[1] == 0 and tile.long < tile.size[1]):
                tile.long += dy
            else:

                # タイル先端が手元ピアノに到達した＝鍵盤をたたくタイミング
                if(tile.pos[1] +dy + tile.long > ylimit - whiteTileAtHandHeight[self.camera]):
                    index = self.calcOmitIndex(tile.index)
                    self.tileAtHandPosList[index].answer = True
                    # タイルを縮める
                    tile.long -= dy

                    # タイル最上部が手元ピアノの最上部に来た＝鍵盤を話すタイミング
                    if(tile.pos[1] +dy > ylimit - whiteTileAtHandHeight[self.camera]):
                        self.tileAtHandPosList[index].answer = False

                # タイル最上部が手元ピアノよりも下 ->消去
                if(tile.pos[1] + dy> ylimit):
                    # tile.tilecolor = (255,255,255)
                    self.tilelist.remove(tile)
                    continue

                # タイル先端を動かす
                tile.pos = [tile.pos[0],tile.pos[1] + dy]

    def updateTileMustPushedList(self):
        self.tileMustPushedList = [tileAtHandPos for tileAtHandPos in self.tileAtHandPosList if tileAtHandPos.answer == True]


    def isStop(self):
        if len(self.tileMustPushedList) == 0:
            return False
        for tile in self.tileMustPushedList:
            if tile.touch == False:
                return True
        return False

    def clearTileTouch(self):
        for tile in self.tileAtHandPosList:
            tile.touch = False