import numpy as np

whiteTilePosX = {
    "normal":np.array([
          0,   25,   49,   74,   99,  123,  148,  
        173,  197,  222,  247,  271,  296,  321,
        345,  370,  395,  419,  444,  469,  493,  
        518,  543,  567,  592,  617,  641,  665,  
        690,  715,  739,  764,  789,  813,  838,
        863,  887,  912,  937,  961,  986, 1011,
       1035, 1060, 1085, 1109, 1134, 1159, 1183, 
       1208, 1233, 1257
    ]),
    "home":np.array([
         -1,   -1,    0,   26,   51,   77,  103,  128,  154,  180,  205,
        231,  257,  282,  308,  334,  359,  385,  411,  436,  462,  488,
        513,  539,  565,  590,  616,  642,  667,  692,  718,  744,  769,
        795,  821,  846,  872,  898,  923,  949,  975, 1000, 1026, 1052,
       1077, 1103, 1129, 1154, 1180, 1206, 1231, 1257])
}

blackTilePosX = {
    "normal":np.array([
         18,   60,   91,  134,  161,  190,  232,  263,  306,  334,  362,
        405,  435,  478,  506,  534,  577,  608,  650,  678,  706,  749,
        780,  823,  850,  879,  922,  952,  995, 1022, 1051, 1094, 1124,
       1167, 1195, 1222
    ]),
    "home":np.array([
         -1,   13,   45,   90,  118,  150,  183,  214,  257,  285,  313,
        356,  386,  429,  457,  485,  528,  559,  601,  629,  657,  700,
        731,  774,  801,  830,  873,  903,  946,  973, 1002, 1045, 1075,
       1118, 1146, 1173])
}

whiteTileWidth = {"normal":22,"home":23}
blackTileWidth = {"normal":17,"home":17}

dy = 8

whiteTileAtHandHeight = 100
blackTileAtHandHeight =  60

class Tile():
    def __init__(self,posXIndex,long=1,ypos=0,right=False,isHomeStr="home") -> None:
        if posXIndex < 52:
            self.pos = [whiteTilePosX[isHomeStr][posXIndex],ypos]
            self.size = [whiteTileWidth[isHomeStr],long*dy]
            if right:
                # 右手白鍵
                self.tilecolor = (255,144,30)
            if not right:
                # 左手白鍵
                self.tilecolor = (180,105,255)
        else:
            self.pos = [blackTilePosX[isHomeStr][posXIndex-52],ypos]
            self.size = [blackTileWidth[isHomeStr],long*dy]
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
    def __init__(self,posXIndex,ylimit,isHomeStr="home") -> None:
        # ylimitとはピアノタイル一番下の位置。ylimit-long*dyなので、つまりそこから上にlong*dy伸ばす
        super().__init__(posXIndex,ypos=ylimit-whiteTileAtHandHeight,isHomeStr=isHomeStr)
        # 白鍵
        if posXIndex < 52:
            self.size = [whiteTileWidth[isHomeStr], whiteTileAtHandHeight]
            self.tilecolor = (255,255,255)
        else:
            self.size = [blackTileWidth[isHomeStr], blackTileAtHandHeight]
            self.tilecolor = (0,0,0)
        # 鍵盤がたたかれているか
        self.touch = False
        # 鍵盤がたたかれるべきか
        self.answer = False





class TileManager:
    def __init__(self,ylimit,isHome=True) -> None:      
        if isHome:
            self.omitTileList = [0,1,52]
            self.omitWhiteTileSum = 2
            self.omitBlackTileSum = 1
            self.isHomeStr = "home"
        else:
            self.omitTileList = []
            self.omitWhiteTileSum = 0
            self.omitBlackTileSum = 0
            self.isHomeStr = "normal"
      # 下にある鍵盤のリスト
        self.tileAtHandPosList = [TileAtHandPos(posXIndex=i,ylimit=ylimit,isHomeStr=self.isHomeStr) for i in range(88) if i not in self.omitTileList]
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
                    self.tilelist.append(Tile(posXIndex=i[1],long=i[0],ypos=0,right = False,isHomeStr=self.isHomeStr))
        if frame in rightKeyPushDict:
            for i in rightKeyPushDict[frame]:
                if i[1] not in self.omitTileList:
                    self.tilelist.append(Tile(posXIndex=i[1],long=i[0],ypos=0,right = True,isHomeStr=self.isHomeStr))

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
                if(tile.pos[1] +dy + tile.long > ylimit - whiteTileAtHandHeight):
                    index = self.calcOmitIndex(tile.index)
                    self.tileAtHandPosList[index].answer = True
                    # タイルを縮める
                    tile.long -= dy  

                    # タイル最上部が手元ピアノの最上部に来た＝鍵盤を話すタイミング
                    if(tile.pos[1] +dy > ylimit - whiteTileAtHandHeight):
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