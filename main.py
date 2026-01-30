import sys
import pygame
from setting import Settings
from level import Level
from player import Player



def display_debug(screen, font, block_font, clock, setting, l, p1):
    texts = []
    clock.tick(setting.fps)
    texts.append(f"FPS: {clock.get_fps():.1f}")
    texts.append("")
    texts.append(f"seed: {l.random_seed}")
    texts.append("")
    texts.append(f"width: {setting.screen_width}  height: {setting.screen_height}")
    texts.append(f"bg_color: {l.bg_color}")
    texts.append(f"line_width: {l.line_width}")
    texts.append(f"line_color: {l.line_color}")
    texts.append("")
    texts.append(f"block_size: {l.block_size}")
    texts.append(f"n: {l.n}  m: {l.m}  total: {l.n*l.m}")
    texts.append("")
    texts.append(f"player_default_color: {setting.player_default_color}")
    texts.append(f"player_default_r: {setting.player_default_r}")
    texts.append(f"player_color: {p1.color}")
    texts.append(f"player_r: {p1.r}")
    texts.append(f"flag_default_color: {setting.flag_default_color}")
    texts.append(f"flag_default_r: {setting.flag_default_r}")
    texts.append(f"flag_color: {p1.flag_color}")
    texts.append(f"flag_r: {p1.flag_r}")
    texts.append("")
    texts.append(f"debug_bg_color: {setting.debug_bg_color}")
    texts.append(f"debug_text_size: {setting.debug_text_size}")
    texts.append(f"debug_text_color: {setting.debug_text_color}")
    texts.append(f"debug_block_text_size: {setting.debug_block_text_size}")
    texts.append(f"debug_block_text_color: {setting.debug_block_text_color}")
    texts.append("")
    texts.append(f"x: {p1.x} y: {p1.y}")
    texts.append(f"steps: {p1.steps}")

    pygame.draw.rect(screen, setting.debug_bg_color, (setting.screen_width + setting.line_width/2, 0, setting.debug_width, setting.screen_height + setting.line_width))
    for i, text in enumerate(texts):
        text_surface = font.render(text, True, setting.debug_text_color)
        screen.blit(text_surface, (setting.screen_width + setting.line_width, i*setting.debug_text_size))

    for i in range(l.n):
        for j in range(l.m):
            text = str(j*l.n+i)
            text_surface = block_font.render(text, True, setting.debug_block_text_color)
            screen.blit(text_surface, (setting.block_size*i+setting.line_width, setting.block_size*j+setting.line_width))
            text = f"({i}, {j})"
            text_surface = block_font.render(text, True, setting.debug_block_text_color)
            screen.blit(text_surface, (setting.block_size*i + setting.line_width, setting.block_size*j+setting.line_width + setting.debug_block_text_size))



def main():
    pygame.init()
    setting = Settings()
    font = pygame.font.SysFont('Arial', setting.debug_text_size)  # 系统字体
    block_font = pygame.font.SysFont('Arial', setting.debug_block_text_size)
    # setting.save()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((setting.screen_width + setting.line_width/2, setting.screen_height + setting.line_width/2))
    l = Level(setting)
    l.generate_maze()
    # l.save()
    p1 = Player(setting, 0, 0, flag=True)
    pygame.display.set_caption("迷宫")
    debug_mode = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    p1.move(l, "U")
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    p1.move(l, "D")
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    p1.move(l, "L")
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    p1.move(l, "R")
                if event.key == pygame.K_F3:
                    debug_mode = not debug_mode
                    if debug_mode:
                        screen = pygame.display.set_mode((setting.screen_width + setting.line_width / 2 + setting.debug_width, setting.screen_height + setting.line_width / 2))
                    else:
                        screen = pygame.display.set_mode((setting.screen_width + setting.line_width / 2, setting.screen_height + setting.line_width / 2))

        screen.fill(setting.bg_color)
        l.draw(screen)
        p1.draw(screen)
        if debug_mode:
            display_debug(screen, font, block_font, clock, setting, l, p1)
        pygame.display.update()



if __name__ == '__main__':
    main()
