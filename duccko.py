import pyxel
import random
import math

class App:

    def __init__(self):
       pyxel.init(256, 128)
       self.reset()
       pyxel.run(self.update, self.draw)

    def reset(self):

        pyxel.load('kamo.pyxres')

        #self.duck(変数)にDuckクラスのインスタンスを代入
        self.duck = Duck()

        #Enemyクラスのインスタンス（３つ）をリストself.enemiesに代入、初期の座標を設定
        self.enemies = [Enemy(8,8), Enemy(240, 60), Enemy(128, 64)]

        #後々追加する敵SpecialEnemyクラスのインスタンスを変数self.specialenemyに代入
        self.specialenemy = SpecialEnemy()

        #ゲームオーバーフラッグははじめはfalse, trueになったらゲームオーバー画面を出す
        self.gameoverflag = False

        #ゲームクリアフラッグをfalseに設定、trueになったらゲーム終了
        self.clearflag = False

        #スコアは0に設定
        self.score = 0
        #クリアスコアをここで設定しておくことで、難易度調整がしやすくなる
        self.clearscore = 10
        #新しく追加するアイテムの座標を決めるときに使う変数に初めは適当な値を入れておく
        self.nx = 8
        self.ny = 8



    def update(self):
        #スペースキーでリスタートができるように設定
        if pyxel.btn(pyxel.KEY_SPACE):
                self.reset()
                self.duck.reset()
                self.specialenemy.reset()

        #ゲームオーバーの場合以下の更新をスキップする
        if self.gameoverflag:
            return
    
        #ゲームクリアの場合以下の更新をスキップする
        if self.clearflag:
            return

        self.duck.move()

        for enemy in self.enemies:
            #それぞれの敵の情報をアップデート
            enemy.update()

            #ゲームオーバーの条件
            #敵アイコンの中心とプレイヤーアイコンの中心の間の距離が、15（敵の視野の範囲よりやや狭め）未満の時、敵と味方の間に壁があるか調べ、
            #なかったらゲームオーバーになる（gameoverflagをtrueにする）
            if math.sqrt(((enemy.centerx)-(self.duck.centerx))*((enemy.centerx)-(self.duck.centerx)) + (enemy.centery-self.duck.centery)*(enemy.centery-self.duck.centery) )< 11.5:
                #プレイヤーの下に壁、敵の上に壁
                if pyxel.tilemap(0).pget(self.duck.x/8, self.duck.y/8+1) == (0, 1) and self.duck.y > enemy.y:
                    if pyxel.tilemap(0).pget(enemy.x/8, enemy.y/8-1) == (0, 1):
                        self.gameoverflag= False
                #プレイヤーの上に壁、敵の下に壁
                elif  pyxel.tilemap(0).pget(self.duck.x/8, self.duck.y/8-1) == (0, 1) and self.duck.y < enemy.y:
                    if pyxel.tilemap(0).pget(enemy.x/8, enemy.y/8+1) == (0, 1):
                        self.gameoverflag= False
                #プレイヤーの右に壁、敵の左に壁
                elif  pyxel.tilemap(0).pget(self.duck.x/8+1, self.duck.y/8) == (0, 1) and self.duck.x < enemy.x:
                    if pyxel.tilemap(0).pget(enemy.x/8-1, enemy.y/8) == (0, 1):
                        self.gameoverflag= False
                #プレイヤーの左に壁、敵の右に壁
                elif  pyxel.tilemap(0).pget(self.duck.x/8-1, self.duck.y/8) == (0, 1) and self.duck.x > enemy.x:
                    if pyxel.tilemap(0).pget(enemy.x/8+1, enemy.y/8) == (0, 1):
                        self.gameoverflag= False
                #間に壁がないとき
                else:
                    pyxel.play(0, 1)
                    self.gameoverflag= True

        if self.specialenemy.x <=self.duck.x +4 <= self.specialenemy.x +8  and  self.specialenemy.y <= self.duck.y <= self.specialenemy.y+ 4:
            self.gameoverflag = True
            pyxel.play(0, 1)


        #スコアが250点を超えたら、追加の敵と特定の座標に宝箱を出す
        if self.score >= self.clearscore:

            self.specialenemy.update()
            pyxel.tilemap(0).pset(13,1, (6, 2)) 
        if pyxel.tilemap(0).pget(self.duck.x/8, self.duck.y/8) == (6, 2):
            self.clearflag = True
            pyxel.play(0, 2)

        #敵を追加        
        if self.score >= len(self.enemies) *40 :
            self.enemies.append(Enemy(120, 64))

        #アイテムの座標と鴨の座標が一致したら10点加点して、その座標に背景タイルを配置→アイテムを画面上から削除
        self.nx = self.duck.x + random.randint(-80, 80)
        self.ny = self.duck.y + random.randint(-80, 80)
        if pyxel.tilemap(0).pget(self.duck.x/8, self.duck.y/8) == (2, 2):
            self.score += 10
            pyxel.play(0, 0)
            if  pyxel.tilemap(0).pget(self.nx/8, self.ny/8) != (0, 1) and pyxel.tilemap(0).pget(self.nx/8, self.ny/8) != (3, 2):
                pyxel.tilemap(0).pset(self.nx/8, self.ny/8, (2, 2)) 
        pyxel.tilemap(0).pset(self.duck.x/8,self.duck.y/8, (0, 2)) 


    def draw(self):
        #ゲームオーバーフラッグがTrueの時、画面の中心に"GAMEOVER!!""PRESS SPACE KEY TO RESTART!!"を表示
        if self.gameoverflag:
            pyxel.bltm(0, 0, 0, 256, 0, 256, 128, 11)
            pyxel.text(50, 64, "GAME OVER!!", 0)
            pyxel.text(20, 70, "PRESS SPACE KEY TO RESTART!!", 0)

        elif self.clearflag:
                pyxel.text(112, 64, "CLEAR!!", 0)

        #ゲームオーバーフラッグがFalseのままなら、敵、鴨、背景（アイテム、壁含む）、スコアを普通に描画
        else:
            pyxel.cls(7)
        
            #背景のタイルマップを表示
            pyxel.bltm(0, 0, 0, 0, 0, 256, 128, 0)
            #Duckクラスのdrawインスタンス呼び出し→鴨アイコンの描画
            self.duck.draw()
            #Enemyクラスのdrawインスタンス呼び出し→敵の描画
            for enemy in self.enemies:
                enemy.draw()
            #スコアが250を超えたら、追加の敵を描写（SpecialEnemyクラスのdrawインスタンス呼び出し）
            #その横に矢印とコメントも追加
            if self.score >= self.clearscore:
                pyxel.text(36, 8, "GET A TREASURE!", 0)
                pyxel.blt(96, 8, 0, 56, 16, 8, 8, 11)
                self.specialenemy.draw()
            #スコア表示
            pyxel.text(16,116,str(self.score), 0)
        
        

