"""
This modules has all the image assets for use in other files 

Author: Anand Maurya
Github: Syntax-Programmer
Email: anand6308anand@gmail.com
"""

__author__ = "Anand Maurya/ Syntax-Programmer"
__email__ = "anand6308anand@gmail.com"


import pygame
import pygame.locals


PIECE_TYPE_TO_INDEX_TABLE = {
    "WPawn": 0,
    "WRook": 1,
    "WKnight": 2,
    "WBishop": 3,
    "WQueen": 4,
    "WKing": 5,
    "BPawn": 6,
    "BRook": 7,
    "BKnight": 8,
    "BBishop": 9,
    "BQueen": 10,
    "BKing": 11,
}


LOADED_IMAGES = []
PIECE_IMAGE_SIZE = 65, 65
pieces = ["Pawn", "Rook", "Knight", "Bishop", "Queen", "King"]
for side in "WB":
    for piece_type in pieces:
        path = f"Assets\\Pieces\\{side}Pieces\\{side}{piece_type}.png"
        image = pygame.image.load(path)
        LOADED_IMAGES.append(pygame.transform.scale(image, PIECE_IMAGE_SIZE))


BOARD_SIZE = 800, 800
board_image = pygame.image.load("Assets\\BoardImg.png")
board_image = pygame.transform.scale(board_image, BOARD_SIZE)


MOVE_MARKER_SIZE = 70, 70
move_maker = pygame.image.load("Assets\\MoveMarker.png")
move_maker = pygame.transform.scale(move_maker, MOVE_MARKER_SIZE)
