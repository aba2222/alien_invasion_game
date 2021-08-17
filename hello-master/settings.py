class Settings:
    """初始化所有类"""

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        # 飞船的设置
        # 飞船速度
        self.ship_speed = 1.5
        self.ship_limit = 3
        # 子弹设置
        self.bullet_width = 1000
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 3
        # 外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 5

        # 以什么样的速度加快游戏
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        # 音量
        self.music_volume = 0.1

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        self.alien_points = 50


        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)


