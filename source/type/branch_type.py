from enum import Enum


class BranchType(Enum):
    Trunk = "Trunk"
    ShootLeft = "ShootLeft"
    ShootRight = "ShootRight"
    Dying = "Dying"
    Dead = "Dead"