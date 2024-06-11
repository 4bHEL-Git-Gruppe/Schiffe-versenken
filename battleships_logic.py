"""
## BATTLESHIPS ##

Board class implements functions for board

Ship class with
 - ship size
 - position
 - (name, ..)



"""

from typing import Literal


class Ship:
    """
    tracks individual ships hitpoints and where it was hit
    whether it is still alive can be read from self.alive
    position always starts at the top left
    rotation is can be entered using the size argument
    also supports non-regular rectangular shapes (e.g. 2x2)
    """
    def __init__(self, size: tuple, position: tuple, name: str) -> None:
        self.size = size
        self.position = position
        self.name = name
        self.alive = True

        self.destroyedParts = list()

    def hit(self, target: tuple) -> bool:
        """
        checks if the ship is hit by a missile hitting the target position
        if so the hit is executed

        parameters:
            target: tuple(x, y) -- tuple containing x, y positions of the target

        Returns
            -> bool -- if an alive part of the ship was hit
        
        """
        # if the ship was already sunk there's no need to check
        if not self.alive:
            return False
        
        # is target on ship
        if (self.position[0] <= target[0] <= self.position[0] + self.size[0] - 1
        and self.position[1] <= target[1] <= self.position[1] + self.size[1] - 1):
            if (pos := (target[0] - self.position[0], target[1] - self.position[1])) in self.destroyedParts:
                return False
            else:
                self.destroyedParts.append(pos)
                # if all parts are hit
                if len(self.destroyedParts) >= self.size[0] * self.size[1]:
                    self.alive = False
                return True
        else:
            return False


class Board:
    def __init__(self, size: tuple, starting_player: int=0, ships: list=None):
        self.active_player = starting_player

        self.size = size

        if not ships:
            self.ship_selection = [(1, 5), (1, 4), (1, 3), (1, 3), (1, 2)]       # fill with ships to be used
        else:
            self.ship_selection = ships

        self.ship_templates = {"carrier": 5,
                               "battleship": 4,
                               "destroyer": 3,
                               "submarine": 3,
                               "boat": 2}

        self.ships = [list(), list()]

        self.unused_ships = [self.ship_selection, self.ship_selection]

    def _set_ship(self, player: int, ship_size: tuple | int, position: tuple, rotation: Literal["v", "h"]=None, name: str=None) -> bool:
        # player id is out of range
        if player not in (1, 2):
            return False
        
        # convert shipsize int and rotation to ship_size tuple
        if isinstance(ship_size, int):
            if not rotation:
                return False
            if rotation == "v":
                ship_size = (1, ship_size)
            elif rotation == "h":
                ship_size = (ship_size, 1)
        
        # remove used ship from available
        if ship_size in self.unused_ships:
            self.unused_ships.remove(ship_size)
        elif (_ship_size := ship_size[::-1]) in self.unused_ships:
            self.unused_ships.remove(_ship_size)
        else:
            return False
        
        # position not on board
        if not (0 <= position[0] <= self.size[0] and 0 <= position[1] <= self.size[1]):
            return False
        
        # ship to big to fit on board
        if not (position[0] + ship_size[0] <= self.size[0] and position[1] + ship_size[1] <= self.size[1]):
            return False
        
        # no name given: generate iterative one
        if not name:
            name = f"battleship_{len(self.ships[player])}"

        self.ships[player].append(Ship(ship_size, position, name))

        return True

    def set_ship(self, player: int, ship: str, position: tuple, rotation: Literal["v", "h"], name=None) -> bool:
        if ship not in self.ship_templates.keys():
            return False
        
        return self._set_ship(player=player, ship_size=self.ship_templates[ship], position=position, rotation=rotation, name=name)
