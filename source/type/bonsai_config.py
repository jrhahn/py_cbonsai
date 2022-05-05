from dataclasses import dataclass
from typing import List


@dataclass
class BonsaiConfig:
    live: bool
    verbosity: int
    lifeStart: int
    multiplier: int
    leaves: List[str]
