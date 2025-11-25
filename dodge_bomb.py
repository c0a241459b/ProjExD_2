import os
import sys
import random
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5), 
    pg.K_LEFT:(-5, 0), 
    pg.K_RIGHT:(+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    値：判定結果タプル（横方向、縦方向）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: #横方向のはみ出しチェック
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #横方向のはみ出しチェック
        tate = False
    return yoko, tate


def game_over(screen: pg.Surface) -> None:
    """
    引数：画面Surface
    値：None
    画面に「Game Over」の文字と「8.png」の画像を描画し、5秒後に終了する
    """
    game_over_surface = pg.Surface((WIDTH, HEIGHT)) #gameover Surfaceを作成し、背景色を黒に設定する
    game_over_surface.fill((0, 0, 0))

    game_over_rect = game_over_surface.get_rect() #gameover SurfaceのRectを作成し、中心を画面の中心に配置する
    game_over_rect.center = (WIDTH // 2, HEIGHT // 2)

    game_over_surface.set_alpha(200) #gameover Surfaceの透明度を設定する

    game_over_font = pg.font.Font(None, 60) # Game Overの文字を描画し、Surfaceに描画する
    game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
    game_over_text_rect = game_over_text.get_rect()
    game_over_text_rect.center = (WIDTH // 2, HEIGHT // 2)
    game_over_surface.blit(game_over_text, game_over_text_rect)

    kk_surface = pg.image.load("fig/8.png") # 8.pngを描画し、Surfaceに描画する
    kk_rect = kk_surface.get_rect()
    kk_rect.center = (WIDTH / 3 , HEIGHT / 2)
    game_over_surface.blit(kk_surface, kk_rect)

    kk_surface = pg.image.load("fig/8.png")
    kk_rect = kk_surface.get_rect()
    kk_rect.center = (WIDTH / 3 * 2, HEIGHT / 2)
    game_over_surface.blit(kk_surface, kk_rect)

    screen.blit(game_over_surface, [0, 0])  # gameover Surfaceを画面に描画する

    pg.display.update() # 5秒後に終了する
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数：なし
    値：tuple（爆弾画像のリスト、爆弾の半径のリスト）
    1から10までの半径のリストを作成し、各半径の円を描くSurfaceを生成してリストに追加する
    """
    bb_imgs = [] # 画像のリストと半径のリストを作成する
    bb_accs = [a for a in range(1, 11)]

    for r in range(1, 11): # 1から10までループを回して、各半径の円を描くSurfaceを生成してリストに追加する
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_imgs.append(bb_img)

    return bb_imgs, bb_accs # 画像のリストと半径のリストをタプルで返す


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    引数：なし
    値：辞書（キーが移動量のタプル、値がSurfaceの辞書）
    画像「3.png」を読み込み、各移動量の向きに回転・反転してSurfaceを作成して辞書に格納する
    """
    # 画像「3.png」を読み込み、各移動量の向きに回転・反転してSurfaceを作成して辞書に格納する
    kk_dict = {
        (0, 0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),  #何もしていないとき
        (0, -5):pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 270, 0.9), True, False),  #上
        (+5, -5):pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 0.9), True, False),  #右上
        (+5,  0):pg.transform.flip(pg.image.load("fig/3.png"), True, False),  #右
        (+5, +5):pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9), True, False),  #右下
        (0, +5):pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 0.9), True, False),  #下
        (-5, +5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9),  #左下
        (-5,  0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),  #左
        (-5, -5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 315, 0.9),  #左上
    }
    return kk_dict


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20)) #空のsurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #半径10の赤い円を描画
    bb_img.set_colorkey((0,0,0,)) #黒色を透過色に設定
    bb_rct = bb_img.get_rect() #爆弾Rect
    bb_rct.centerx = random.randint(0, WIDTH) #爆弾横座標
    bb_rct.centery = random.randint(0, HEIGHT) #爆弾縦座標
    vx, vy = +5, +5 #爆弾の横速度, 縦速度

    bb_imgs, bb_accs = init_bb_imgs()
    
    kk_imgs = get_kk_imgs()

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct): #こうかとんと爆弾が衝突したら
            game_over(screen)



        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #横方向の移動量
                sum_mv[1] += mv[1] #縦方向の移動量

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): #画面外なら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #移動を無かったことにする

        avx = vx * bb_accs[min(tmr // 500, 9)] # 速度を更新する
        avy = vy * bb_accs[min(tmr // 500, 9)] 

        kk_img = kk_imgs[tuple(sum_mv)] # 画像を取得する

        bb_img = bb_imgs[min(tmr // 500, 9)] # 画像「bb_img」を取得する
        bb_img.set_colorkey((0,0,0,)) # 背景色を黒に設定する

        bb_rct.width = bb_img.get_rect().width # Rectの幅と高さを取得する
        bb_rct.height = bb_img.get_rect().height

        bb_rct.move_ip(avx, avy) # 移動量を足す

        screen.blit(kk_img, kk_rct)
        yoko, tate = check_bound(bb_rct)
        if not yoko: #横方向にはみ出ていたら
            vx *= -1
        if not tate: #縦方向にはみ出ていたら
            vy *= -1
        bb_rct.move_ip(vx, vy) #爆弾の移動
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
