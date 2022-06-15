# import
from pathlib import Path
import pygame
import random
import sys
import time
from utils import ASSETS_DIR, BACKGROUND_IMAGE, BOARD_IMAGE, CIRCLE_IMAGE, CROSS_IMAGE, CROSSHAIR_IMAGE, CELL_DELTA, CELL_ORIGIN, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_SIZE            
# game settings

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(Path(ASSETS_DIR) / filename)
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Sign(pygame.sprite.Sprite):
    def __init__(self, filename, coordinate, size = 1, length = 150):
        super().__init__()
        self.image = pygame.image.load(Path(ASSETS_DIR) / filename)
        self.image = pygame.transform.scale(self.image, (length, length))
        self.rect = pygame.Rect(coordinate[0], coordinate[1], size, size)

class Board:
    def __init__(self, size = 600):
        self.size = size
        self.surface = pygame.image.load(Path(ASSETS_DIR) / BOARD_IMAGE)
        self.surface = pygame.transform.scale(self.surface, (size, size))
        self.status = create_2D()
    
    def is_valid_move(self, row, col):
        return self.status[row][col] == 0

    def move(self, row, col, player):
        self.status[row][col] = player
        return 2 if player == 1 else 1
    
    def is_player_win(self, player) -> bool:
        win = False
        # check rows
        for i in range(3):
            win = True
            for j in range(3):
                if player != self.status[i][j]:
                    win = False
                    break
            if win:
                return win
        
        # check cols
        for i in range(3):
            win = True
            for j in range(3):
                if player != self.status[j][i]:
                    win = False
                    break
            if win:
                return win
        # check diagonals
        win = True
        for j in range(3):
            if player != self.status[j][j]:
                win = False
                break
        if win:
            return win
        
        win = True
        for e, i in enumerate(list(range(2, -1, -1))):
            if player != self.status[e][i]:
                win = False
                break
        if win:
            return win
    
    def is_board_filled(self): 
        for row in self.status:
            for sign in row:
                if sign == 0:
                    return False
        return True 

def init_player(players):
    return random.randint(*players)

def create_2D():
    # [[1, 2, 3],
    #  [4, 5, 6],
    #  [7, 8, 9]]
    x = []
    for i in range(3):
        row = []
        
        for j in range(3):
            row.append(0)
        
        x.append(row)
    return x    

if "__main__" == __name__:
    running = True

    # initialization
    pygame.init()
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Tic Tac Toe")

    background = pygame.image.load(Path(ASSETS_DIR) / BACKGROUND_IMAGE)
    board = Board()
    player = init_player([1, 2])
    sign_mapping = {
        1: CIRCLE_IMAGE,
        2: CROSS_IMAGE
    }
    group = pygame.sprite.Group()
    crosshair = Crosshair(CROSSHAIR_IMAGE)
    group.add(crosshair)
    # circle = Sign(CIRCLE_IMAGE, (100, 100))
    # cross = Sign(CROSS_IMAGE, (, x))
    # group.add(circle)
    # group.add(cross)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = event.pos
                print(f"pos_x {pos_x}, pos_y {pos_y}")
                if not (pos_x <= board.size and pos_y <= board.size):
                    continue
                (_, _, width, height) = board.surface.get_rect()
                col = int(pos_x // (width/3))
                row = int(pos_y // (height/3))
                print(f"row {row}, col {col}")

                if board.is_valid_move(row, col):
                    current_player = player
                    sign = Sign(sign_mapping[current_player], (col*CELL_DELTA+CELL_ORIGIN, row*CELL_DELTA+CELL_ORIGIN))
                    player = board.move(row, col, current_player)
                    group.add(sign)
                    group.add(crosshair)
                    print(board.status)
                    if board.is_player_win(current_player):
                        print(f"Player {current_player} wins")
                        time.sleep(3)
                        sys.exit()
                    if board.is_board_filled():
                        print("Draw")
                        time.sleep(3)
                        sys.exit()

        screen.blit(background, (0, 0))
        screen.blit(board.surface, (0, 0))
        group.draw(screen)
        group.update()
        clock.tick(60)
        pygame.display.flip()
