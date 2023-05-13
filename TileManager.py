import numpy as np

whiteTilePosX = {
    "mac":np.array([
          0,   37,   74,  111,  148,  185,  222,  259,  296,  333,  370,
        407,  444,  481,  518,  555,  592,  629,  666,  703,  740,  777,
        814,  851,  888,  925,  961,  998, 1035, 1072, 1109, 1146, 1183,
       1220, 1257, 1294, 1331, 1368, 1405, 1442, 1479, 1516, 1553, 1590,
       1627, 1664, 1701, 1738, 1775, 1812, 1849, 1886]),
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
       1085, 1109, 1134, 1159, 1183, 1208, 1233, 1257]),
    "home":np.array([
         -1,   -1,    0,   26,   51,   77,  103,  128,  154,  180,  205,
        231,  257,  282,  308,  334,  359,  385,  411,  436,  462,  488,
        513,  539,  565,  590,  616,  642,  667,  692,  718,  744,  769,
        795,  821,  846,  872,  898,  923,  949,  975, 1000, 1026, 1052,
       1077, 1103, 1129, 1154, 1180, 1206, 1231, 1257])
}

blackTilePosX = {
    "mac":np.array([
         22,   94,  135,  206,  244,  283,  354,  395,  465,  503,  544,
        609,  654,  719,  760,  802,  867,  914,  977, 1019, 1061, 1125,
       1171, 1236, 1277, 1320, 1385, 1429, 1494, 1535, 1578, 1643, 1688,
       1752, 1794, 1835]),
    "windows":np.array([
         18,   60,   91,  134,  161,  190,  232,  263,  306,  334,  362,
        405,  435,  478,  506,  534,  577,  608,  650,  678,  706,  749,
        780,  823,  850,  879,  922,  952,  995, 1022, 1051, 1094, 1124,
       1167, 1195, 1222]),
    "external":np.array([
         18,   60,   91,  134,  161,  190,  232,  263,  306,  334,  362,
        405,  435,  478,  506,  534,  577,  608,  650,  678,  706,  749,
        780,  823,  850,  879,  922,  952,  995, 1022, 1051, 1094, 1124,
       1167, 1195, 1222]),
    "home":np.array([
         -1,   13,   45,   90,  118,  150,  183,  214,  257,  285,  313,
        356,  386,  429,  457,  485,  528,  559,  601,  629,  657,  700,
        731,  774,  801,  830,  873,  903,  946,  973, 1002, 1045, 1075,
       1118, 1146, 1173])
}

whiteTileWidth = {"mac":33,"windows":23,"external":23,"home":33}
blackTileWidth = {"mac":25,"windows":17,"external":17,"home":25}



whiteTileAtHandHeight = {"mac":160,"windows":100,"external":100,"home":160}
blackTileAtHandHeight = {"mac":100,"windows":60,"external":60,"home":100}


dy = 5

class Tile():
    def __init__(self,posXIndex,continuous=1,ypos=0,right=False,camera="mac") -> None:
        if posXIndex < 52:
            self.pos = [whiteTilePosX[camera][posXIndex],ypos]
            self.size = [whiteTileWidth[camera],continuous*dy]
            if right:
                # 右手白鍵
                self.tilecolor = (255,144,30)
            if not right:
                # 左手白鍵
                self.tilecolor = (180,105,255)
        else:
            self.pos = [blackTilePosX[camera][posXIndex-52],ypos]
            self.size = [blackTileWidth[camera],continuous*dy]
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
        self.reachTileAtHanndPos = False

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
        if camera=='home':
            self.omitTileList = [0,1,52]
            self.omitWhiteTileSum = 2
            self.omitBlackTileSum = 1
            self.camera = "home"
        else:
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
                    self.tilelist.append(Tile(posXIndex=i[1],continuous=i[0],ypos=0,right = False,camera=self.camera))
        if frame in rightKeyPushDict:
            for i in rightKeyPushDict[frame]:
                if i[1] not in self.omitTileList:
                    self.tilelist.append(Tile(posXIndex=i[1],continuous=i[0],ypos=0,right = True,camera=self.camera))

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
                # タイル先端を動かす
                tile.pos = [tile.pos[0],tile.pos[1] + dy]

                # タイル先端が手元ピアノに到達した＝鍵盤をたたくタイミング
                if(tile.pos[1] + tile.long > ylimit - whiteTileAtHandHeight[self.camera]):
                    index = self.calcOmitIndex(tile.index)
                    self.tileAtHandPosList[index].answer = True
                    # タイルを縮める
                    tile.long -= dy

                    # タイル最上部が手元ピアノの最上部に来た＝鍵盤を話すタイミング
                    if(tile.pos[1] +dy > ylimit - whiteTileAtHandHeight[self.camera]):
                        self.tileAtHandPosList[index].answer = False

                if(tile.pos[1] + tile.long > ylimit):
                    tile.long -= dy

                # タイル最上部が手元ピアノよりも下 ->消去
                if(tile.pos[1] > ylimit):
                    # tile.tilecolor = (255,255,255)
                    self.tilelist.remove(tile)
                    continue



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