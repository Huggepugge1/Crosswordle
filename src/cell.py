from get_pos import get_pos

class Cell:
    def __init__(self, position: tuple[int, int], is_writable: bool, words: tuple[str, str], current_content: str, solution: str):
        self.position = position
        self.is_writable = is_writable
        self.words = words
        self.current_content = current_content
        self.solution = solution


def make_cells_from_user_state(user_state: str, solution: str, width: int):
    cells = []
    pos_words = find_words(solution, width)
    

    for pos, cell in enumerate(user_state):
        x, y = get_pos(pos, width)
        if cell == "-":
            cells.append(Cell(position = (x, y), is_writable = True, words = get_words(pos, pos_words), current_content = "", solution = get_solution(pos, solution)))
        elif cell == ".":
            cells.append(Cell(position = (x, y), is_writable = False, words = get_words(pos, pos_words), current_content=".", solution = get_solution(pos, solution)))  
        else:
            cells.append(Cell(position = (x, y), is_writable = True, words = get_words(pos, pos_words), current_content = cell, solution = get_solution(pos, solution)))


def find_words(solution, width):
    pos_words = {}
    word = ""
    position = []

    # Find all horizontal words
    for pos, char in enumerate(solution):
        if char == ".":
            if word:
                pos_words[word] = position
            word, position = "", []
        else:
            word += char
            position.append(pos)
        
        if pos % width == width - 1:
            if word:
                pos_words[word] = position
            word, position = "", []

    # Find all vertical words
    for col in range(width):
        word = ""
        position = []
        for row in range(len(solution) // width):
            pos = row * width + col
            char = solution[pos]

            if char == ".":
                if word:
                    pos_words[word] = position
                word, position = "", []
            else:
                word += char
                position.append(pos)
        
        if word:
            pos_words[word] = position

    return pos_words


def get_words(pos, pos_words):
    word_1 = ""
    word_2 = ""
    for word in pos_words:
        if pos in pos_words[word]:
            if word_1 == "":
                word_1 = word
            else:
                word_2 = word
                break

    return word_1, word_2

    
def get_solution(pos, solution):
    return solution[pos]
