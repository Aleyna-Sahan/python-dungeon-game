import random
import pygame
from constants import WHITE, BLUE, YELLOW, GREEN, RED

skill_pools = {
    "Şövalye": {
        "Güçlü Darbe": {"damage": 40, "mp_cost": 3, "desc": "Ağır bir saldırı yapar."},
        "Kalkan Savunması": {"damage": 0, "mp_cost": 2, "defend": True, "desc": "Savunmaya geçer, hasarı azaltır."}
    },
    "Büyücü": {
        "Buz Oku": {"damage": 25, "mp_cost": 3, "desc": "Düşmanı dondurur."},
        "Yıldırım": {"damage": 40, "mp_cost": 6, "desc": "Gökyüzünden yıldırım düşürür."}
    },
    "Okçu": {
        "Zehirli Ok": {"damage": 20, "mp_cost": 2, "desc": "Zamanla hasar verir."},
        "Çift Ok": {"damage": 30, "mp_cost": 4, "desc": "Aynı anda 2 ok fırlatır."}
    }
}

def get_random_skill_for_class(character_class):
    pool = skill_pools.get(character_class, {})
    if not pool:
        return None, None  # O sınıfa ait yetenek yoksa None döner
    
    skill_name = random.choice(list(pool.keys()))
    skill_info = pool[skill_name]
    return skill_name, skill_info

class Button:
    def __init__(self, x, y, w, h, text, font=None, color=(200, 200, 200), text_color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = font or pygame.font.SysFont(None, 30)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Character:
    def __init__(self, name, cls):
        self.name = name
        self.cls = cls
        self.hp = 100
        self.mp = 50
        self.inventory = []
        self.is_defending = False

        if cls == "Şövalye":
            self.color = WHITE
            starter_skill = {
                "Kılıçla Vurma": {"damage": 100, "mp_cost": 0}
            }
        elif cls == "Büyücü":
            self.color = BLUE
            starter_skill = {
                "Ateş Topu": {"damage": 30, "mp_cost": 0}
            }
        elif cls == "Okçu":
            self.color = YELLOW
            starter_skill = {
                "Keskin Nişan": {"damage": 18, "mp_cost": 0, "crit_chance": 0.5}
            }
        else:
            starter_skill = {
                "Basit Saldırı": {"damage": 10, "mp_cost": 0}
            }

        self.skills = {}
        for skill_name, skill_info in starter_skill.items():
            self.skills[skill_name] = {"info": skill_info, "level": 1}

    def assign_skills_for_room(self, screen):
        pool = skill_pools.get(self.cls, {})
        # Yeteneklerden oyuncuda olmayanlar seçiliyor
        available_skills = [s for s in pool.items() if s[0] not in self.skills]

        if not available_skills:
            print("Yetenek havuzundan alınacak başka yetenek yok!")
            return

        # Rastgele 2 yetenek seçiliyor
        chosen_skills = random.sample(available_skills, k=min(2, len(available_skills)))

        # Seçim ekranını göster
        self.show_skill_selection(screen, chosen_skills)

    def show_skill_selection(self, screen, chosen_skills):
        pygame.font.init()
        clock = pygame.time.Clock()
        buttons = []
        start_x, start_y = 100, 100
        width, height = 300, 50
        font = pygame.font.SysFont(None, 30)

        # Butonları oluştur
        for i, (skill_name, skill_info) in enumerate(chosen_skills):
            btn = Button(start_x, start_y + i*(height + 10), width, height, skill_name, font=font)
            buttons.append((btn, skill_name, skill_info))

        selecting = True
        while selecting:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    selecting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn, skill_name, skill_info in buttons:
                        if btn.is_clicked(pos):
                            # Yetenek seçildiğinde oyuncuya ekle
                            self.skills[skill_name] = {"info": skill_info, "level": 1}
                            print(f"Yetenek seçildi: {skill_name}")
                            selecting = False

            # Butonları çiz
            for btn, _, _ in buttons:
                btn.draw(screen)

            pygame.display.flip()
            clock.tick(30)

    def get_skill_names(self):
        return list(self.skills.keys())

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        if self.is_defending:
            dmg = max(0, dmg // 2)
        self.hp -= dmg

    def use_skill(self, skill_name, enemy):
        if skill_name not in self.skills:
            print(f"{skill_name} kullanılamıyor!")
            return False
        skill_data = self.skills[skill_name]
        skill = skill_data["info"]
        level = skill_data["level"]

        mp_cost = skill.get("mp_cost", 0)
        if self.mp < mp_cost:
            print("Yeterli MP'n yok!")
            return False
        self.mp -= mp_cost
        self.is_defending = skill.get("defend", False)

        base_damage = skill.get("damage", 0)
        damage = base_damage * (1 + 0.1 * (level - 1))

        if "crit_chance" in skill:
            if random.random() < skill["crit_chance"]:
                damage *= 2
                print("Kritik vuruş!")

        damage = int(damage)

        if damage > 0:
            enemy.take_damage(damage)
            print(f"{skill_name} ile {damage} hasar verildi.")
        else:
            print(f"{skill_name} ile hasar verilmedi.")

        return True

class Enemy:
    def __init__(self, name, hp, attack, color=GREEN, size=40):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.color = color
        self.size = size
        self.is_defending = False

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        if self.is_defending:
            dmg = max(0, dmg // 2)
        self.hp -= dmg

    def attack_player(self, player):
        damage = self.attack
        if player.is_defending:
            damage = max(0, damage // 2)
        player.hp -= damage

class Item:
    def __init__(self, name, heal_amount=0, mp_restore=0):
        self.name = name
        self.heal_amount = heal_amount
        self.mp_restore = mp_restore

    def use(self, player):
        if self.heal_amount > 0:
            max_hp = 120 if player.cls == "Şövalye" else 100
            player.hp = min(player.hp + self.heal_amount, max_hp)
        if self.mp_restore > 0:
            max_mp = 50 if player.cls == "Büyücü" else 30
            player.mp = min(player.mp + self.mp_restore, max_mp)

def enter_room(player, screen, clock, room_type):
    if room_type == "eşya":
        # Örnek seçim metodu, kendi kodunda seçimi yap
        choice = select_room_choice(screen, clock)  # Bu fonksiyon sende olmalı

        if choice == "skill":
            player.assign_skills_for_room(screen)
        elif choice == "item":
            item = Item("Can İksiri", heal_amount=30)
            player.inventory.append(item)
            print("Eşya odası! Can İksiri bulundu.")

def select_room_choice(screen, clock):
    selecting = True
    font = pygame.font.SysFont(None, 40)
    while selecting:
        screen.fill((0, 0, 0))
        text1 = font.render("S: Yetenek Seç", True, (255, 255, 255))
        text2 = font.render("I: Eşya Al", True, (255, 255, 255))
        screen.blit(text1, (100, 100))
        screen.blit(text2, (100, 160))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                selecting = False
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return "skill"
                elif event.key == pygame.K_i:
                    return "item"
        clock.tick(30)
