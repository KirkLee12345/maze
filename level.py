import pygame
import random
import json



class Level:
    def __init__(self, setting):
        self.line_width = setting.line_width
        self.width = setting.screen_width
        self.height = setting.screen_height
        self.block_size = setting.block_size
        self.line_color = setting.line_color
        self.bg_color = setting.bg_color
        self.finish_block_color = setting.finish_block_color
        self.random_seed = setting.random_seed if setting.random_seed else random.randint(1, 10000000000000000)
        self.n = int(setting.screen_width / setting.block_size)
        self.m = int(setting.screen_height / setting.block_size)
        self.finish_x = self.n-1
        self.finish_y = self.m-1
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
        pygame.draw.rect(screen, self.finish_block_color, (self.finish_x*self.block_size+self.line_width-1, self.finish_y*self.block_size+self.line_width-1, self.block_size-self.line_width, self.block_size-self.line_width), 0)

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

    def save_to_file(self, path="maze.json"):
        with open(path, "w") as f:
            json.dump(self.__dict__, f)

    def load_from_file(self, path="maze.json"):
        with open(path, "r") as f:
            self.__dict__ = json.load(f)

    def to_dict_string(self):
        return json.dumps(self.__dict__)

    def load_from_dict_string(self, string):
        self.__dict__ = json.loads(string)