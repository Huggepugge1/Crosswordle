import cell
import clue


ACROSS = 0
DOWN = 1


class Crossword:
    def __init__(self, 
                 title: str, 
                 author: str, 
                 copyright: str, 
                 version: str, 
                 width: int, 
                 height: int, 
                 solution: str, 
                 user_state: str, 
                 clues: list[str]):

        self.title = title
        self.author = author
        self.copyright = copyright
        self.version = version
        self.width = width
        self.height = height
        self.solution = solution
        
        self.clues = clue.assign_clues(clues, solution, width)

        self.cells = cell.make_cells_from_user_state(user_state, self.solution, self.width)


    def get_clues(self, pos = tuple[int, int]) -> tuple[clue.Clue, clue.Clue]:
        """
        Get a cells clues
        Returns a tuple (Clue, Clue) where the first clue is ACROSS and the second DOWN
        """
        clues = (None, None)
        for clue in self.clues:
            if clue.pos == pos:
                if clue.direction == ACROSS:
                    clues[ACROSS] = clue
                else:
                    clues[DOWN] = clue

        return clues

