"""Describes the items in the game."""


class Item():
    """The base class for all items"""
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.description, self.value)


class Weapon(Item):
    def __init__(self, name, description, value, damage):
        self.damage = damage
        super().__init__(name, description, value)

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage: {}".format(self.name, self.description, self.value, self.damage)


class Rock(Weapon): 
    def __init__(self):
        super().__init__(name="Rock",
                         description="Just hope you don't run into any monsters while holding this, what the fuck are you going to do with a rock?",
                         value=0,
                         damage=3)


class Dagger(Weapon):
    def __init__(self):
        super().__init__(name="Dagger",
                         description="A small rusty knife. At least it's not a goddamn rock though.",
                         value=10,
                         damage=10)

class Sword(Weapon):
    def __init__(self):
        super().__init__(name="Sword",
                         description="A long steel blade, suitable for slashing and stabbing.",
                         value=15,
                         damage=15)
class Dildo(Weapon) :
    def __init__(self):
        super().__init__(name ="Mighty Dildo",
                         description="Brown boy's personal dildo! Great for sticking into holes",
                         value=69,
                         damage=696969)


class Gold(Item):
    def __init__(self, amt):
        self.amt = amt
        super().__init__(name="Gold",
                         description="A brown sack containing gold coins.".format(str(self.amt)),
                         value=self.amt)
