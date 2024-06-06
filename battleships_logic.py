"""
## BATTLESHIPS ##

Board class implements functions for board

Ship class with
 - ship size
 - position
 - (name, ..)



"""


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
                if len(self.destroyedParts) == self.size[0] * self.size[1]:
                    self.alive = False
                return True
        else:
            return False
