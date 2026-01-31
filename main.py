import sys
import pygame
from setting import Settings
from level import Level
from player import Player
import time



def display_debug(screen, font, block_font, clock, setting, l, p1, start_time):
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
    texts.append(f"start_time: {start_time}")
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


def display_timer(screen, font, setting, start_time, end_time, finished):
    elapsed_time = end_time - start_time
    tmin = int(elapsed_time // 60)
    tsec = int(elapsed_time % 60)
    msec = int(elapsed_time * 1000 % 1000)
    text = f"{tmin:02d}:{tsec:02d}:{msec:03d}"
    k = max((5000-(elapsed_time * 1000))/5000, 0)
    if k == 0 and not finished:
        return text
    text_surface = font.render(text, True, setting.timer_text_color)
    text_surface.set_alpha(int(k*255) if not finished else 255)
    text_rect = text_surface.get_rect()
    text_rect.center = screen.get_rect().center
    screen.blit(text_surface, text_rect)
    return text



def main():
    pygame.init()
    setting = Settings()
    font = pygame.font.SysFont('Arial', setting.debug_text_size)  # 系统字体
    block_font = pygame.font.SysFont('Arial', setting.debug_block_text_size)
    timer_font = pygame.font.SysFont('Arial', int(setting.screen_width / 20))
    # setting.save()
    clock = pygame.time.Clock()
    l = Level(setting)
    l.generate_maze()
    # l.save()
    p1 = Player(setting, 0, 0, flag=True)
    pygame.display.set_caption("迷宫")
    debug_mode = False
    finished = False

    screen = pygame.display.set_mode((setting.screen_width + setting.line_width / 2, setting.screen_height + setting.line_width / 2))

    text_surface = timer_font.render("Press Enter to generate maze and start timer.", True, setting.timer_text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = screen.get_rect().center

    _ = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                _ = True
                break
        if _:
            break
        screen.fill(setting.bg_color)
        screen.blit(text_surface, text_rect)
        pygame.display.update()

    start_time = time.time()

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
        if not finished:
            end_time = time.time()
        if p1.x == l.n-1 and p1.y == l.m-1:
            finished = True
        timer_text = display_timer(screen, timer_font, setting, start_time, end_time, finished)
        p1.draw(screen)
        if debug_mode:
            display_debug(screen, font, block_font, clock, setting, l, p1, start_time)
        pygame.display.set_caption("迷宫 " + timer_text)
        pygame.display.update()



if __name__ == '__main__':
    main()
