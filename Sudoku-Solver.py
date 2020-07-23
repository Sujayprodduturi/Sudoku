import pygame
pygame.init()


def valid(board, num, pos):
    # Row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    # Col
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    # Sub grid
    subcube_x = pos[1] // 3
    subcube_y = pos[0] // 3

    for i in range(subcube_y * 3, subcube_y * 3 + 3):
        for j in range(subcube_x * 3, subcube_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True


def empty_cube(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None


def solution(board):
    empty = empty_cube(board)
    if not empty:
        return True
    else:
        row, col = empty

        for i in range(1, 10):
            if valid(board, i, (row, col)):
                board[row][col] = i

                if solution(board):
                    return True

                board[row][col] = 0

        return False


# Grid
class Grid:
    board = [
        [5, 0, 9, 0, 6, 0, 0, 0, 7],
        [0, 0, 0, 0, 7, 0, 0, 1, 3],
        [0, 0, 0, 1, 0, 5, 0, 0, 9],
        [4, 0, 0, 0, 8, 0, 0, 2, 1],
        [1, 0, 0, 0, 2, 3, 6, 0, 5],
        [9, 3, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 6, 5, 1, 9, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 6, 0, 0, 0, 7, 8, 0, 0]
    ]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.selected = None
        self.model = None
        self.new_model()
        self.win = win

    def new_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def perm_val(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_val(val)
            self.new_model()
            if valid(self.model, val, (row, col)) and solution(self.model):
                return True
            else:
                self.cubes[row][col].set_val(0)
                self.cubes[row][col].set_temp(0)

                self.new_model()
                return False

    def temp_value(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        size = self.width/9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(win, (0, 0, 0), (0, i*size), (self.width, i*size), thickness)
            pygame.draw.line(win, (0, 0, 0), (i*size, 0), (i*size, self.height), thickness)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            size = self.width / 9
            x = pos[0]//size
            y = pos[1]//size
            return(int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def back_track_solution(self):
        self.new_model()
        empty = empty_cube(self.model)
        if not empty:
            return True
        else:
            row, col = empty

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set_val(i)
                self.cubes[row][col].draw_update(self.win, True)
                self.new_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.back_track_solution():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set_val(0)
                self.new_model()
                self.cubes[row][col].draw_update(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, rows, cols, width, height):
        self.value = value
        self.temp = 0
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 32)
        size = self.width/9
        x = self.cols*size
        y = self.rows*size

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (120, 120, 120))
            win.blit(text, (x + (size-text.get_width())/2, y + (size-text.get_height())/2))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (size-text.get_width())/2, y + (size-text.get_height())/2))

        if self.selected:
            if self.value != 0:
                pygame.draw.rect(win, (0, 255, 0), (x, y, size, size), 3)
            else:
                pygame.draw.rect(win, (255, 0, 0), (x, y, size, size), 3)

    def draw_update(self, win, w=True):
        fnt = pygame.font.SysFont('comicsans', 32)

        size = self.width/9
        x = self.cols*size
        y = self.rows*size

        pygame.draw.rect(win, (255, 255, 255), (x, y, size, size), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (size - text.get_width())/2, y + (size - text.get_height())/2))

        if w:
            pygame.draw.rect(win, (0, 255, 0), (x, y, size, size), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, size, size), 3)

    def set_val(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_win(win, board, strikes):
    win.fill((255, 255, 255))
    fnt = pygame.font.SysFont("comicsans", 32)
    text = fnt.render("X" * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and Board
    board.draw(win)


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    game = Grid(9, 9, 540, 540, win)
    strikes = 0
    key = 0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    game.clear()
                    key = 0

                if event.key == pygame.K_RETURN:
                    row, col = game.selected
                    if game.cubes[row][col].temp != 0:
                        if game.perm_val(game.cubes[row][col].temp):
                            print("Good")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = 0

                    if game.is_finished():
                        print("Game Over")
                        run = False

                if event.key == pygame.K_SPACE:
                    game.back_track_solution()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = game.click(pos)
                if clicked:
                    game.select(clicked[0], clicked[1])

        if game.selected and key != 0:
            game.temp_value(key)

        redraw_win(win, game, strikes)
        pygame.display.update()

main()
pygame.quit()