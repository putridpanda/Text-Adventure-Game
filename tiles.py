"""Describes the tiles in the world space."""
import pdb

import items, enemies, actions, world
from random import randint


class MapTile:
    """The base class for a tile within the world space"""
    def __init__(self, x, y):
        """Creates a new tile.

        :param x: the x-coordinate of the tile
        :param y: the y-coordinate of the tile
        """
        self.x = x
        self.y = y

    def intro_text(self):
        """Information to be displayed when the player moves into this tile."""
        raise NotImplementedError()

    def modify_player(self, the_player):
        """Process actions that change the state of the player."""
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())

        return moves


class StartingRoom(MapTile):
    def intro_text(self):
        return """
        You find yourself in what seems to be center of a deep, dark cave.
        The paths leading to the rest of the cave are dark and foreboding.

        Escape the cave, and live. Fail, and die.
        """

    def modify_player(self, the_player):
        #Room has no action on player
        pass


class EmptyCavePath(MapTile):
    def intro_text(self):
        r = randint(0,3)
        if r == 0:
            return """
            Another unremarkable part of the cave. You must forge onwards.
            """
        elif r == 1:
            return """
            Mold grows on the wall, and a human skeleton rots in the corner.
            """
        elif r == 2:
            return """
            As you enter this section, a colony of bats flies at you!

            Is this the origin story of Batman????
            """
        else:
            """
            Water drips from the ceiling, as you walk through yet another empty section of
            this seemingly undending cave.
            """

    def modify_player(self, the_player):
        #Room has no action on player
        pass


class LootRoom(MapTile):
    """A room that adds something to the player's inventory"""
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, the_player): #Adds the loot to the player inventory
        #pdb.set_trace()
        if self.item.name == "Gold":
            newamt = self.item.amt
            the_player.inventory[0].amt += newamt
            the_player.inventory[0].value = the_player.inventory[0].amt


            
        elif self.item.name == "Dagger":
            has_dagger = False
            for member in the_player.inventory:
                if member.name == "Dagger":
                    has_dagger = True
            if not has_dagger:
                print("\nYou notice something shiny in the corner.\nIt's a dagger! You pick it up!\n")
                the_player.inventory.append(self.item)
            else:
                print("This is not the exit you are looking for. Move along.")


        elif self.item.name == "Sword":
            has_sword = False
            for member in the_player.inventory:
                if member.name == "Sword":
                    has_sword = True
            if not has_sword:
                print("A long, sharp sword lies against the wall. It seems to gleam in the darkness.\n")
                the_player.inventory.append(self.item)
            else:
                print("This is not the exit you are looking for. Move along.")


                
        else:
            the_player.inventory.append(self.item) #adds the item to the end of the inventory array

    def modify_player(self, the_player):
        self.add_loot(the_player)


class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger())

    def intro_text(self):
        pass

class FindSwordRoom(LootRoom):
    def __init__(self,x,y):
        super().__init__(x,y,items.Sword())

    def intro_text(self):
        return """
        You find a long sword in the center of the room.
        You're kind of OP now, so if you die, you really suck at this.
        """


class FindGoldRoom(LootRoom):
    def __init__(self, x, y):
        goldnum = randint(0, 20)
        super().__init__(x, y, items.Gold(goldnum))

    def intro_text(self):
        return """
        Someone dropped some gold!!! You pick it up.
        """
    
class DildoRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dildo())

    def intro_text(self):
        return """
        You hear whimpering coming from a dark corner...
        From the shadows emerges a brown boy.
        He pulls a giant dildo from his ass and hands it to you.
        """


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()


class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant spider jumps down from its web in front of you!
            """
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """


class OgreRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Ogre())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            An ogre is blocking your path!
            """
        else:
            return """
            A dead ogre reminds you of your triumph.
            """


class SnakePitRoom(MapTile):
    def intro_text(self):
        return """
        You have fallen into a pit of moderately dangerous snakes, and were brutally attacked!!!

        Luckily, you managed to escape!
        """

    def modify_player(self, player):
        player.hp /= 2


class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!


        Victory is yours!
        """

    def modify_player(self, player):
        player.victory = True
