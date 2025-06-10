import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fontlar
FONT = pygame.font.SysFont(None, 30)
BIGFONT = pygame.font.SysFont(None, 72)

def wait_for_click(clock):
    waiting = True
    while waiting:
        clock.tick(60)  # FPS'yi sabitle
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

pygame.font.init()  # Font sistemini başlat

# Yazı tipi tanımlamaları
FONT_LARGE = pygame.font.SysFont("arial", 48)
FONT_MEDIUM = pygame.font.SysFont("arial", 36)
FONT_SMALL = pygame.font.SysFont("arial", 24)
