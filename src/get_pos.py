def get_pos(pos: int, width: int) -> tuple[int, int]:
    x = pos // width
    y = pos % width
    return (x, y)