#鴨
class Duck:

    def __init__(self):
        self.reset()

    #リスタート時に設定をリセットするためのメソッド
    def reset(self):
        #鴨の初期設定
        #スタート地点右下
        #初期x座標
        self.x= 240
        #初期y座標
        self.y= 112
        #鴨が右向きか左向きかを記憶（1の時は左、0の時は右。初めは←向きなので1
        self.dir = 1
        #鴨の進むスピード（x軸、y軸それぞれ）
        self.vx = 2
        self.vy = 2
        #鴨アイコンの中心座標を記憶→敵の視野内にいる判定、敵と触れている判定に用いる
        self.centerx = self.x + 4
        self.centery = self.y + 4
        
    def move(self):
        #矢印キーの操作と壁判定
        if pyxel.btn(pyxel.KEY_RIGHT):#右矢印キーが押されているとき…
            self.dir = 0 #アイコンが右向きになる
            #ここでは、プレイヤーの進行方向の座標に壁タイルまたは土タイル（画面淵）がないときのみ、プレイヤーが動くように場合分けされている
            if pyxel.tilemap(0).pget(self.x /8 +0.6, self.y/8) != (0, 1) and pyxel.tilemap(0).pget(self.x/8+0.6 , self.y/8) != (3, 2): 
                self.x += self.vx #右に決められた速さで進む
        elif pyxel.btn(pyxel.KEY_LEFT): #左矢印キーが押されているとき…
            self.dir = 1 #アイコンが左向きになる
            if pyxel.tilemap(0).pget(self.x/8 - 0.6, self.y/8) != (0, 1) and pyxel.tilemap(0).pget(self.x/8-0.6, self.y/8) != (3, 2):
                self.x -= self.vx #左に決められた速さで進む
        elif pyxel.btn(pyxel.KEY_UP):#上矢印キーが押されているとき…
            if pyxel.tilemap(0).pget(self.x /8, self.y/8-0.6) != (0, 1) and pyxel.tilemap(0).pget(self.x/8, self.y/8-0.6) != (3, 2):
                self.y -= self.vy #上に決められた速さで進む
        elif pyxel.btn(pyxel.KEY_DOWN): #下矢印キーが押されているとき…
            if pyxel.tilemap(0).pget(self.x /8, self.y/8+0.6) != (0, 1) and pyxel.tilemap(0).pget(self.x /8, self.y/8+ 0.6) != (3, 2):
                self.y += self.vy #下に決められた速さで進む
        #鴨アイコンの中心の座標を更新
        self.centerx= self.x+ 4
        self.centery= self.y +4


        
    def draw(self):
        #鴨の描画
        #鴨が左に進んでいるとき、左向きの鴨を描画する
        if self.dir == 1:
            pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, 11)
        #鴨が右に進んでいるとき、右向きの鴨を描画する
        if self.dir == 0:
            pyxel.blt(self.x, self.y, 0, 8, 8, 8, 8, 11)




