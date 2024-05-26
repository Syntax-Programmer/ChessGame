import pygame
import pygame.locals
from sys import exit
from Engine import Main
from typing import Tuple, Dict, List


def MouseToGridConverter(mouse_pos: Tuple[int, int]) -> Tuple[int, int]:
    """
    Converts the random pos of the user click to represent a particular square.

    Args:
        mouse_pos:Tuple[int,int] : The coords of the user's clicks.

    Return:
        Tuple[int,int] : The user click associated to a square.
        For eg :
        (150, 101) -> (1, 1), (714, 222) -> (7, 2)
    """
    x_pos = (mouse_pos[0] - mouse_pos[0] % 100) // 100
    y_pos = (mouse_pos[1] - mouse_pos[1] % 100) // 100
    return x_pos, y_pos


pygame.init()


def PieceImagePlacer(
    loaded_images, occupied_squares: Dict[Tuple[int, int], str]
) -> None:
    """
    Places all the piece images on the correct place.

    Args:
        loaded_img: List[Surface] : List of all piece images.
        occupied_squares: Dict[Tuple[int, int], str] : Dictionary where occupied squares are
        mapped to piece on them.

    Return:
        None : None
    """
    MAPPING_TABLE = {
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
    SCALING_RATIO = 100
    OFFSET = 17
    for locations, piece_type in occupied_squares.items():
        screen.blit(
            loaded_images[MAPPING_TABLE[piece_type]],
            (
                (locations[0] * SCALING_RATIO) + OFFSET,
                (locations[1] * SCALING_RATIO) + OFFSET,
            ),
        )


move_marker = pygame.image.load("Assets\\MoveMarker.png")
move_marker = pygame.transform.scale(move_marker, (70, 70))


def MoveMarkerPlacer(move_address: List[Tuple[int, int] | None]) -> None:
    """
    Marks all the places the respective piece can move to.

    Args:
        move_address: List[Tuple[int,int] | None] : All the possible locations a
        piece can move to.

    Return:
        None : None
    """
    SCALING_RATIO = 100
    OFFSET = 15
    marker = move_marker
    for locations in move_address:
        screen.blit(
            marker,
            (
                (locations[0] * SCALING_RATIO) + OFFSET,
                (locations[1] * SCALING_RATIO) + OFFSET,
            ),
        )


main = Main()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
board_img = pygame.image.load("Assets\\BoardImg.png")
board_img = pygame.transform.scale(board_img, (WIDTH, HEIGHT))

timer = pygame.time.Clock()
FPS = 120
BLACK = (0, 0, 0)

running = True
mouse_grid_pos = -1, -1
moving_data = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_grid_pos = MouseToGridConverter(mouse_pos=pygame.mouse.get_pos())
    # Resetting the screen before new data is filled in.
    screen.fill(BLACK)
    screen.blit(board_img, (0, 0))
    # If the user has clicked for on a valid piece and the possible move have been created.
    if main.move_address:
        # Checks if the click is in move_address meaning the move is to be performed.
        if mouse_grid_pos in main.move_address:
            main.occupied_squares.pop(moving_data[0])
            main.occupied_squares.update({mouse_grid_pos: moving_data[1]})
            main.move_address = []
            moving_data = []
            mouse_grid_pos = -1, -1
            # If the move has been done then turn change
            main.move_count += 1
        # If the user has not performed a move but has clicked a square.
        elif mouse_grid_pos != moving_data[0]:
            # We redo the logic to check if the new pos the user has clicked is a valid piece.
            # This creates the new move address if the same side piece is clicked.
            main.Logic(mouse_grid_pos=mouse_grid_pos)
            # If move address gets created then we remake the move data and move the piece in the next iteration.
            if main.move_address:
                moving_data = [mouse_grid_pos, main.occupied_squares[mouse_grid_pos]]
            # If no move address is created that is no valid movable piece is clicked then the conditions reset and
            # we again wait for a click
            else:
                main.move_address = []
                moving_data = []
                mouse_grid_pos = -1, -1
    elif not main.move_address:
        main.Logic(mouse_grid_pos=mouse_grid_pos)
        if main.move_address:
            moving_data = [mouse_grid_pos, main.occupied_squares[mouse_grid_pos]]
        else:
            moving_data = []
    # These place the pieces and their move markers.
    PieceImagePlacer(
        loaded_images=main.loaded_images, occupied_squares=main.occupied_squares
    )
    MoveMarkerPlacer(move_address=main.move_address)
    pygame.display.flip()
    timer.tick(FPS)

pygame.quit()
