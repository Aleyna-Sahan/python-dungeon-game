import random
import pygame
from characters import Character, Enemy, Item, get_random_skill_for_class
from constants import GREEN, WHITE, FONT_LARGE, wait_for_click
from combat import combat
from enemys import create_goblin, create_snake, create_ghost
from ui import select_skill_upgrade, select_room_choice, show_skill_selection

def get_random_enemy():
    enemy_creators = [create_goblin, create_snake, create_ghost]
    return random.choice(enemy_creators)()

def enter_room(room_type, player, screen, clock, room_number):
    screen.fill((0, 0, 0))

    # Oda adını belirle
    if room_type == "boş":
        room_name = "Boş Oda"
    elif room_type == "eşya":
        room_name = "Eşya Odası"
    elif room_type == "düşman":
        room_name = "Düşman Odası"
    elif room_type == "boss":
        room_name = "Boss Odası"
    else:
        room_name = "Bilinmeyen Oda"

    # Oda bilgilerini ekrana yaz
    text = FONT_LARGE.render(f"{room_number}. Oda: {room_name}", True, WHITE)
    screen.blit(text, (100, 200))
    pygame.display.flip()

    wait_for_click(clock)

    # === ODA TÜRLERİ ===
    if room_type == "boş":
        print("Oda boş, dinleniyorsun...")
        max_hp = 120 if player.cls == "Şövalye" else 100
        player.hp = min(player.hp + 10, max_hp)
        print(f"10 can yeniledin! (Yeni HP: {player.hp})")

    elif room_type == "eşya":
        # Karakter sınıfına uygun rastgele yetenek seç
        skill_name, skill_info = get_random_skill_for_class(player.cls)

        # Yetenek ismini buton üstünde göstermek için gönder
        choice = select_room_choice(screen, clock, current_skill_name=skill_name)

        if choice == "skill":
            if skill_name in player.skills:
                # Aynı yetenek varsa seviyesini artır
                player.skills[skill_name]["level"] += 1
                print(f"{skill_name} yeteneği seviye atladı!")
            else:
                # Yeni yetenek ekle
                player.skills[skill_name] = {"info": skill_info, "level": 1}
                print(f"Yeni yetenek kazandın: {skill_name}")
        elif choice == "item":
            item = Item("Can İksiri", heal_amount=30)
            player.inventory.append(item)
            print("Can İksiri aldın ve envantere eklendi.")

    elif room_type == "düşman":
        enemy = get_random_enemy()
        return combat(screen, clock, player, enemy)

    elif room_type == "boss":
        enemy = Enemy("Ağaç Canavarı", 150, 20)
        return combat(screen, clock, player, enemy)

    return player.is_alive()

def generate_room():
    room_types = ["düşman", "eşya", "boş"]
    return random.choice(room_types)
