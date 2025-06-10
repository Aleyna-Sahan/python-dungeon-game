import random
from constants import GREEN  # Varsa

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


def create_goblin():
    return Enemy("Goblin", 40, 10, GREEN, 40)

def create_snake():
    return Enemy("Yılan", 35, 8, (100, 200, 100), 30)

def create_ghost():
    return Enemy("Hayalet", 50, 12, (150, 150, 255), 45)

