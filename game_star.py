class GameStars:
    """跟踪游戏"""

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        # 最高得分
        with open("record/high_score.txt", "r") as high:
            self.high_score = int(high.read())

    def reset_stats(self):
        # 初始化信息
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
