import pygame
import sys
from constants import *
from ui import Button, draw_text, draw_character_pixel
from characters import Character

def intro_screen(screen, clock):
    screen.fill(BLACK)
    title_text = "DUNGEON MASTER"
    prompt_text = "Başlamak için bir tuşa basın"
    title_surf = BIGFONT.render(title_text, True, WHITE)
    prompt_surf = FONT.render(prompt_text, True, WHITE)
    title_rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//3))
    prompt_rect = prompt_surf.get_rect(center=(WIDTH//2, HEIGHT//2))

    screen.blit(title_surf, title_rect)
    screen.blit(prompt_surf, prompt_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        clock.tick(30)

def game_over_screen(screen, clock, won=False):
    screen.fill(BLACK)
    if won:
        over_text = "TEBRİKLER! KAZANDIN"
    else:
        over_text = "ÖLDÜN!"
    prompt_text = "Yeniden Oyna veya Çık"

    over_surf = BIGFONT.render(over_text, True, WHITE)
    prompt_surf = FONT.render(prompt_text, True, WHITE)

    over_rect = over_surf.get_rect(center=(WIDTH//2, HEIGHT//3))
    prompt_rect = prompt_surf.get_rect(center=(WIDTH//2, HEIGHT//3 + 60))

    # Butonlar
    btn_width, btn_height = 150, 50
    btn_y = HEIGHT//2

    retry_button = Button(WIDTH//2 - btn_width - 20, btn_y, btn_width, btn_height, "Yeniden Oyna", FONT, (0, 128, 0), WHITE)
    quit_button = Button(WIDTH//2 + 20, btn_y, btn_width, btn_height, "Çık", FONT, (128, 0, 0), WHITE)

    screen.blit(over_surf, over_rect)
    screen.blit(prompt_surf, prompt_rect)

    retry_button.draw(screen)
    quit_button.draw(screen)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if retry_button.is_clicked(event):
                waiting = False
                return True  # Yeniden dene
            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()
        clock.tick(30)

def character_select_screen(screen, clock):
    buttons = []
    classes = ["Şövalye", "Büyücü", "Okçu"]
    colors = [WHITE, (0, 0, 255), (255, 255, 0)]  # WHITE, BLUE, YELLOW gibi

    for i, cls in enumerate(classes):
        buttons.append(Button(300, 200 + i*80, 200, 50, cls, FONT, (50, 50, 50), WHITE))

    BIGFONT = pygame.font.Font(None, 48)

    while True:
        screen.fill(BLACK)
        draw_text(screen, "Karakter Sınıfını Seç", 280, 100, BIGFONT)

        for i, color in enumerate(colors):
            draw_character_pixel(screen, color, 220, 205 + i*80, 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for btn in buttons:
                if btn.is_clicked(event):
                    player = Character("Kahraman", btn.text)
                    return player

        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(30)

