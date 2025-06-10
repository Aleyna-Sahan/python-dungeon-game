import pygame, sys

from ui import Button, FONT, draw_character_pixel, draw_text
from constants import BLACK, WHITE

def combat(screen, clock, player, enemy):
    buttons = []
    skill_names = list(player.skills.keys())

    for i, skill in enumerate(skill_names):
        buttons.append(Button(50, 400 + i*60, 200, 50, skill, FONT, (50, 50, 50), WHITE))

    use_item_btn = Button(300, 400, 150, 50, "Eşya Kullan", FONT, (50, 50, 50), WHITE)

    while player.is_alive() and enemy.is_alive():
        screen.fill(BLACK)

        draw_character_pixel(screen, player.color, 100, 150)
        draw_character_pixel(screen, enemy.color, 600, 150, enemy.size)

        draw_text(screen, f"{player.name} - HP: {player.hp}  MP: {player.mp}", 50, 50, FONT)
        draw_text(screen, f"{enemy.name} - HP: {enemy.hp}", 50, 100, FONT)

        for btn in buttons:
            btn.draw(screen)
        use_item_btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, btn in enumerate(buttons):
                    if btn.is_clicked(event):
                        skill_name = skill_names[i]
                        success = player.use_skill(skill_name, enemy)
                        if not success:
                            break
                        if enemy.is_alive():
                            enemy.attack_player(player)
                        player.is_defending = False
                        break
                else:
                    if use_item_btn.is_clicked(event):
                        if len(player.inventory) == 0:
                            print("Envanterin boş!")
                        else:
                            item = player.inventory[0]
                            item.use(player)
                            player.inventory.pop(0)
                            if enemy.is_alive():
                                enemy.attack_player(player)
                            player.is_defending = False

        pygame.display.flip()
        clock.tick(30)

    if player.is_alive():
        print(f"{enemy.name} yenildi!")
        return True  # Oyuncu kazandı, hayatta
    else:
        print("Maalesef öldün... Oyun bitti.")
        return False  # Oyuncu öldü
