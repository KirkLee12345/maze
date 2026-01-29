import random
import pygame



class settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.line_width = 4
        self.block_size = 50
        self.bg_color = (255, 255, 255)
        self.line_color = (0, 0, 0)
        self.fps = 60
        self.random_seed = 0  # 设置随机数种子，设置为0则每次运行都生成一个随机数
        self.player_default_color = (120, 0, 120)
        self.player_default_r = 15


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
        for i in range(int(setting.screen_width/setting.block_size)):
            self.blocks.append([])
            for j in range(int(setting.screen_height/setting.block_size)):
                self.blocks[i].append(block(False, False, False, False))
        self.fa = {}
        self.n = int(self.setting.screen_width / setting.block_size)
        self.m = int(self.setting.screen_height / setting.block_size)

    def draw(self, screen):
        for i in range(int(self.setting.screen_width/self.setting.block_size+1)):
            pygame.draw.line(screen, self.setting.line_color, (i*self.setting.block_size, 0), (i*self.setting.block_size, self.setting.screen_height), self.setting.line_width)
        for j in range(int(self.setting.screen_height/self.setting.block_size+1)):
            pygame.draw.line(screen, self.setting.line_color, (0, j*self.setting.block_size), (self.setting.screen_width, j*self.setting.block_size), self.setting.line_width)
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[i])):
                if self.blocks[i][j].u:
                    pygame.draw.line(screen, self.setting.bg_color, (i*self.setting.block_size+self.setting.line_width/2+1, j*self.setting.block_size), (i*self.setting.block_size+self.setting.block_size-self.setting.line_width/2, j*self.setting.block_size), self.setting.line_width)
                if self.blocks[i][j].l:
                    pygame.draw.line(screen, self.setting.bg_color, (i*self.setting.block_size, j*self.setting.block_size+self.setting.line_width/2+1), (i*self.setting.block_size, j*self.setting.block_size+self.setting.block_size-self.setting.line_width/2), self.setting.line_width)

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


class player:
    def __init__(self, setting, x, y, color=None, r=None):
        self.setting = setting
        self.color = color if color else setting.player_default_color
        self.r = r if r else setting.player_default_r
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x*self.setting.block_size+self.setting.block_size/2, self.y*self.setting.block_size+self.setting.block_size/2), self.r)

    def move(self, l, direction):
        if direction == "U" and l.blocks[self.x][self.y].u:
            self.y -= 1
        if direction == "D" and l.blocks[self.x][self.y].d:
            self.y += 1
        if direction == "L" and l.blocks[self.x][self.y].l:
            self.x -= 1
        if direction == "R" and l.blocks[self.x][self.y].r:
            self.x += 1








def main():
    pygame.init()
    setting = settings()

    clock = pygame.time.Clock()



    screen = pygame.display.set_mode((setting.screen_width + setting.line_width/2, setting.screen_height + setting.line_width/2))
    l = level(setting)
    l.generate_maze()
    p1 = player(setting, 0, 0)

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