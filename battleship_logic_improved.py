from typing import Literal

class Ship:
    """
    Tracks individual ships hitpoints and where it was hit.
    Whether it is still alive can be read from self.alive.
    Position always starts at the top left.
    Rotation can be entered using the size argument.
    Also supports non-regular rectangular shapes (e.g. 2x2).
    """
    def __init__(self, size: tuple, position: tuple, name: str) -> None:
        self.size = size
        self.position = position
        self.name = name
        self.alive = True
        self.destroyed_parts = []

    def on_ship(self, position: tuple) -> bool:
        return (self.position[0] <= position[0] < self.position[0] + self.size[0] and
                self.position[1] <= position[1] < self.position[1] + self.size[1])

    def hit(self, target: tuple) -> bool:
        if not self.alive:
            return False

        if self.on_ship(target):
            relative_pos = (target[0] - self.position[0], target[1] - self.position[1])
            if relative_pos not in self.destroyed_parts:
                self.destroyed_parts.append(relative_pos)
                if len(self.destroyed_parts) >= self.size[0] * self.size[1]:
                    self.alive = False
                return True
        return False

class Board:
    def __init__(self, size: tuple, starting_player: int = 0, ships: list = None, spacing: Literal["cornersok", "nocorners", "none"] = "cornersok"):
        self.active_player = starting_player
        self.size = size
        self.ship_selection = ships if ships else [(1, 5), (1, 4), (1, 3), (1, 3), (1, 2)]
        self.spacing = spacing
        self.ship_templates = {"carrier": 5, "battleship": 4, "destroyer": 3, "submarine": 3, "boat": 2}
        self.ships = [[], []]
        self.unused_ships = [self.ship_selection.copy(), self.ship_selection.copy()]

    def _is_valid_position(self, player: int, ship_size: tuple, position: tuple) -> bool:
        if not (0 <= position[0] < self.size[0] and 0 <= position[1] < self.size[1]):
            return False
        if not (position[0] + ship_size[0] <= self.size[0] and position[1] + ship_size[1] <= self.size[1]):
            return False

        notspace = 1 if self.spacing == "cornersok" else 0

        for ship in self.ships[player]:
            if (ship.position[0] - ship_size[0] + notspace <= position[0] <= ship.position[0] + ship.size[0] - notspace and
                ship.position[1] - ship_size[1] + notspace <= position[1] <= ship.position[1] + ship.size[1] - notspace):
                return False
        return True

    def _set_ship(self, player: int, ship_size: tuple | int, position: tuple, rotation: Literal["v", "h"] = None, name: str = None) -> bool:
        if player not in range(len(self.ships)):
            return False
        if isinstance(ship_size, int):
            if not rotation:
                return False
            ship_size = (1, ship_size) if rotation == "v" else (ship_size, 1)

        if not self._is_valid_position(player, ship_size, position):
            return False

        if ship_size in self.unused_ships[player]:
            self.unused_ships[player].remove(ship_size)
        elif ship_size[::-1] in self.unused_ships[player]:
            self.unused_ships[player].remove(ship_size[::-1])
        else:
            return False

        if not name:
            name = f"battleship_{len(self.ships[player])}"
        self.ships[player].append(Ship(ship_size, position, name))
        return True

    def set_ship(self, player: int, ship: str, position: tuple, rotation: Literal["v", "h"], name: str = None) -> bool:
        if ship not in self.ship_templates:
            return False
        return self._set_ship(player, self.ship_templates[ship], position, rotation, name)

    def attack(self, player: int, position: tuple) -> bool:
        if player != self.active_player:
            return False

        opponent = (player + 1) % len(self.ships)
        for ship in self.ships[opponent]:
            if ship.hit(position):
                return True

        self.active_player = opponent
        return False

    def is_defeated(self, player: int) -> bool:
        return all(not ship.alive for ship in self.ships[player])

def draw(board, player, show=True):
    canvas = [[" "]]
    for i in range(board.size[0]):
        canvas[0].append(f" {i} ")
    for y in range(board.size[1]):
        line = [str(y)]
        for x in range(board.size[0]):
            for ship in board.ships[player]:
                if ship.on_ship((x, y)):
                    if (x - ship.position[0], y - ship.position[1]) in ship.destroyed_parts:
                        line.append(" □ ")
                    else:
                        line.append(" ▣ " if show else " . ")
                    break
            else:
                line.append(" . ")
        canvas.append(line)

    for line in canvas:
        print("".join(line))

if __name__ == "__main__":
    boards = Board((10, 10))

    while True:
        if len(boards.unused_ships[0]) > 0:
            active = 0
        elif len(boards.unused_ships[1]) > 0:
            active = 1
        else:
            print("Finished setting ships.")
            break

        draw(boards, active, True)
        ship_type = input("Ship type: ").strip().lower()
        rotation = input("Ship rotation (v/h): ").strip().lower()
        try:
            positionx = int(input("Ship x position: ").strip())
            positiony = int(input("Ship y position: ").strip())
            position = (positionx, positiony)
        except ValueError:
            print("Invalid input. Please enter numeric values for positions.")
            continue

        if boards.set_ship(active, ship_type, position, rotation):
            print(f"{boards.ships[active][-1].name} was placed.")
        else:
            print("Invalid position or ship type. Please try again.")

    print("Finished setting ships.")

    while not boards.is_defeated(0) and not boards.is_defeated(1):
        print(f"Player {boards.active_player}'s turn.")
        draw(boards, (boards.active_player + 1) % 2, False)

        try:
            positionx = int(input("Attack x position: ").strip())
            positiony = int(input("Attack y position: ").strip())
            position = (positionx, positiony)
        except ValueError:
            print("Invalid input. Please enter numeric values for positions.")
            continue

        if boards.attack(boards.active_player, position):
            print("Hit! Attack again.")
        else:
            print("Miss. Next player's turn.")

    winner = (boards.active_player + 1) % 2
    print(f"Player {winner} wins!")
