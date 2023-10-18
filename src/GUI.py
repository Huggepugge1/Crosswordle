import pygame
import random
import string
import crossword_reader
import cell
from get_pos import get_pos
import textwrap


ACROSS = 0


class GUI_Cell:
    def __init__(self, rect, pos, cell):
        self.rect = rect
        self.pos = pos
        self.cell = cell
        self.color = "white"

    def change_color(self):
        if self.cell.solution == self.cell.content: 
            self.color = "green"
            return
        for word in self.cell.words:
            if self.cell.content != "" and self.cell.content in word: 
                self.color = "yellow"



def initialize_gui_cells(screen, screen_width, screen_height, crossword_width: int, crossword_height: int, cells: list[cell.Cell]) -> list[dict]: 
    padding_bottom = 200
    padding_top = 25

    gui_cell_size = (screen_height - padding_top - padding_bottom) // crossword_width
    
    padding_x = (screen_width - (gui_cell_size * crossword_width)) // 2
    
    gui_cells = []
    
    for row in range(crossword_height):
        for col in range(crossword_width):
            rect = pygame.Rect(col * gui_cell_size + padding_x, row * gui_cell_size + padding_top, gui_cell_size, gui_cell_size)
            pos = row * crossword_height + col
            gui_cells.append(GUI_Cell(rect, pos, cells[pos]))

    return gui_cells


