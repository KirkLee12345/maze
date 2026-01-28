import pygame




class settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)
        self.fps = 60


def main():
    pygame.init()
    setting = settings()

    clock = pygame.time.Clock()



    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))
    pygame.display.set_caption("迷宫")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        screen.fill(setting.bg_color)



        clock.tick(setting.fps)
        pygame.display.set_caption("迷宫 " + f"{clock.get_fps():.1f}")
        pygame.display.update()




if __name__ == '__main__':
    main()