"""
## BATTLESHIPS ##
"""

from typing import Literal


class Ship:
    """
    defines one Ship which 
        - can be placed at any point
        - can assume any given rectangular shape
        - tracks its own health
        - using the name attribute it can be customized by the user
    """
    def __init__(self, size: tuple[int, int], position: tuple[int, int], name: str, destroyed_parts: list=None) -> None:
        """
        parameters:
            size: tuple[int, int] -- (x_size, y_size) of ship
            position: tuple[int, int] -- (x_pos, y_pos) of the top and left most part of the ship (head)
            name: str -- name of the ship
        """
        self.size = size
        self.position = position
        self.name = name
        self.alive = True

        if not destroyed_parts:
            self.destroyedParts = list()    # stores destroyed parts of ship relative to ship head(self.position)
                                            # might be better to change to absolute, depending on GUI interfacing
        else:
            self.destroyedParts = destroyed_parts

    def on_ship(self, probe_position: tuple[int, int]) -> bool:
        """
        returns true if given position intersects with the ship

        parameters:
            probe_position: tuple[int, int] -- (x_pos, y_pos) to test
        
        Returns:
            -> bool -- if probe_position on ship
        """
        if (self.position[0] <= probe_position[0] <= self.position[0] + self.size[0] - 1
        and self.position[1] <= probe_position[1] <= self.position[1] + self.size[1] - 1):
            return True
        else:
            return False

    def hit(self, target: tuple[int, int]) -> bool:
        """
        checks if the ship is hit by a missile hitting the target position
        if so the hit is executed

        parameters:
            target: tuple[int, int] -- (x_pos, y_pos) of the target position

        Returns
            -> bool -- if an alive part of the ship was hit
        
        """
        # if the ship was already sunk, it cannot be hit again
        if not self.alive:
            return False
        
        # is target on ship
        if self.on_ship(target):
            # pos needs to be calculated to fit relative coords of destroyedParts
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
    def __init__(self, size: tuple[int, int], starting_player: int=0, ships: list[tuple[int, int]]=None, spacing: Literal["cornersok", "nocorners", "none"]="cornersok") -> None:
        """
        parameters:
            size: tuple[int, int] -- (x_size, y_size) of board
            starting_player: int = 0 -- number of starting player
            ships: list[tuple[int, int]] = None -- selection of ships for the game
            spacing: Literal["cornersok", "nocorners", "none"] = "cornersok" -- refers to the space between ships
        """
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

        # (unused) ships for each player
        self.ships = [list(), list()]
        self.unused_ships = [self.ship_selection[::], self.ship_selection[::]]

        self.misses = [list(), list()]   # misses ON specific board

    def _is_valid_position(self, player: int, ship_size: tuple[int, int], position: tuple[int, int]) -> bool:
        """
        checks if the desired position and ship size can be placed on the board

        parameters:
            player: int -- number of the placing player
            ship_size: tuple[int, int] -- (x_size, y_size) of the ship
            position: tuple[int, int] -- (x_pos, y_pos) of the ship

        Returns:
            -> bool -- if ship placement is valid
        """
        # position not on board
        if not (0 <= position[0] <= self.size[0] and 0 <= position[1] <= self.size[1]):
            return False
        
        # ship to big to fit on board
        if not (position[0] + ship_size[0] <= self.size[0] and position[1] + ship_size[1] <= self.size[1]):
            return False
        
        # overlap to other ships
        if self.spacing == "nocorners":
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

    def _set_ship(self, player: int, ship_size: tuple[int, int] | int, position: tuple[int, int], rotation: Literal["v", "h"]=None, name: str=None) -> bool:
        """
        sets ship of ship_size on position with rotation on board of player

        parameters:
            player: int -- number of the placing player
            ship_size: tuple[int, int] | int -- (x_size, y_size) of the ship; if only int is given it is converted
            position: tuple[int, int] -- (x_pos, y_pos) of the ship
            rotation: Literal["v", "h"] = None -- needed when type(ship_size) == int, otherwise ignored
            name: str = None -- name of the ship

        Returns:
            -> bool -- if placing was successful
        """
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
        elif (_ship_size := ship_size[::-1]) in self.unused_ships[player]:  # unused_ships are assumed to be rotatable
            self.unused_ships[player].remove(_ship_size)
        else:
            return False
        
        # no name given: generate iterative one
        if not name:
            name = f"battleship_{len(self.ships[player])}"

        self.ships[player].append(Ship(ship_size, position, name))

        return True

    def set_ship(self, player: int, ship: str, position: tuple[int, int], rotation: Literal["v", "h"], name: str=None) -> bool:
        """
        conversion of specific ship key names to usable values

        parameters:
            player: int -- number of the placing player
            ship: str -- key name of ship size
            position: tuple[int, int] -- (x_pos, y_pos) of the ship
            rotation: Literal["v", "h"] -- sets rotation of ship
            name: str = None -- name of the ship

        Returns:
            -> bool -- if placing was successful
        """
        if ship not in self.ship_templates.keys():
            return False
        
        return self._set_ship(player=player, ship_size=self.ship_templates[ship], position=position, rotation=rotation, name=name)

    def attack(self, player: int, position: tuple[int, int]) -> bool:
        """
        attacks position on board of opponent

        parameters:
            player: int -- number of the placing player
            position: tuple[int, int] -- (x_pos, y_pos) of the target

        Returns:
            -> bool -- True if ship was hit; False if something went wrong or miss
        """
        # player id is incorrect
        if player != self.active_player:
            return False
        
        # if ship of other player is hit
        for ship in self.ships[(player+1)%len(self.ships)]:
            if ship.hit(position):
                return True
        
        self.active_player = (player+1)%len(self.ships)   # switch player

        self.misses.append(position)

        return False
    
    def is_defeated(self, player: int) -> bool:
        """
        parameters:
            player: int -- player number
        
        Returns:
            -> bool -- if player is defeated
        """
        # player id is out of range
        if player not in range(0, len(self.ships)):
            return False
        
        # check if at least one ship is still alive
        for ship in self.ships[player]:
            if ship.alive:
                return False
        return True
    
    def import_game(self, data: list) -> None:
        self.ships = [list() for _ in range(len(data))]
        self.misses = [list() for _ in range(len(data))]
        for board_data in range(len(data)):
            for ship in data[board_data].keys()[:-1]:
                ship_data = data[board_data][ship]
                self.ships[board_data].append(Ship(size=tuple(ship_data["size"]), position=tuple(ship_data["position"]), name=ship, destroyed_parts=ship_data["destroyedParts"]))
            self.misses[board_data] = data[board_data]["miss"]
                                              
    
