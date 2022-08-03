import pygame
from pygame.sprite import Sprite



class HP(Sprite):
    def __init__(self,ai_settings,screen):
        "初始化血量"
        super().__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        # 加载血条图像
        self.image_100 = pygame.image.load("images\hp_full.png")
        self.image_70 = pygame.image.load("images\hp_70.png")
        self.image_50 = pygame.image.load("images\hp_50.png")
        self.image_30 = pygame.image.load("images\hp_30.png")
        self.rect = self.image_100.get_rect()
        self.screen_rect = screen.get_rect()

        #放置血条
        self.rect.centerx = 50
        self.rect.bottom = 90

    def blitme(self):
        """在指定位置绘制血条"""
        if self.ai_settings.ship_hp/self.ai_settings.ship_max_hp == 1:
            self.screen.blit(self.image_100, self.rect)
        elif self.ai_settings.ship_hp/self.ai_settings.ship_max_hp >= 0.7:
            self.screen.blit(self.image_70, self.rect)
        elif self.ai_settings.ship_hp/self.ai_settings.ship_max_hp >= 0.5:
            self.screen.blit(self.image_50, self.rect)
        else:
            self.screen.blit(self.image_30, self.rect)
