from get_pos import get_pos


ACROSS = 0
DOWN = 1


class Clue:
    def __init__(self, string: str, direction: int, pos: tuple[int, int], number: int):
        self.string = string
        self.direction = direction
        self.pos = pos
        self.number = number


    def __repr__(self):
        return f"<Clue: string: {self.string}, direction: {'DOWN' if self.direction else 'ACROSS'}, pos: {self.pos}, number: {self.number}>"


def assign_clues(clue_strings: list[str], solution: str, width: int) -> list[Clue]:
    clues = []
    current_clue_number = 1
    blank_cells = []
    
    for pos, cell in enumerate(solution):
        if cell == ".":
            blank_cells.append(get_pos(pos, width))
    
    for pos, cell in enumerate(solution):
        print(pos, clues)
        clue_assigned = False
        x, y = get_pos(pos, width)
        if cell != "." and (x == 0 or solution[pos - 1] == "."):
            clues.append(Clue(clue_strings.pop(0), ACROSS, pos = (x, y), number = current_clue_number))
            clue_assigned = True

        if cell != "." and (y == 0 or (pos >= width and solution[pos - width] == ".")):
            clues.append(Clue(clue_strings.pop(0), DOWN, pos = (x, y), number = current_clue_number))
            clue_assigned = True

        current_clue_number += clue_assigned
        
    print(clues)

