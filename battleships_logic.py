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

    def on_ship(self, position: tuple) -> bool:
        if (self.position[0] <= position[0] <= self.position[0] + self.size[0] - 1
        and self.position[1] <= position[1] <= self.position[1] + self.size[1] - 1):
            return True
        else:
            return False

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
        if self.on_ship(target):
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
    def __init__(self, size: tuple, starting_player: int=0, ships: list=None, spacing: Literal["cornersok", "nocorners", "none"]="cornersok"):
        self.active_player = starting_player

        self.size = size

        if not ships:
            self.ship_selection = [(1, 5), (1, 4), (1, 3), (1, 3), (1, 2)]       # fill with ships to be used
        else:
            self.ship_selection = ships

        self.spacing = spacing

        self.ship_templates = {"carrier": 5,
                               "battleship": 4,
                               "destroyer": 3,
                               "submarine": 3,
                               "boat": 2}

        self.ships = [list(), list()]

        self.unused_ships = [self.ship_selection[::], self.ship_selection[::]]

    def _is_valid_position(self, player: int, ship_size: tuple, position: tuple) -> bool:
        # position not on board
        if not (0 <= position[0] <= self.size[0] and 0 <= position[1] <= self.size[1]):
            return False
        
        # ship to big to fit on board
        if not (position[0] + ship_size[0] <= self.size[0] and position[1] + ship_size[1] <= self.size[1]):
            return False
        
        # overlap to other ships
        if self.spacing == "gap":
            notspace = 0
        else:
            notspace = 1

        for ship in self.ships[player]:
            if self.spacing == "cornersok":
                if (ship.position[0] - ship_size[0] + 1 <= position[0] <= ship.position[0] + ship.size[0] - 1       # direct overlap x
                and ship.position[1] - ship_size[1] <= position[1] <= ship.position[1] + ship.size[1]):             # gap overlap y
                    return False
                elif (ship.position[0] - ship_size[0] <= position[0] <= ship.position[0] + ship.size[0]             # gap overlap x
                and ship.position[1] - ship_size[1] + 1 <= position[1] <= ship.position[1] + ship.size[1] - 1):     # direct overlap y
                    return False
            
            elif (ship.position[0] - ship_size[0] + notspace <= position[0] <= ship.position[0] + ship.size[0] - notspace
            and ship.position[1] - ship_size[1] + notspace <= position[1] <= ship.position[1] + ship.size[1] - notspace):
                return False
        
        return True

    def _set_ship(self, player: int, ship_size: tuple | int, position: tuple, rotation: Literal["v", "h"]=None, name: str=None) -> bool:
        # player id is out of range
        if player not in range(0, len(self.ships)):
            return False
        
        # convert shipsize int and rotation to ship_size tuple
        if isinstance(ship_size, int):
            if not rotation:
                return False
            if rotation == "v":
                ship_size = (1, ship_size)
            elif rotation == "h":
                ship_size = (ship_size, 1)

        # position not on board
        if not self._is_valid_position(player, ship_size, position):
            return False
        
        # remove used ship from available
        if ship_size in self.unused_ships[player]:
            self.unused_ships[player].remove(ship_size)
        elif (_ship_size := ship_size[::-1]) in self.unused_ships[player]:
            self.unused_ships[player].remove(_ship_size)
        else:
            return False
        
        # no name given: generate iterative one
        if not name:
            name = f"battleship_{len(self.ships[player])}"

        self.ships[player].append(Ship(ship_size, position, name))

        return True

    def set_ship(self, player: int, ship: str, position: tuple, rotation: Literal["v", "h"], name: str=None) -> bool:
        if ship not in self.ship_templates.keys():
            return False
        
        return self._set_ship(player=player, ship_size=self.ship_templates[ship], position=position, rotation=rotation, name=name)

    def attack(self, player: int, position: tuple) -> bool:
        # player id is incorrect
        if player != self.active_player:
            return False
        
        for ship in self.ships[(player+1)%len(self.ships)]:
            if ship.hit(position):
                return True
        
        self.active_player = (player+1)%len(self.ships)   # switch player

        return False
    
    def is_defeated(self, player: int) -> bool:
        # player id is out of range
        if player not in range(0, len(self.ships)):
            return False
        
        for ship in self.ships[player]:
            if ship.alive:
                return False
        return True
    
def draw(board, player):
    canvas = [[" "]]
    for i in range(0, board.size[0]):
        canvas[0].append(" " + str(i) + " ")
    for y in range(board.size[1]):
        line = [str(y)]
        for x in range(board.size[0]):
            for ship in board.ships[player]:
                if ship.on_ship((x, y)):
                    if (x-ship.position[0], y-ship.position[1]) in ship.destroyedParts:
                        line.append(" □ ")
                    else:
                        line.append(" . ")
                    break
            else:
                line.append(" . ")
        canvas.append(line)

    for line in canvas:
        print("".join(line))
            

if "__main__" == __name__:
    boards = Board((10, 10))

    """
    "carrier": 5,
    "battleship": 4,
    "destroyer": 3,
    "submarine": 3,
    "boat": 2
    
    
    """

    while True:
        if len(boards.unused_ships[0]) > 0:
            active = 0
        elif len(boards.unused_ships[1]) > 0:
            active = 1
        else:
            print("finished setting")
            break

        draw(boards, active)
        ship_type = input("Ship type: ")
        rotation = input("ship rotation: ")
        positionx = int(input("ship x position: "))
        positiony = int(input("ship y position: "))
        position = (positionx, positiony)

        if boards.set_ship(active, ship_type, position, rotation):
            print(f"{boards.ships[active][-1].name} was placed")
        else:
            print("something went wrong, check pos")

    print("finished setting")

    while not(boards.is_defeated(0) or boards.is_defeated(1)):
        print(f"{boards.active_player}s turn")

        draw(boards, (boards.active_player+1)%2)
        
        positionx = int(input("ship x position: "))
        positiony = int(input("ship y position: "))
        position = (positionx, positiony)

        if boards.attack(boards.active_player, position):
            print("hit, again")
        else:
            print("miss")

    print("end:", boards.active_player, "won")


