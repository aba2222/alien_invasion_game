import pygame
from pygame.sprite import Group

import game_functions as gf
from button import Button
from game_star import GameStars
from music import Music
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from health_point import HP


def run_game():
    # 初始化游戏、设置屏幕和对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("game")

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    #创建血量
    hp = HP(ai_settings,screen)
    # 用于子弹的编组
    bullets = Group()
    aliens_bullets = Group()
    # 一个外星人编组
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens,aliens_bullets)
    # 储存统计信息
    stats = GameStars(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # 声音
    music = Music(ai_settings.music_volume)

    # 按钮
    play_button = Button(ai_settings, screen, "play", "EXIT")

    # 开始主循环
    while True:
        # 监视键盘和鼠标
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, music,aliens_bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button,aliens_bullets,hp)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets,aliens_bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets,aliens_bullets)

if __name__=="__main__":
    run_game()
