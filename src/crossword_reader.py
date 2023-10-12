import crossword


def read_string(file):
    string = b""
    while (char := file.read(1)) != b"\x00":
        string += char

    return string


def crossword_reader(file_path: str):
    clues = []
    with open(file_path, "rb") as puzzle_file:
        checksum   = puzzle_file.read(0x02)
        file_magic = puzzle_file.read(0x0C)
        
        CIB_checksum         = puzzle_file.read(0x02)
        masked_low_checksum  = puzzle_file.read(0x04)
        masked_high_checksum = puzzle_file.read(0x04)

        version  = puzzle_file.read(0x04).decode("ISO-8859-1")
        reserved = puzzle_file.read(0x02)

        scrambled_checksum = puzzle_file.read(0x02)

        unknown = puzzle_file.read(0x2C - 0x20)

        width           = puzzle_file.read(0x01)
        height          = puzzle_file.read(0x01)
        number_of_clues = puzzle_file.read(0x02)

        bitmask         = puzzle_file.read(0x02)
        scrambled_tag   = puzzle_file.read(0x02)

        width = int.from_bytes(width)
        height = int.from_bytes(height)

        crossword_size = width * height

        solution   = puzzle_file.read(crossword_size).decode("ISO-8859-1")
        user_state = puzzle_file.read(crossword_size).decode("ISO-8859-1")

        title     = read_string(puzzle_file).decode("ISO-8859-1")
        author    = read_string(puzzle_file).decode("ISO-8859-1")
        copyright = read_string(puzzle_file).decode("ISO-8859-1")

        clues = []
        for _ in range(int.from_bytes(number_of_clues, "little")):
            current_clue = read_string(puzzle_file).decode("ISO-8859-1")
            clues.append(current_clue)

        return crossword.Crossword(title, author, copyright, version, width, height, solution, user_state, clues)