def draw(board: Board, player: int, show: bool = True) -> None:
    """
    temporary drawing function for testing
    
    parameters:
        board: Board -- board class the game is played on
        player: int -- this player's board is displayed
        show: bool = True -- if unhit parts of a ship are displayed
    """
    canvas = [[" "]]
    # first line of indexes
    for i in range(0, board.size[0]):
        canvas[0].append(" " + str(i) + " ")
    
    # for each position check if ships is on it
    for y in range(board.size[1]):
        line = [str(y)]
        for x in range(board.size[0]):
            for ship in board.ships[player]:
                # if ship is on position, draw then break loop since there can only be one ship
                if ship.on_ship((x, y)):
                    # how to display ship depending on alive / shown
                    if (x-ship.position[0], y-ship.position[1]) in ship.destroyedParts:
                        line.append(" □ ")
                    else:
                        if show:
                            line.append(" ▣ ")
                        else:
                            line.append(" . ")
                    break
            # if the for loop was not broken out of (=> no ship found for position)
            else:
                line.append(" . ")
        canvas.append(line)

    # actually print whole board
    for line in canvas:
        print("".join(line))
            

if "__main__" == __name__:
    boards = Board((10, 10))    # declare Board with given size

    """
    "carrier": 5,
    "battleship": 4,
    "destroyer": 3,
    "submarine": 3,
    "boat": 2
    """

    # setting
    while True:
        # if both players have finished setting -> break
        if len(boards.unused_ships[0]) > 0:
            active = 0
        elif len(boards.unused_ships[1]) > 0:
            active = 1
        else:
            print("finished setting")
            break
        
        # draw and ask for input
        draw(boards, active, True)
        ship_type = input("Ship type: ")
        rotation = input("ship rotation: ")
        positionx = int(input("ship x position: "))
        positiony = int(input("ship y position: "))
        position = (positionx, positiony)

        # try to set for given ship
        if boards.set_ship(active, ship_type, position, rotation):
            print(f"{boards.ships[active][-1].name} was placed")
        else:
            print("something went wrong, check pos")

    print("finished setting")

    # attacking while nobody has been defeated
    while not(boards.is_defeated(0) or boards.is_defeated(1)):
        print(f"{boards.active_player}s turn")

        # draw and ask for input
        draw(boards, (boards.active_player+1)%2, False)
        positionx = int(input("ship x position: "))
        positiony = int(input("ship y position: "))
        position = (positionx, positiony)

        # try to attack given position
        if boards.attack(boards.active_player, position):
            print("hit, again")
        else:
            print("miss")

    print("end:", boards.active_player, "won")


