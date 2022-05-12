import logging
from pathlib import Path
from time import time
from typing import Tuple

import numpy as np
from PIL import Image
from colorama import Style, Fore

from source.type.color_type import ColorType
from source.type.window_type import WindowType

logging.basicConfig()
logger = logging.getLogger(__name__)


class BitmapScreenBuffer:
    def __init__(
            self,
            screen_size_x: int = 70,
            screen_size_y: int = 70
    ):
        self.bitmap_size = 7
        self.screen_size_x = screen_size_x
        self.screen_size_y = screen_size_y
        self.buffer = [" "] * (self.screen_size_x * self.screen_size_y)

        self.current_style = ColorType.White

        self.im = Image.new('RGB', (screen_size_x * self.bitmap_size, screen_size_y * self.bitmap_size))
        self.pixels = self.im.load()

        self.current_frame = 0

        self.path_save = Path(f"frames_{int(time())}")

        self.path_save.mkdir(exist_ok=True)

    def get_screen_offset(self, window: WindowType) -> int:
        offset = 0

        if window == WindowType.Base:
            offset = self.get_max_screen_height(window=WindowType.Tree)

        return offset

    def get_max_screen_height(self, window: WindowType) -> int:
        if window == WindowType.Base:
            return 4
        elif window == WindowType.Tree:
            return self.screen_size_y - 4

        return 0

    def get_max_screen_size(self, window: WindowType) -> Tuple:
        return self.screen_size_x, self.get_max_screen_height(window=window)

    def wattron(self, style: ColorType) -> None:
        self.current_style = style

    def wattroff(self) -> None:
        self.current_style = Style.RESET_ALL + Fore.RESET

    def get_bitmap(self, char: str) -> np.ndarray:
        if '&' in char:
            return np.array((
                (0, 1, 0, 0, 0, 0, 0),
                (0, 1, 1, 1, 1, 0, 0),
                (1, 1, 1, 1, 1, 1, 1),
                (1, 1, 1, 1, 1, 0, 0),
                (0, 1, 1, 1, 1, 1, 1),
                (0, 0, 0, 1, 1, 0, 1),
                (0, 0, 0, 0, 1, 0, 1)
            ))
        elif '|' in char:
            return np.array((
                (0, 0, 1, 1, 0, 0, 0),
                (0, 0, 0, 1, 1, 0, 0),
                (0, 0, 0, 1, 1, 0, 0),
                (0, 0, 1, 1, 0, 0, 0),
                (0, 0, 1, 1, 0, 0, 0),
                (0, 0, 1, 1, 0, 0, 0),
                (0, 1, 1, 1, 1, 1, 0)
            ))
        elif '/' in char:
            return np.array((
                (0, 0, 0, 0, 0, 1, 1),
                (0, 0, 0, 0, 1, 1, 0),
                (0, 0, 0, 1, 1, 0, 0),
                (0, 0, 1, 1, 0, 0, 0),
                (1, 1, 1, 0, 0, 0, 0),
                (1, 1, 0, 0, 0, 0, 0),
                (1, 1, 0, 0, 0, 0, 0)
            ))
        elif '\\' in char:
            return np.array((
                (1, 1, 0, 0, 0, 0, 0),
                (1, 1, 0, 0, 0, 0, 0),
                (0, 1, 1, 0, 0, 0, 0),
                (0, 0, 1, 1, 1, 0, 0),
                (0, 0, 0, 0, 1, 1, 1),
                (0, 0, 0, 0, 1, 1, 1),
                (0, 0, 0, 0, 1, 1, 1)
            ))
        elif '_' in char:
            return np.array((
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (1, 1, 1, 1, 1, 1, 1)
            ))
        elif '~' in char:
            return np.array((
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (0, 1, 0, 0, 0, 0, 0),
                (1, 0, 1, 0, 0, 0, 1),
                (1, 1, 0, 1, 0, 0, 1),
                (0, 0, 0, 0, 1, 1, 0),
                (0, 0, 0, 0, 0, 0, 0)
            ))
        elif '(' in char:
            return np.array((
                (0, 0, 0, 0, 1, 1, 1),
                (0, 0, 1, 1, 1, 0, 0),
                (0, 1, 1, 0, 0, 0, 0),
                (0, 1, 0, 0, 0, 0, 0),
                (0, 1, 0, 0, 0, 0, 0),
                (0, 0, 1, 1, 1, 0, 0),
                (0, 0, 0, 0, 1, 1, 1)
            ))
        elif ')' in char:
            return np.array((
                (1, 1, 1, 0, 0, 0, 0),
                (0, 0, 1, 1, 1, 0, 0),
                (0, 0, 0, 0, 1, 1, 0),
                (0, 0, 0, 0, 0, 1, 0),
                (0, 0, 0, 0, 0, 1, 0),
                (0, 0, 1, 1, 1, 0, 0),
                (1, 1, 1, 0, 0, 0, 0)
            ))
        elif ')' in char:
            return np.array((
                (1, 1, 1, 0, 0, 0, 0),
                (0, 0, 1, 1, 1, 0, 0),
                (0, 0, 0, 0, 1, 1, 0),
                (0, 0, 0, 0, 0, 1, 0),
                (0, 0, 0, 0, 0, 1, 0),
                (0, 0, 1, 1, 1, 0, 0),
                (1, 1, 1, 0, 0, 0, 0)
            ))
        elif '.' in char:
            return np.array((
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 1, 0, 0, 0),
                (0, 0, 1, 1, 1, 0, 0),
                (0, 0, 0, 1, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0)
            ))
        elif ' ' == char[0]:
            return np.array((
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0)
            ))

        logger.error(f"Unknown type {char}")

        return np.array((
            (0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0)
        ))

    def render_single_char(
            self,
            offset_x: int,
            offset_y: int,
            bitmap: np.ndarray
    ):
        for xx in range(self.bitmap_size):
            for yy in range(self.bitmap_size):
                if offset_x * self.bitmap_size + xx >= self.screen_size_x * self.bitmap_size:
                    logger.error(f"x exceeds screen width {offset_x} / {self.bitmap_size} ({self.screen_size_x})")
                    return

                if offset_y * self.bitmap_size + yy >= self.screen_size_y * self.bitmap_size:
                    logger.error(f"y ranges into base: {offset_y} >= ${self.screen_size_y}")
                    return

                color = [self.current_style.value[ii] * bitmap[yy, xx] for ii in range(3)]
                self.pixels[offset_x * self.bitmap_size + xx, offset_y * self.bitmap_size + yy] = tuple(color)

    def mvwprintw(
            self,
            window: WindowType,
            offset_y: int,
            offset_x: int,
            content: str
    ) -> None:
        if window == WindowType.Base:
            offset_x += (self.screen_size_x - len(content)) / 2

        y = int(self.get_screen_offset(window) + offset_y)

        for index, char in enumerate(content):
            x = int(offset_x + index)

            bitmap = self.get_bitmap(char=char)

            self.render_single_char(
                offset_x=x,
                offset_y=y,
                bitmap=bitmap
            )

    def screen_buffer_to_string(self) -> str:
        for it in range(1, self.screen_size_y - 1):
            self.buffer[it * self.screen_size_x] = '\n'

        self.im.save(self.path_save / f"frame_{self.current_frame:05d}.png")
        self.current_frame += 1

        return ''.join(self.buffer)