def update_gui_cell(screen, screen_width, screen_height, crossword_width, gui_cell, selected_gui_cell, clues):
    if gui_cell.cell.content == ".":
        pygame.draw.rect(screen, "black", gui_cell.rect)
    
    elif gui_cell.pos == selected_gui_cell:
        pygame.draw.rect(screen, "light blue", gui_cell.rect)
        pygame.draw.rect(screen, "black", gui_cell.rect, 2)
    else:
        pygame.draw.rect(screen, gui_cell.color, gui_cell.rect)
        pygame.draw.rect(screen, "black", gui_cell.rect, 2)
        
    gui_cell_font_size = 25
    font = pygame.font.Font('freesansbold.ttf', gui_cell_font_size)
    gui_cell_content = font.render(gui_cell.cell.content, True, "black")
    gui_cell_content_rect = gui_cell_content.get_rect()
    gui_cell_content_rect.center = (gui_cell.rect.x + gui_cell.rect.width // 2, gui_cell.rect.y + gui_cell.rect.height // 2)
    screen.blit(gui_cell_content, gui_cell_content_rect)


    # Draw clues
    padding_bottom = 150
    
    # Remove old clues
    hider = pygame.Rect(0, screen_height - padding_bottom + 20, screen_width, padding_bottom - 20)
    pygame.draw.rect(screen, "white", hider)
    
    clue_number_font_size = 10
    clue_font_size = 20
    for clue in clues:
        clue_pos = clue.pos[0] * crossword_width + clue.pos[1]
        
        if clue_pos == gui_cell.pos:
            # Draw numbers
            font = pygame.font.Font('freesansbold.ttf', clue_number_font_size)
            gui_cell_content = font.render(str(clue.number), True, "black")
            gui_cell_content_rect = gui_cell_content.get_rect()
            gui_cell_content_rect.center = (gui_cell.rect.x + clue_number_font_size, gui_cell.rect.y + clue_number_font_size)
            screen.blit(gui_cell_content, gui_cell_content_rect)
        
        if clue_pos != selected_gui_cell:
            continue 
        
        # New clues
        text_wrapper = textwrap.TextWrapper(screen_width // 40)
        font = pygame.font.Font('freesansbold.ttf', clue_font_size)
        if selected_gui_cell == clue_pos:
            if clue.direction == ACROSS:
                # Draw across
                for row, string in enumerate(text_wrapper.wrap(clue.string)):
                    across_clue_text = font.render((f"{clue.number}. " * int(row == 0)) + string, True, "black")
                    across_clue_text_rect = across_clue_text.get_rect()
                    across_clue_text_rect.center = (screen_width // 3, screen_height - padding_bottom + 50 + row * clue_font_size)
                    screen.blit(across_clue_text, across_clue_text_rect)

            else:
                # Draw DOWN
                for row, string in enumerate(text_wrapper.wrap(clue.string)):
                    down_clue_text = font.render((f"{clue.number}. " * int(row == 0)) + string, True, "black")
                    down_clue_text_rect = down_clue_text.get_rect()
                    down_clue_text_rect.center = (screen_width // 3 * 2, screen_height - padding_bottom + 50 + row * clue_font_size)
                    screen.blit(down_clue_text, down_clue_text_rect)


def draw_crossword(screen, screen_width, screen_height, crossword_width, crossword_height, gui_cells, selected_gui_cell, clues):       
    screen.fill("white")
    padding_bottom = 150

    font = pygame.font.Font('freesansbold.ttf', 40)
    
    # Draw across
    across_text = font.render('ACROSS', True, "black")
    across_text_rect = across_text.get_rect()
    across_text_rect.center = (screen_width // 3, screen_height - padding_bottom)
    screen.blit(across_text, across_text_rect)

    # Draw DOWN
    down_text = font.render('DOWN', True, "black")
    down_text_rect = down_text.get_rect()
    down_text_rect.center = (screen_width // 3 * 2, screen_height - padding_bottom)
    screen.blit(down_text, down_text_rect)

    # Draw gui_cells
    gui_cell_font_size = 25
    font = pygame.font.Font('freesansbold.ttf', gui_cell_font_size)
    for gui_cell in gui_cells:
        if gui_cell.cell.content == ".":
            pygame.draw.rect(screen, "black", gui_cell.rect)
        
        elif gui_cell.pos == selected_gui_cell:
            pygame.draw.rect(screen, "light blue", gui_cell.rect)
            pygame.draw.rect(screen, "black", gui_cell.rect, 2)
        else:
            pygame.draw.rect(screen, gui_cell.color, gui_cell.rect)
            pygame.draw.rect(screen, "black", gui_cell.rect, 2)
        
        gui_cell_content = font.render(gui_cell.cell.content, True, "black")
        gui_cell_content_rect = gui_cell_content.get_rect()
        gui_cell_content_rect.center = (gui_cell.rect.x + gui_cell.rect.width // 2, gui_cell.rect.y + gui_cell.rect.height // 2)
        screen.blit(gui_cell_content, gui_cell_content_rect)
                
    # Draw clues
    clue_number_font_size = 10
    clue_font_size = 20
    for clue in clues:
        clue_pos = clue.pos[0] * crossword_width + clue.pos[1]
        gui_cell = gui_cells[clue_pos]
        
        # Draw numbers
        font = pygame.font.Font('freesansbold.ttf', clue_number_font_size)
        gui_cell_content = font.render(str(clue.number), True, "black")
        gui_cell_content_rect = gui_cell_content.get_rect()
        gui_cell_content_rect.center = (gui_cell.rect.x + clue_number_font_size, gui_cell.rect.y + clue_number_font_size)
        screen.blit(gui_cell_content, gui_cell_content_rect)

        # Draw clue
        font = pygame.font.Font('freesansbold.ttf', clue_font_size)
        if selected_gui_cell == clue_pos:
            if clue.direction == ACROSS:
                # Draw across
                across_clue_text = font.render(f"{clue.number}. {clue.string}", True, "black")
                across_clue_text_rect = across_clue_text.get_rect()
                across_clue_text_rect.center = (screen_width // 3, screen_height - padding_bottom + 50)
                screen.blit(across_clue_text, across_clue_text_rect)

            else:
                # Draw DOWN
                down_clue_text = font.render(f"{clue.number}. {clue.string}", True, "black")
                down_clue_text_rect = down_clue_text.get_rect()
                down_clue_text_rect.center = (screen_width // 3 * 2, screen_height - padding_bottom + 50)
                screen.blit(down_clue_text, down_clue_text_rect)
 

def main(crossword_width, crossword_height):
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_rect().width, screen.get_rect().height
    clock = pygame.time.Clock()
    
    crossword = crossword_reader.crossword_reader("../crosswords/1.puz")

    cells = crossword.cells
    gui_cells = initialize_gui_cells(screen, screen_width, screen_height, crossword_width, crossword_height, crossword.cells)
    clues = crossword.clues

    selected_gui_cell = 0
    draw_crossword(screen, screen_width, screen_height, crossword_width, crossword_height, gui_cells, selected_gui_cell, clues)
    pygame.display.flip()
    
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                last_selected_gui_cell = selected_gui_cell
                for gui_cell in gui_cells:
                    if gui_cell.rect.collidepoint(event.pos):
                        selected_gui_cell = gui_cell.pos
                
                gui_cell = gui_cells[last_selected_gui_cell]
                update_gui_cell(screen, screen_width, screen_height, crossword_width, gui_cell, selected_gui_cell, clues)
                gui_cell = gui_cells[selected_gui_cell]
                update_gui_cell(screen, screen_width, screen_height, crossword_width, gui_cell, selected_gui_cell, clues)
                pygame.display.flip()
                
            elif event.type == pygame.TEXTINPUT:
                gui_cells[selected_gui_cell].cell.content = event.text.upper() if gui_cells[selected_gui_cell].cell.content != "." else "."
                
                gui_cell = gui_cells[selected_gui_cell]
                selected_gui_cell += 1
                while gui_cells[selected_gui_cell].cell.content == ".":
                    selected_gui_cell += 1

                update_gui_cell(screen, screen_width, screen_height, crossword_width, gui_cell, selected_gui_cell, clues)
                pygame.display.flip()
                
                gui_cell = gui_cells[selected_gui_cell]
                update_gui_cell(screen, screen_width, screen_height, crossword_width, gui_cell, selected_gui_cell, clues)
                pygame.display.flip()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    for gui_cell in gui_cells:
                        gui_cell.change_color()
                        update_gui_cell(screen, screen_width, screen_height, crossword_width, gui_cell, selected_gui_cell, clues)
                        pygame.display.flip()
                
                elif event.key == pygame.K_TAB:
                    draw_crossword(screen, screen_width, screen_height, crossword_width, crossword_height, gui_cells, selected_gui_cell, clues)
                    pygame.display.flip()
                
                elif event.key == pygame.K_UP:
                    gui_cell = gui_cells[selected_gui_cell]
                    
                    top = max(selected_gui_cell - crossword_width, -1) == -1
                    if not top:
                        selected_gui_cell = selected_gui_cell - crossword_width
                    
                    while gui_cells[selected_gui_cell].cell.content == "." and not top:
                        selected_gui_cell = selected_gui_cell - crossword_width
                        top = max(selected_gui_cell - crossword_width, -1) == -1

                    update_gui_cell(screen, screen_width, screen_height, crossword_width, gui_cell, selected_gui_cell, clues)
                    pygame.display.flip()
                    
                    gui_cell = gui_cells[selected_gui_cell]
                    update_gui_cell(screen, screen_width, screen_height, crossword_width, gui_cell, selected_gui_cell, clues)
                    pygame.display.flip()
                
                elif event.key == pygame.K_DOWN:
                    gui_cell = gui_cells[selected_gui_cell]
                    crossword_size = crossword_width * crossword_height
                    
                    bottom = min(selected_gui_cell + crossword_width, crossword_size) == crossword_size
                    if not bottom:
                        selected_gui_cell = selected_gui_cell + crossword_width
                    bottom = min(selected_gui_cell + crossword_width, crossword_size) == crossword_size
                    
                    while gui_cells[selected_gui_cell].cell.content == "." and not bottom:
                        selected_gui_cell = selected_gui_cell + crossword_width
                        bottom = min(selected_gui_cell + crossword_width, crossword_size) == crossword_size

                    update_gui_cell(screen, screen_width, screen_height, crossword_width, gui_cell, selected_gui_cell, clues)
                    pygame.display.flip()
                    
                    gui_cell = gui_cells[selected_gui_cell]
                    update_gui_cell(screen, screen_width, screen_height, crossword_width, gui_cell, selected_gui_cell, clues)
                    pygame.display.flip()

                
                elif event.key == pygame.K_LEFT:
                    gui_cell = gui_cells[selected_gui_cell]
                    
                    top_left = selected_gui_cell == 0
                    if not top_left:
                        selected_gui_cell = selected_gui_cell - 1
                    
                    while gui_cells[selected_gui_cell].cell.content == "." and not top_left:
                        selected_gui_cell = selected_gui_cell - 1
                        top_left = selected_gui_cell == 0

                    update_gui_cell(screen, screen_width, screen_height, crossword_width, gui_cell, selected_gui_cell, clues)
                    pygame.display.flip()
                    
                    gui_cell = gui_cells[selected_gui_cell]
                    update_gui_cell(screen, screen_width, screen_height, crossword_width, gui_cell, selected_gui_cell, clues)
                    pygame.display.flip()
                
                elif event.key == pygame.K_RIGHT:
                    gui_cell = gui_cells[selected_gui_cell]
                    crossword_size = crossword_width * crossword_height
                    
                    bottom_right = selected_gui_cell == crossword_size - 1
                    if not bottom_right:
                        selected_gui_cell = selected_gui_cell + 1
                    bottom_right = selected_gui_cell == crossword_size - 1
                    
                    while gui_cells[selected_gui_cell].cell.content == "." and not top:
                        selected_gui_cell = selected_gui_cell + 1
                        bottom_right = selected_gui_cell == crossword_size - 1

                    update_gui_cell(screen, screen_width, screen_height, crossword_width, gui_cell, selected_gui_cell, clues)
                    pygame.display.flip()
                    
                    gui_cell = gui_cells[selected_gui_cell]
                    update_gui_cell(screen, screen_width, screen_height, crossword_width, gui_cell, selected_gui_cell, clues)
                    pygame.display.flip()


main(15, 15)

