import pygame
import random
from pygame.sprite import Sprite

from alien_bullet import ABullet


class Alien(Sprite):
    """外星人类"""

    def __init__(self, ai_settings, screen, aliens_bullets):
        """初始化"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.aliens_bullets = aliens_bullets

        # 加载图像
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 初始位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 储存位置
        self.x = float(self.rect.x)

    def blitme(self):
        """画外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """运动方向"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """移动"""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x
        """随机射子弹"""
        if random.randint(0,10000) == 1 and len(self.aliens_bullets) < 10:
            new_bullet = ABullet(self.ai_settings,self.screen,self)
            self.aliens_bullets.add(new_bullet)
