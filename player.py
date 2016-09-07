from random import randint
import items, world
import pdb


class Player():
    def __init__(self):
        self.inventory = [items.Gold(15), items.Rock()]
        self.hp = 100
        self.location_x, self.location_y = world.starting_position
        self.victory = False

    def is_alive(self):
        return self.hp > 0

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def print_inventory(self):
        for item in self.inventory:
            print(item, '\n')

    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).intro_text())

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def calculate_crit(self, bestweapon):
        prob = randint(1,100)       #generate a random number
        # Each weapon should have a different critical hit ratio
        # If Rock gets a crit, it can double damage. But doubling damage of Mighty Dildo is OP
        if prob <= 20 and bestweapon.name == "Rock":
            return bestweapon.damage * 2
        elif prob <= 15 and bestweapon.name == "Dagger":
            return bestweapon.damage * 1.8
        elif prob <= 10 and bestweapon.name == "Sword":
            return bestweapon.damage * 1.5
        elif prob <= 5 and bestweapon.name == "Mighty Dildo":
            return bestweapon.damage * 1.2
        else:
            return bestweapon.damage

    def attack(self, enemy):
        best_weapon = None
        max_dmg = 0
        for i in self.inventory:
            if isinstance(i, items.Weapon): #finding the strongest weapon to use
                if i.damage > max_dmg:
                    max_dmg = i.damage
                    best_weapon = i
        dmg_dealt = self.calculate_crit(best_weapon)
        print("You use {} against {}!".format(best_weapon.name, enemy.name))
        if dmg_dealt != best_weapon.damage:
            print("CRITICAL HIT!".format(best_weapon.name))
        enemy.hp -= dmg_dealt
        if not enemy.is_alive():
            print("You killed {}!".format(enemy.name))
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))

    def flee(self, tile):
        """Moves the player randomly to an adjacent tile"""
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[r])

