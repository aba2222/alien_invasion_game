import pygame.mixer


class Music:
    """音效"""

    def __init__(self, music_volume):
        self.boom = pygame.mixer.Sound("images/boom.wav")
        self.boom.set_volume(music_volume)
