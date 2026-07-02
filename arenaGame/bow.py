from rangedWeapon import RangedWeapon

class Bow(RangedWeapon):
    def __init__(self, owner):
        super().__init__(
            owner=owner,
            damage=3,
            projectile_speed=400,
            cooldown=1)
