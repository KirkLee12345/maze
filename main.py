import pygame
import numpy



class settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.line_width = 4
        self.bg_color = (255, 255, 255)
        self.fps = 60


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







def main():
    pygame.init()
    setting = settings()

    clock = pygame.time.Clock()



    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))
    l = level(setting)
    l.blocks[10][10].u = True
    l.blocks[10][10].l = True

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