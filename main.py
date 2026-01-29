import random
import pygame
import json



class Settings:
    def __init__(self):
        self.block_size = 50  # 方格大小
        self.screen_width = 1200  # 屏幕宽度（必须是方格大小的整数倍）
        self.screen_height = 800  # 屏幕高度（必须是方格大小的整数倍）
        self.line_width = 4  # 墙壁线宽度
        self.bg_color = (255, 255, 255)  # 背景颜色（元组RGB值）
        self.line_color = (0, 0, 0)  # 墙壁颜色（元组RGB值）
        self.fps = 60  # 帧率
        self.random_seed = 0  # 随机数种子（设置为0则每次运行都生成一个随机数）
        self.player_default_color = (120, 0, 120)  # 玩家默认颜色（元组RGB值）
        self.player_default_r = 15  # 玩家默认半径

    def save(self, path="setting.json"):
        with open(path, "w") as f:
            json.dump(self.__dict__, f)

    def load(self, path="setting.json"):
        with open(path, "r") as f:
            self.__dict__ = json.load(f)


class Level:
    def __init__(self, setting):
        self.line_width = setting.line_width
        self.width = setting.screen_width
        self.height = setting.screen_height
        self.block_size = setting.block_size
        self.line_color = setting.line_color
        self.bg_color = setting.bg_color
        self.random_seed = setting.random_seed if setting.random_seed else random.randint(1, 100000000000000000000000000000000)
        self.n = int(setting.screen_width / setting.block_size)
        self.m = int(setting.screen_height / setting.block_size)
        self.blocks = []
        for i in range(self.n):
            self.blocks.append([])
            for j in range(int(self.m)):
                self.blocks[i].append({"u": False, "d": False, "l": False, "r": False})

    def draw(self, screen):
        for i in range(int(self.n+1)):
            pygame.draw.line(screen, self.line_color, (i*self.block_size, 0), (i*self.block_size, self.height), self.line_width)
        for j in range(int(self.m+1)):
            pygame.draw.line(screen, self.line_color, (0, j*self.block_size), (self.width, j*self.block_size), self.line_width)
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[i])):
                if self.blocks[i][j]["u"]:
                    pygame.draw.line(screen, self.bg_color, (i*self.block_size+self.line_width/2+1, j*self.block_size), (i*self.block_size+self.block_size-self.line_width/2, j*self.block_size), self.line_width)
                if self.blocks[i][j]["l"]:
                    pygame.draw.line(screen, self.bg_color, (i*self.block_size, j*self.block_size+self.line_width/2+1), (i*self.block_size, j*self.block_size+self.block_size-self.line_width/2), self.line_width)

    def generate_maze(self):
        fa = {}
        def connect_block(x, y):
            fa[findfa(x)] = findfa(y)
            x1 = x % self.n
            y1 = x // self.n
            x2 = y % self.n
            y2 = y // self.n
            if x1 == x2:
                if y1 > y2:
                    self.blocks[x1][y1]["u"] = True
                    self.blocks[x2][y2]["d"] = True
                else:
                    self.blocks[x1][y1]["d"] = True
                    self.blocks[x2][y2]["u"] = True
            else:
                if x1 > x2:
                    self.blocks[x1][y1]["l"] = True
                    self.blocks[x2][y2]["r"] = True
                else:
                    self.blocks[x1][y1]["r"] = True
                    self.blocks[x2][y2]["l"] = True

        def findfa(x):
            if fa[x] == x:
                return x
            return findfa(fa[x])

        for i in range(self.m):
            for j in range(self.n):
                fa[i*self.n+j] = i*self.n+j
        edges = []
        for i in range(self.m):
            for j in range(self.n):
                if j != self.n-1:
                    edges.append((i*self.n+j, i*self.n+j+1))
                if i != self.m-1:
                    edges.append((i*self.n+j, (i+1)*self.n+j))
        cnt = 0
        random.seed(self.random_seed)
        while cnt < self.m*self.n-1:
            t = random.choice(edges)
            edges.remove(t)
            if findfa(t[0]) != findfa(t[1]):
                connect_block(t[0], t[1])
                cnt += 1

    def save(self, path="maze.json"):
        with open(path, "w") as f:
            json.dump(self.__dict__, f)

    def load(self, path="maze.json"):
        with open(path, "r") as f:
            self.__dict__ = json.load(f)


class Player:
    def __init__(self, setting, x, y, color=None, r=None):
        self.block_size = setting.block_size
        self.color = color if color else setting.player_default_color
        self.r = r if r else setting.player_default_r
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x*self.block_size+self.block_size/2, self.y*self.block_size+self.block_size/2), self.r)

    def move(self, l, direction):
        if direction == "U" and l.blocks[self.x][self.y]["u"]:
            self.y -= 1
        if direction == "D" and l.blocks[self.x][self.y]["d"]:
            self.y += 1
        if direction == "L" and l.blocks[self.x][self.y]["l"]:
            self.x -= 1
        if direction == "R" and l.blocks[self.x][self.y]["r"]:
            self.x += 1



def main():
    pygame.init()
    setting = Settings()
    # setting.save()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((setting.screen_width + setting.line_width/2, setting.screen_height + setting.line_width/2))
    l = Level(setting)
    l.generate_maze()
    # l.save()
    p1 = Player(setting, 0, 0)
    pygame.display.set_caption("迷宫")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    p1.move(l, "U")
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    p1.move(l, "D")
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    p1.move(l, "L")
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    p1.move(l, "R")

        screen.fill(setting.bg_color)
        l.draw(screen)
        p1.draw(screen)
        clock.tick(setting.fps)
        pygame.display.set_caption(f"迷宫 FPS：{clock.get_fps():.1f}")
        pygame.display.update()



if __name__ == '__main__':
    main()