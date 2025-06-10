import pygame, random, sys
from constants import WHITE, BLACK
from characters import get_random_skill_for_class

pygame.init()
FONT = pygame.font.Font(None, 24)

class Button:
    def __init__(self, x, y, width, height, text, font, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

def draw_text(screen, text, x, y, font, color=WHITE):
    surf = font.render(text, True, color)
    rect = surf.get_rect(topleft=(x, y))
    screen.blit(surf, rect)

def show_skill_selection(screen, chosen_skills, player):
    buttons = []
    start_x, start_y = 100, 100
    w, h = 300, 50

    for i, (skill_name, skill_info) in enumerate(chosen_skills):
        btn = Button(start_x, start_y + i*(h + 10), w, h, skill_name, FONT, WHITE, BLACK)
        buttons.append((btn, skill_name, skill_info))

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn, skill_name, skill_info in buttons:
                    if btn.is_clicked(event):
                        player.skills[skill_name] = {"info": skill_info, "level": 1}
                        print(f"Seçilen yetenek: {skill_name}")
                        running = False

        for btn, _, _ in buttons:
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(30)

def select_skill_upgrade(screen, clock, player):
    skills = random.sample(list(player.skill_pool.keys()), k=3)
    buttons = []

    for i, skill in enumerate(skills):
        btn = Button(100, 100 + i * 80, 300, 60, skill, FONT, WHITE, BLACK)
        buttons.append(btn)

    selecting = True
    while selecting:
        screen.fill(BLACK)

        for btn in buttons:
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in buttons:
                    if btn.is_clicked(event):
                        selected_skill = btn.text
                        if selected_skill in player.skills:
                            player.skills[selected_skill]["level"] += 1
                            # mp_cost ve damage bilgisi skill_info'dan alınmalı yoksa default atanmalı
                            if "mp_cost" in player.skills[selected_skill]:
                                player.skills[selected_skill]["mp_cost"] = max(1, player.skills[selected_skill]["mp_cost"] - 1)
                            if "damage" in player.skills[selected_skill]:
                                player.skills[selected_skill]["damage"] += 5
                            print(f"{selected_skill} yeteneği seviye atladı!")
                        else:
                            skill_info = player.skill_pool[selected_skill]
                            player.skills[selected_skill] = {
                                "level": 1,
                                "mp_cost": skill_info.get("mp_cost", 10),
                                "damage": skill_info.get("damage", 15),
                                "color": skill_info.get("color", WHITE)
                            }
                            print(f"Yeni yetenek öğrendin: {selected_skill}")
                        selecting = False
                        break

        pygame.display.flip()
        clock.tick(30)

def select_room_choice(screen, clock, current_skill_name=None):
    running = True

    item_button = Button(100, 300, 200, 60, "Can İksiri Al", FONT, WHITE, BLACK)
    skill_text = current_skill_name if current_skill_name else "Yetenek Al"
    skill_button = Button(400, 300, 200, 60, skill_text, FONT, WHITE, BLACK)

    while running:
        screen.fill(BLACK)
        draw_text(screen, "Eşya Odası! Bir ödül seç:", 100, 100, FONT)

        item_button.draw(screen)
        skill_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if item_button.is_clicked(event):
                    return "item"
                elif skill_button.is_clicked(event):
                    return "skill"

        clock.tick(60)

def draw_character_pixel(screen, color, x, y, size=40):
    pygame.draw.rect(screen, color, (x, y, size, size))
