import pygame
import sys
import utils
from utils import BG_COLOR, HEIGHT, WIDTH, SIZE, GAME_TITLE, STROKE_WIDTH, STROKE_COLOR, SIGN_COLOR, CROSS_MARGIN
# BG_COLOR = (36, 106, 115)
# HEIGHT = 600
# WIDTH = 600
# SIZE = (HEIGHT, WIDTH)
# GAME_TITLE = "Tic Tac Toe"
# STROKE_WIDTH = 5
# STROKE_COLOR = (255, 255, 255)
# SIGN_COLOR = (246, 174, 45)
# CROSS_MARGIN = 40

class Board:
    def __init__(self, n: int):
        self.n = n

class Player:
    def __init__(self, sign: int):
        self.sign = sign

def draw_line():
    pygame.draw.line(screen, STROKE_COLOR, (0, HEIGHT/3), (WIDTH, HEIGHT/3), STROKE_WIDTH)
    pygame.draw.line(screen, STROKE_COLOR, (0, HEIGHT/3*2), (WIDTH, HEIGHT/3*2), STROKE_WIDTH)
    pygame.draw.line(screen, STROKE_COLOR, (WIDTH/3, 0), (WIDTH/3, HEIGHT), STROKE_WIDTH)
    pygame.draw.line(screen, STROKE_COLOR, (WIDTH/3*2, 0), (WIDTH/3*2, HEIGHT), STROKE_WIDTH)

def draw_circle(row, col):
    pygame.draw.circle(screen, SIGN_COLOR, (int(col * WIDTH/3 + WIDTH/6), int(row * HEIGHT/3 + HEIGHT/6)), HEIGHT/6 * 0.7, STROKE_WIDTH)

    # [[1, 2, 3],
    #  [4, 5, 6],
    #  [7, 8, 9]]

def draw_cross(row, col):
    pygame.draw.line(screen,
                     SIGN_COLOR,
                     (int(col * WIDTH/3 + CROSS_MARGIN), int(row * HEIGHT/3 + CROSS_MARGIN)),
                     (int(col * WIDTH/3 + WIDTH/3 - CROSS_MARGIN), int(row * HEIGHT/3 + HEIGHT/3 - CROSS_MARGIN)), 
                     STROKE_WIDTH)
    pygame.draw.line(screen,
                     SIGN_COLOR,
                     (int(col * WIDTH/3 + CROSS_MARGIN), int(row * HEIGHT/3 + HEIGHT/3 - CROSS_MARGIN)),
                     (int(col * WIDTH/3 + WIDTH/3 - CROSS_MARGIN), int(row * HEIGHT/3 + CROSS_MARGIN)), 
                     STROKE_WIDTH)
#:%s/pattern/replace/g 

def draw_sign(row, col):
    if player == 1:
        draw_circle(row, col)
    elif player == 2:
        draw_cross(row, col)

def is_valid_move(row, col):
    # 0 -> None
    # 1 -> O
    # 2 -> X
    return board[row][col] == 0

def create_board():
    # [[1, 2, 3],
    #  [4, 5, 6],
    #  [7, 8, 9]]
    board = []
    for i in range(3):
        row = []
        
        for j in range(3):
            row.append(0)
        
        board.append(row)
    return board    

def move(row, col):
    board[row][col] = player

def is_player_win():
    win = False
    # check rows
    for i in range(3):
        win = True
        for j in range(3):
            if player != board[i][j]:
                win = False
                break
        if win:
            return win
    
    # check cols
    for i in range(3):
        win = True
        for j in range(3):
            if player != board[j][i]:
                win = False
                break
        if win:
            return win
    # check diagonals
    win = True
    for j in range(3):
        if player != board[j][j]:
            win = False
            break
    if win:
        return win
    
    win = True
    for e, i in enumerate(list(range(2, -1, -1))):
        if player != board[e][i]:
            win = False
            break
    if win:
        return win

def is_board_filled():
    # for i in range(3):
    #     for j in range(3):
    #         if board[i][j] == 0:
    #             return False
    # return True
    for row in board:
        for sign in row:
            if sign == 0:
                return False
    return True 


if "__main__" == __name__:
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption(GAME_TITLE)
    screen.fill(utils.BG_COLOR)
    draw_line()
    board = create_board()
    player = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = event.pos
                col = int(pos_x // (WIDTH/3))
                row = int(pos_y // (HEIGHT/3))
                # print(row, col)
                # draw_cross(row, col)
                if is_valid_move(row, col):
                    print("valid")
                    move(row, col)
                    draw_sign(row, col)
                    
                    if is_player_win():
                        print(f"Player{player} wins")
                        sys.exit()
                    
                    if is_board_filled():
                        print("Tie")
                        sys.exit()
                    
                    # player = 3 - player
                    player = 2 if player == 1 else 1
                else:
                    print("fail")

        pygame.display.update()            
