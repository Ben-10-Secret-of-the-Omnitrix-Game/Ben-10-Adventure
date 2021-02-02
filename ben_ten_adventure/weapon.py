"""
here will be different classes for weapons

- player can interact with NPCs using weapon
- NPC and player can be injured or killed by weapon

"""


class BaseWeapon:
    def __init__(self, damage, radius, attack_pause=40):
        self.damage = damage
        self.radius = radius
        self.attack_pause = attack_pause