#敵
class Enemy:
    #引数x,yを追加することでApp()内で呼び出す際に、敵ごとの開始位置を設定できる
    def __init__(self, x, y):
        self.reset(x, y)

    #リスタート時に設定をリセットするためのメソッド
    def reset(self, x, y):
        #初期x座標
        self.x= x
        #初期y座標
        self.y= y
        #初めのx軸方向の速さをランダムに決定
        self.vx= random.randint(1, 2)
        #初めのy軸方向の速さをランダムに決定
        self.vy= random.randint(1, 2)
        #一定時間が過ぎたら速度を更新するために必要。時間間隔もランダムに決めることでより敵の動きが不規則になる
        self.time= random.randint(5, 10)
        #ランダムに進む向き（上下左右）を決定
        self.ran= random.randint(1, 4)
        #敵アイコンの中央の座標を記憶。App()内でプレイヤーが敵の視野内にいるかの判定、敵と触れているかの判定に用いる
        self.centerx= self.x+ 4
        self.centery= self.y +4

    def update(self):
        #移動パターンと壁判定の設定
        #ranが1かつ、進行方向に壁又は土タイルがない場合のみ敵は移動する
        if self.ran==1:#右に移動
            if pyxel.tilemap(0).pget(self.x /8 +0.5, self.y/8) != (0, 1) and pyxel.tilemap(0).pget(self.x /8 +0.5, self.y/8) != (3, 2): 
                self.x += self.vx
        elif self.ran==2:#左に移動
            if pyxel.tilemap(0).pget(self.x /8- 0.5, self.y/8) != (0, 1) and pyxel.tilemap(0).pget(self.x /8- 0.5, self.y/8) != (3, 2):
                self.x -= self.vx
        #上に進む
        elif self.ran==3 and pyxel.tilemap(0).pget(self.x /8, self.y/8-0.5) != (0, 1) and pyxel.tilemap(0).pget(self.x /8, self.y/8- 0.5) != (3, 2):
            self.y -= self.vy
        #下に進む
        elif self.ran==4 and pyxel.tilemap(0).pget(self.x /8, self.y/8+ 0.5) != (0, 1) and pyxel.tilemap(0).pget(self.x /8, self.y/8+ 0.5) != (3, 2):
            self.y += self.vy

        #updateが実行される度に、self.timeが1ずつ減る
        self.time -= 1  
        #self.time<0になる度にself.time, self.ran, self.vx, self.vyがランダムに決まる→時間経過とともに敵の移動速度と移動速度が更新される時間間隔が変化
        if self.time < 0:
            self.time= random.randint(5, 10)
            self.ran= random.randint(1, 4)
            self.vx= random.randint(1, 2)
            self.vy= random.randint(1, 2)
        #敵アイコンの中央の座標を更新
        self.centerx= self.x+ 4
        self.centery= self.y +4

            
    def draw(self):#self.x, self.yで記憶した座標に敵のアイコン（猫）を表示する
        #視野範囲→中が塗りつぶされてない円で可視化
        pyxel.circb(self.centerx, self.centery, 15, 7)
        #self.ranで記憶した敵の進む向きにあった敵アイコンを描画
        if self.ran!= 2:#敵が左に進むとき、敵アイコンは左向き
            pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, 11)
        elif self.ran!= 1:#敵が右に進むとき、敵アイコンは右向き
             pyxel.blt(self.x, self.y, 0, 16, 0, 8, 8, 11)


class SpecialEnemy:
    def __init__(self):
        self.reset()

    #リスタート時に設定をリセットするためのメソッド
    def reset(self):
        #初期x座標
        self.x = 72
        #初期y座標
        self.y = 24
        #移動方向（左右）はランダムに決定。0の時右向き、1の時左向き
        self.ran = random.randint(0, 1)
        #移動の速さもランダムに決定
        self.v = random.randint(1, 3)
        #移動方向と速さを時間経過とともに変化させるために必要
        self.time = random.randint(5, 10)

    def update(self):
        #self.ranで記憶してある値に応じでself.vに記憶してある速さをself.xから足すまたは引く
        #この敵は、y座標は固定してあり、特定のx座標の範囲内を移動する→特定の位置に配置してある宝箱を守るように動いている
        #self.xが128より小さい又は72の時のみ右に進む
        if self.ran == 0: 
            if self.x <= 128: 
                self.x += self.v
        #self.xが72より大きい又は72の時のみ左に進む
        if self.ran == 1:
            if self.x >= 72:
                self.x -= self.v

        #class Enemyと同様
        self.time -= 1
        if self.time < 0:
            self.ran = random.randint(0, 1)
            self.v = random.randint(1, 3)
            self.time = random.randint(5, 10)
        

    def draw(self): #self.x, self.yで記憶した座標に敵のアイコン（カラス）を表示する
        #self.ranに記憶してある進行方向に応じた方向を向いているカラスを描写
        if self.ran == 0: #右向き
            pyxel.blt(self.x, self.y, 0, 40, 16, 8, 8, 11)
        elif self.ran == 1: #左向き
            pyxel.blt(self.x, self.y, 0, 32, 16, 8, 8, 11)
             

App()