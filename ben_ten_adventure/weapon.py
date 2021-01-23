"""
here will be different classes for weapons

- player can interact with NPCs using weapon
- NPC and player can be injured or killed by weapon

"""


class BaseWeapon:
    def __init__(self, damage, radius):
        self.damage = damage
        self.radius = radius
