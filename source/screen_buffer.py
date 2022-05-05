import logging
from typing import Tuple

from colorama import Style, Fore

from source.color import colored
from source.type.color_type import ColorType
from source.type.window_type import WindowType

logger = logging.getLogger(__name__)


class ScreenBuffer:
    def __init__(
            self,
            screen_size_x: int = 139,
            screen_size_y: int = 30
    ):
        self.screen_size_x = screen_size_x
        self.screen_size_y = screen_size_y
        self.buffer = [" "] * (self.screen_size_x * self.screen_size_y)

        self.current_style = ColorType.White

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

    def mvwprintw(
            self,
            window: WindowType,
            offset_y: int,
            offset_x: int,
            content: str
    ) -> None:
        if offset_x + len(content) >= self.screen_size_x:
            logger.error(f"x exceeds screen width {offset_x} ({self.screen_size_x}")
            return

        if offset_y >= self.get_max_screen_height(window):
            logger.error(f"y ranges into base: {offset_y} >= ${self.get_max_screen_height(window)}")
            return

        offset = (self.get_screen_offset(window) + offset_y) * self.screen_size_x + offset_x

        if window == WindowType.Base:
            offset = (self.get_screen_offset(window) + offset_y) * self.screen_size_x + offset_x + (
                    self.screen_size_x - len(content)) / 2

        if (offset + len(content) >= self.screen_size_x * self.screen_size_y) or (offset < 0):
            logger.error(
                "message exceeds screen buffer: ${offset + content.length} > ${screenSizeX * screenSizeY}"
            )

        for index, char in enumerate(content):
            self.buffer[int(offset + index)] = colored(
                text=content[index],
                color_type=self.current_style
            )

    def screen_buffer_to_string(self) -> str:
        for it in range(1, self.screen_size_y - 1):
            self.buffer[it * self.screen_size_x] = '\n'

        return ''.join(self.buffer)
