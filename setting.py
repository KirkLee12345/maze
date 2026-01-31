import json



class Settings:
    def __init__(self):
        self.block_size = 50  # 方格大小
        self.screen_width = 1200  # 屏幕宽度（必须是方格大小的整数倍）
        self.screen_height = 800  # 屏幕高度（必须是方格大小的整数倍）
        self.line_width = 4  # 墙壁线宽度
        self.finish_block_color = (0, 255, 0)  # 终点颜色（元组RGB值）
        self.debug_width = 300  # debug区域宽度
        self.bg_color = (255, 255, 255)  # 背景颜色（元组RGB值）
        self.line_color = (0, 0, 0)  # 墙壁颜色（元组RGB值）
        self.debug_bg_color = (200, 200, 200)  # debug区域背景颜色（元组RGB值）
        self.debug_text_size = 16  # debug区域文字大小
        self.debug_text_color = (0, 0, 0)  # debug区域文字颜色（元组RGB值）
        self.debug_block_text_size = 10  # debug模式下格子编号和坐标文字大小
        self.debug_block_text_color = (200, 200, 200)  # debug模式下格子编号和坐标文字颜色（元组RGB值）
        self.timer_text_color = (180, 180, 180)  # 计时器文字颜色（元组RGB值）
        self.player_default_color = (120, 0, 120)  # 玩家默认颜色（元组RGB值）
        self.player_default_r = 15  # 玩家默认半径
        self.fps = 60  # 帧率
        self.random_seed = 0  # 随机数种子（设置为0则每次运行都生成一个随机数）
        self.flag_default_color = (240, 0, 240)  # 标记点默认颜色（元组RGB值）
        self.flag_default_r = 10  # 标记点默认半径

    def save(self, path="setting.json"):
        with open(path, "w") as f:
            json.dump(self.__dict__, f)

    def load(self, path="setting.json"):
        with open(path, "r") as f:
            self.__dict__ = json.load(f)