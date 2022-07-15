import pygame
from pygame.sprite import Sprite


class ABullet(Sprite):
    """一个对子弹管理的类"""

    def __init__(self, ai_settings, screen, alien):
        """在飞船所处位置创建子弹"""
        super().__init__()
        self.screen = screen

        # 在（0,0）处创建一个表示子弹的矩形，在设置位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.top

        # 储存用小数表示子弹位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed = ai_settings.a_bullet_allowed

    def update(self):
        """向上移动"""
        self.y += self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上画子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)