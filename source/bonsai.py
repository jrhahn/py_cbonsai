import logging
import random
import time
from typing import Tuple

# from source import random
from source.bitmap_screen_buffer import BitmapScreenBuffer
from source.counters import Counters
from source.screen_buffer import ScreenBuffer
from source.type.bonsai_config import BonsaiConfig
from source.type.branch_type import BranchType
from source.type.color_type import ColorType
from source.type.window_type import WindowType
from source.utils import roll

logger = logging.getLogger(__name__)


class Bonsai:
    def __init__(self):
        self.screen_buffer = BitmapScreenBuffer()
        self.draw_base()

    def draw_base(self):
        self.screen_buffer.wattron(style=ColorType.Green)
        self.screen_buffer.wattron(style=ColorType.BrightGreen)
        self.screen_buffer.mvwprintw(WindowType.Base, offset_y=0, offset_x=-9, content="___________")
        self.screen_buffer.wattron(style=ColorType.Yellow)  # 11
        self.screen_buffer.mvwprintw(WindowType.Base, offset_y=0, offset_x=0, content="./~~~\\.")
        self.screen_buffer.wattron(style=ColorType.BrightGreen)  # 2
        self.screen_buffer.mvwprintw(WindowType.Base, offset_y=0, offset_x=9, content="___________")
        self.screen_buffer.wattron(style=ColorType.White)  # 8

        self.screen_buffer.mvwprintw(WindowType.Base, 1, 0, content=" \\                           / ")
        self.screen_buffer.mvwprintw(WindowType.Base, 2, 0, content=" \\_________________________/ ")
        self.screen_buffer.mvwprintw(WindowType.Base, 3, 0, content="(_)                   (_)")

        self.screen_buffer.wattroff()

    last_time = 0

    @staticmethod
    def update_screen(time_step: float) -> None:
        current_time = time.time()

        if Bonsai.last_time + time_step > current_time:
            # fixme updater window
            Bonsai.last_time = current_time

    # based on type of tree, determine what color a branch should be
    def choose_color(
            self,
            branch_type: BranchType
    ) -> None:
        if branch_type in (BranchType.Trunk, BranchType.ShootLeft, BranchType.ShootRight):
            if random.randint(0, 1) == 0:
                self.screen_buffer.wattron(ColorType.Yellow)  # 11
            else:
                self.screen_buffer.wattron(ColorType.Brown)  # 3

        elif branch_type == BranchType.Dying:
            if random.randint(0, 9) == 0:
                self.screen_buffer.wattron(ColorType.BrightGreen)  # 2 #bold
            else:
                self.screen_buffer.wattron(ColorType.BrightGreen)  # 2

        elif branch_type == BranchType.Dead:
            if random.randint(0, 2) == 0:
                self.screen_buffer.wattron(ColorType.Green)  # 10 bold
            else:
                self.screen_buffer.wattron(ColorType.Green)  # 10

        else:
            self.screen_buffer.wattron(ColorType.Green)

    # determine change in X and Y coordinates of a given branch
    @staticmethod
    def set_deltas(
            branch_type: BranchType,
            life: int,
            age: int,
            multiplier: int
    ) -> Tuple[int, int]:
        dx = 0
        dy = 0
        if branch_type == BranchType.Trunk:
            # new or dead trunk
            if age <= 2 or life < 4:
                dy = 0
                dx = random.randint(0, 2) - 1

            # young trunk should grow wide
            elif age < (multiplier * 3):
                # every (multiplier * 0.8) steps, raise tree to next level
                dx = 0
                dy = 0

                if age % int(multiplier // 2) == 0:
                    dy = -1

                rr = roll(10)
                if rr == 0:
                    dx = -2
                elif 1 <= rr <= 3:
                    dx = -1
                elif 4 <= rr <= 5:
                    dx = 0
                elif 6 <= rr <= 8:
                    dx = 1
                elif 9 == rr:
                    dx = 2

            # middle-aged trunk
            else:
                rr = roll(10)
                dy = -1 if rr > 2 else 0
                dx = random.randint(0, 2) - 1

        elif branch_type == BranchType.ShootLeft:
            # trend left and little vertical movement
            rr = roll(10)

            if 0 <= rr <= 1:
                dy = -1
            elif 2 <= rr <= 7:
                dy = 0
            elif 8 <= rr <= 9:
                dy = 1

            dx = 0
            rr = roll(10)

            if 0 <= rr <= 1:
                dx = -2
            elif 2 <= rr <= 5:
                dx = -1
            elif 6 <= rr <= 8:
                dx = 0
            elif 9 <= rr <= 9:
                dx = 1

        elif branch_type == BranchType.ShootRight:
            # right shoot: trend right and little vertical movement

            dy = 0
            rr = roll(10)

            if 0 <= rr <= 1:
                dy = -1
            elif 2 <= rr <= 7:
                dy = 0
            elif 8 <= rr <= 9:
                dy = 1

            dx = 0
            rr = roll(10)

            if 0 <= rr <= 1:
                dx = 2
            elif 2 <= rr <= 5:
                dx = 1
            elif 6 <= rr <= 8:
                dx = 0
            elif rr == 9:
                dx = -1

        elif branch_type == BranchType.Dying:
            # dying: discourage vertical growth(?); trend left/right (-3,3)
            dy = 0
            rr = roll(10)

            if 0 <= rr <= 1:
                dy = -1
            elif 2 <= rr <= 8:
                dy = 0
            elif 9 <= rr <= 9:
                dy = 1

            dx = 0
            rr = roll(15)

            if 0 <= rr <= 0:
                dx = -3
            elif 1 <= rr <= 2:
                dx = -2
            elif 3 <= rr <= 5:
                dx = -1
            elif 6 <= rr <= 8:
                dx = 0
            elif 9 <= rr <= 11:
                dx = 1
            elif 12 <= rr <= 13:
                dx = 2
            elif rr == 14:
                dx = 3

        elif branch_type == BranchType.Dead:
            # dead: fill in surrounding area
            dy = 0
            rr = roll(10)

            if 0 <= rr <= 2:
                dy = -1
            elif 3 <= rr <= 6:
                dy = 0
            elif 7 <= rr <= 9:
                dy = 1

            dx = random.randint(0, 2) - 1

        if dx == 0:
            print()

        return dx, dy

    @staticmethod
    def choose_string(
            conf: BonsaiConfig,
            branch_type: BranchType,
            life: int,
            dx: int,
            dy: int
    ) -> str:
        if life < 4:
            branch_type = BranchType.Dying

        pattern = "?"
        if branch_type == BranchType.Trunk:
            if dy == 0:
                pattern = "/~"
            elif dx < 0:
                pattern = "\\|"
            elif dx == 0:
                pattern = "/|\\"
            elif dx > 0:
                pattern = "|/"

        elif branch_type == BranchType.ShootLeft:
            if dy > 0:
                pattern = "\\"
            elif dy == 0:
                pattern = "\\_"
            elif dx < 0:
                pattern = "\\|"
            elif dx == 0:
                pattern = "/|"
            elif dx > 0:
                pattern = "/"

        elif branch_type == BranchType.ShootRight:
            if dy > 0:
                pattern = "/"
            elif dy == 0:
                pattern = "_/"
            elif dx < 0:
                pattern = "\\|"
            elif dx == 0:
                pattern = "/|"
            elif dx > 0:
                pattern = "/"

        elif branch_type == BranchType.Dying or branch_type == BranchType.Dead:
            rnd_index = random.randint(0, len(conf.leaves) - 1)

            if rnd_index >= len(conf.leaves):
                raise ValueError(f"index {rnd_index} out of bounds: {len(conf.leaves)}")

            pattern = str(conf.leaves[rnd_index])

        return pattern

    def branch(
            self,
            conf: BonsaiConfig,
            counters: Counters,
            y: int,
            x: int,
            branch_type: BranchType,
            life: int
    ):
        counters.branches += 1
        shoot_cooldown = conf.multiplier

        while life > 0:
            print(f"life: {life}")
            life -= 1  # decrement remaining life counter

            dx, dy = self.set_deltas(
                branch_type=branch_type,
                life=life,
                age=conf.lifeStart - life,
                multiplier=conf.multiplier
            )

            max_y = self.screen_buffer.get_max_screen_height(WindowType.Tree)

            if dy > 0 and y > (max_y - 2):
                dy -= 1

            # near-dead branch should branch into a lot of leaves
            if life < 3:
                self.branch(
                    conf=conf,
                    counters=counters,
                    y=y,
                    x=x,
                    branch_type=BranchType.Dead,
                    life=life
                )

            # dying trunk should branch into a lot of leaves
            elif branch_type == BranchType.Trunk and life < (conf.multiplier + 2):
                self.branch(
                    conf=conf,
                    counters=counters,
                    y=y,
                    x=x,
                    branch_type=BranchType.Dying,
                    life=life
                )

            # dying shoot should branch into a lot of leaves
            elif (branch_type == BranchType.ShootLeft or branch_type == BranchType.ShootRight) \
                    and life < (conf.multiplier + 2):
                self.branch(
                    conf=conf,
                    counters=counters,
                    y=y,
                    x=x,
                    branch_type=BranchType.Dying,
                    life=life
                )

            # trunks should re-branch if not close to ground AND either randomly, or upon every <multiplier> steps
            elif branch_type == BranchType.Trunk and (random.randint(0, 2) == 0 or (life % int(conf.multiplier) == 0)):
                # if trunk is branching and not about to die, create another trunk with random life
                if (random.randint(0, 7) == 0) and life > 7:
                    shoot_cooldown = conf.multiplier * 2  # reset shoot cooldown
                    self.branch(
                        conf=conf,
                        counters=counters,
                        y=y,
                        x=x,
                        branch_type=BranchType.Trunk,
                        life=life + (random.randint(0, 4) - 2)
                    )

                # otherwise create a shoot
                elif shoot_cooldown <= 0:
                    shoot_cooldown = conf.multiplier * 2  # reset shoot cooldown

                    shoot_life = life + conf.multiplier

                    # first shoot is randomly directed
                    counters.shoots += 1
                    counters.shootCounter += 1

                    # create shoot
                    shoot_type = BranchType.ShootRight

                    if (counters.shootCounter % 2) + 1 == 1:
                        shoot_type = BranchType.ShootLeft

                    self.branch(
                        conf=conf,
                        counters=counters,
                        y=y,
                        x=x,
                        branch_type=shoot_type,
                        life=shoot_life
                    )

            shoot_cooldown -= 1

            # move in x and y directions
            x += dx
            y += dy

            # choose string to use for this branch
            branch_str = self.choose_string(
                conf=conf,
                branch_type=branch_type,
                life=life,
                dx=dx,
                dy=dy
            )

            self.choose_color(
                branch_type=branch_type
            )

            self.screen_buffer.mvwprintw(WindowType.Tree, y, x, branch_str)

            self.screen_buffer.wattroff()

            self.screen_buffer.screen_buffer_to_string()

    def grow_tree(
            self,
            conf: BonsaiConfig,
            counters: Counters
    ):
        max_x, max_y = self.screen_buffer.get_max_screen_size(WindowType.Tree)

        # reset counters
        counters.shoots = 0
        counters.branches = 0
        counters.shootCounter = random.randint(0, 10000)

        if conf.verbosity > 0:
            self.screen_buffer.mvwprintw(WindowType.Tree, 2, 5, "maxX: $maxX, maxY: $maxY")

        # recursively grow tree trunk and branches
        self.branch(
            conf=conf,
            counters=counters,
            y=max_y - 1,
            x=max_x / 2,
            branch_type=BranchType.Trunk,
            life=conf.lifeStart
        )

    def run(self) -> str:
        conf = BonsaiConfig(
            live=False,
            verbosity=0,
            lifeStart=32,
            multiplier=5,
            leaves=[],
        )

        conf.leaves = '&'

        counters = Counters(
            branches=0,
            shoots=0,
            shootCounter=0
        )

        counter = 0
        max_iterations = 1
        while counter < max_iterations:
            self.grow_tree(conf, counters)

            counter += 1

        return self.screen_buffer.screen_buffer_to_string()
