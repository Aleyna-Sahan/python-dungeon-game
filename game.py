import pygame
import sys
from constants import *
from characters import Enemy, get_random_skill_for_class
from screens import intro_screen, character_select_screen, game_over_screen
from rooms import generate_room, enter_room
from combat import combat
from ui import select_room_choice  # Eksik olan bu

def game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Basit RPG")
    clock = pygame.time.Clock()

    while True:
        intro_screen(screen, clock)
        player = character_select_screen(screen, clock)

        floors = 50
        rooms_per_floor = 10
        alive = True
        won = False

        for floor in range(floors):
            print(f"{floor+1}. katta ilerliyorsun...")
            for room_number in range(1, rooms_per_floor + 1):
                print(f"{room_number}. odaya girdin...")
                room_type = generate_room()

                # Eğer son oda ise boss odası
                if room_number == rooms_per_floor:
                    if floor == floors - 1:
                        boss = Enemy("Minotaur - Boss", 100, 20, RED, 60)
                        alive = combat(screen, clock, player, boss)
                        if player.is_alive():
                            won = True
                        else:
                            alive = False
                        break
                    else:
                        boss = Enemy("Kat Bossu", 80, 15, RED, 50)
                        alive = combat(screen, clock, player, boss)
                        if not player.is_alive():
                            alive = False
                            break
                else:
                    # Odaya gir
                    alive = enter_room(room_type, player, screen, clock, room_number)

                    if not alive:
                        break

                    # Eğer eşya odasıysa rastgele yetenek göster
                    if room_type == "item":
                        skill_name, skill_info = get_random_skill_for_class(player.cls)
                        choice = select_room_choice(screen, clock, current_skill_name=skill_name)

                        if choice == "skill":
                            player.skills[skill_name] = {"info": skill_info, "level": 1}
                            print(f"Yeni yetenek: {skill_name}")

            if not alive or won:
                break

        if won:
            yeniden = game_over_screen(screen, clock, won=True)
        else:
            yeniden = game_over_screen(screen, clock, won=False)

        if not yeniden:
            break


if __name__ == "__main__":
    game()
