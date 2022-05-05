from source.type.color_type import ColorType


def colored(
        text: str,
        color_type: ColorType
) -> str:
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(
        color_type.value[0],
        color_type.value[1],
        color_type.value[2],
        text
    )
