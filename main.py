import random
import pygame



class settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.line_width = 4
        self.bg_color = (255, 255, 255)
        self.fps = 60
        self.random_seed = 0  # 设置随机数种子，设置为0则每次运行都生成一个随机数


class block:
    def __init__(self, u, d, l, r):
        self.u = u
        self.d = d
        self.l = l
        self.r = r


class level:
    def __init__(self, setting):
        self.setting = setting
        self.blocks = []
        for i in range(int(setting.screen_width/50)):
            self.blocks.append([])
            for j in range(int(setting.screen_height/50)):
                self.blocks[i].append(block(False, False, False, False))
        self.fa = {}
        self.n = int(self.setting.screen_width / 50)
        self.m = int(self.setting.screen_height / 50)

    def draw(self, screen):
        for i in range(int(self.setting.screen_width/50+1)):
            pygame.draw.line(screen, (0, 0, 0), (i*50, 0), (i*50, self.setting.screen_height), self.setting.line_width)
        for j in range(int(self.setting.screen_height/50+1)):
            pygame.draw.line(screen, (0, 0, 0), (0, j*50), (self.setting.screen_width, j*50), self.setting.line_width)
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[i])):
                if self.blocks[i][j].u:
                    pygame.draw.line(screen, (255, 255, 255), (i*50+self.setting.line_width/2+1, j*50), (i*50+50-self.setting.line_width/2, j*50), self.setting.line_width)
                if self.blocks[i][j].l:
                    pygame.draw.line(screen, (255, 255, 255), (i*50, j*50+self.setting.line_width/2+1), (i*50, j*50+50-self.setting.line_width/2), self.setting.line_width)

    def connect_block(self, x, y):
        self.fa[self.findfa(x)] = self.findfa(y)
        x1 = x % self.n
        y1 = x // self.n
        x2 = y % self.n
        y2 = y // self.n
        if x1 == x2:
            if y1 > y2:
                self.blocks[x1][y1].u = True
                self.blocks[x2][y2].d = True
            else:
                self.blocks[x1][y1].d = True
                self.blocks[x2][y2].u = True
        else:
            if x1 > x2:
                self.blocks[x1][y1].l = True
                self.blocks[x2][y2].r = True
            else:
                self.blocks[x1][y1].r = True
                self.blocks[x2][y2].l = True

    def findfa(self, x):
        if self.fa[x] == x:
            return x
        return self.findfa(self.fa[x])

    def generate_maze(self):
        for i in range(self.m):
            for j in range(self.n):
                self.fa[i*self.n+j] = i*self.n+j
        edges = []
        for i in range(self.m):
            for j in range(self.n):
                if j != self.n-1:
                    edges.append((i*self.n+j, i*self.n+j+1))
                if i != self.m-1:
                    edges.append((i*self.n+j, (i+1)*self.n+j))
        cnt = 0
        if self.setting.random_seed == 0:
            self.setting.random_seed = random.randint(1, 100000000000000000000000000000000)
        random.seed(self.setting.random_seed)
        print("迷宫地图生成随机数种子为：", self.setting.random_seed)
        while cnt < self.m*self.n-1:
            t = random.choice(edges)
            edges.remove(t)
            if self.findfa(t[0]) != self.findfa(t[1]):
                self.connect_block(t[0], t[1])
                cnt += 1








def main():
    pygame.init()
    setting = settings()

    clock = pygame.time.Clock()



    screen = pygame.display.set_mode((setting.screen_width + setting.line_width/2, setting.screen_height + setting.line_width/2))
    l = level(setting)
    l.generate_maze()

    pygame.display.set_caption("迷宫")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        screen.fill(setting.bg_color)

        l.draw(screen)

        clock.tick(setting.fps)
        pygame.display.set_caption("迷宫 " + f"{clock.get_fps():.1f}")
        pygame.display.update()




if __name__ == '__main__':
    main()