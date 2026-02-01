import pygame



class Player:
    def __init__(self, setting, x, y, color=None, flag_default_color=None, r=None, flag_r=None, flag=False):
        self.block_size = setting.block_size
        self.color = color if color else setting.player_default_color
        self.flag_color = flag_default_color if flag_default_color else setting.flag_default_color
        self.r = r if r else setting.player_default_r
        self.flag_r = flag_r if flag_r else setting.flag_default_r
        self.x = x
        self.y = y
        self.steps = 0
        self.flag = flag
        self.flags = []

    def draw(self, screen):
        if self.flag:
            for flagxy in self.flags:
                pygame.draw.circle(screen, self.flag_color, (flagxy[0] * self.block_size + self.block_size / 2 +1, flagxy[1] * self.block_size + self.block_size / 2 +1), self.flag_r)
        pygame.draw.circle(screen, self.color, (self.x*self.block_size+self.block_size/2+1, self.y*self.block_size+self.block_size/2+1), self.r)

    def move(self, l, direction):
        def moved():
            self.flags.append((self.x, self.y))
            self.steps += 1
        if direction == "U" and l.blocks[self.x][self.y]["u"]:
            moved()
            self.y -= 1
        if direction == "D" and l.blocks[self.x][self.y]["d"]:
            moved()
            self.y += 1
        if direction == "L" and l.blocks[self.x][self.y]["l"]:
            moved()
            self.x -= 1
        if direction == "R" and l.blocks[self.x][self.y]["r"]:
            moved()
            self.x += 1