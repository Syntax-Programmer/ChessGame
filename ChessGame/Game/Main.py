"""
This is the main game file that hosts the game 

Author: Anand Maurya
Github: Syntax-Programmer
Email: anand6308anand@gmail.com
"""

__author__ = "Anand Maurya/ Syntax-Programmer"
__email__ = "anand6308anand@gmail.com"


from sys import exit
from Engine import Main
from typing import List, Tuple, Literal, Dict

import pygame
import pygame.locals
import AssetsLoader


pygame.init()
main = Main()


INT_RANGE = Literal[0, 1, 2, 3, 4, 5, 6, 7]


def mouse_pos_to_square_mapper(
    mouse_pos: Tuple[int, int]
) -> Tuple[INT_RANGE, INT_RANGE]:
    """
    Maps the user click to a square on the board.

    Takes the random click pos on the screen and maps it to an square coordinate
    corresponding to a square.

    Parameters:
    ----------
    1. mouse_pos : Tuple[int, int]
        The location of the user click.

    Returns:
    -------
    Tuple[INT_RANGE, INT_RANGE] :
        The click coordinates mapped to a square on the chess board.
    """
    x_pos = (mouse_pos[0] - mouse_pos[0] % 100) // 100
    y_pos = (mouse_pos[1] - mouse_pos[1] % 100) // 100
    return x_pos, y_pos


def piece_image_renderer(
    occupied_squares: Dict[Tuple[int, int], str],
    move_list: List[Tuple[int, int] | None],
) -> None:
    global screen
    """
    Places all the piece related images on the board.

    Takes occupied_squares to determine what pieces should be on the board and
    move_list for the locations to mark as movable.

    Parameters:
    ----------
    1. occupied_squares : Dict[Tuple[INT_RANGE, INT_RANGE], str]
        A dictionary of all the occupied squares mapped to the piece occupying that square.
    2. move_list : List[Tuple[INT_RANGE, INT_RANGE] | None]
        The locations of possible movable locations of a given piece.
    """
    SCALING_RATIO = 100
    OFFSET = 17
    for piece_location, piece_type in occupied_squares.items():
        screen.blit(
            AssetsLoader.LOADED_IMAGES[
                AssetsLoader.PIECE_TYPE_TO_INDEX_TABLE[piece_type]
            ],
            (
                (piece_location[0] * SCALING_RATIO) + OFFSET,
                (piece_location[1] * SCALING_RATIO) + OFFSET,
            ),
        )
    for locations in move_list:
        screen.blit(
            AssetsLoader.move_maker,
            (
                (locations[0] * SCALING_RATIO) + OFFSET,
                (locations[1] * SCALING_RATIO) + OFFSET,
            ),
        )


def game_state_determiner(move_count: int) -> Tuple[int, str]:
    """
    Determines the effect of the last move on the game-state.

    Takes the move_number just after it has been incremented by 1 to check if the other side is
    in checkmate or stalemate.

    Parameters:
    ----------
    1. move_count : int
            The move number going on.

    Returns:
    -------
    Tuple[int,str] :
        The tuple contains the game_state_code and the appropriate side.
        Codes:
            0 : Normal
            1 : Checkmate
            2 : Stalemate
    """
    own_color = "W" if move_count % 2 == 0 else "B"
    opponent_color = "B" if own_color == "W" else "W"
    for piece_location, piece_type in list(main.occupied_squares.items())[:]:
        movable_location = []
        if piece_type[0] == own_color:
            movable_location = main.move_list_mapping_table[piece_type[1:]](
                location=piece_location, move_count=move_count
            )
        # If movable_location is even filled with 1 location then no checkmate or stalemate.
        # This breaks as soon as one location is found saving computation.
        if movable_location:
            return (0, "NoSide")
    # If no piece can move and king is in check then checkmate.
    if main.is_own_king_attacked(move_count=move_count):
        return (1, opponent_color)
    # Else stalemate.
    return (2, own_color)


def castling_rights_manager(
    piece_that_has_to_move: Tuple[Tuple[INT_RANGE, INT_RANGE], str]
) -> None:
    """
    Cancels the appropriate castling rights.

    Cancels the rights if the king or rook of one side moves.

    Parameters:
    ----------
    1. piece_that_has_to_be_moved : Tuple[Tuple[INT_RANGE, INT_RANGE] | None, str | None]
        A empty list if no piece has to be moved else a [location, piece_type] item.
    """
    if piece_that_has_to_move[1] == "WKing":
        main.white_long_castle = main.white_short_castle = False
    elif piece_that_has_to_move[1] == "BKing":
        main.black_long_castle = main.black_short_castle = False
    elif piece_that_has_to_move[1] == "WRook":
        if piece_that_has_to_move[0] == (0, 7):
            main.white_long_castle = False
        elif piece_that_has_to_move[0] == (7, 7):
            main.white_short_castle = False
    elif piece_that_has_to_move[1] == "BRook":
        if piece_that_has_to_move[0] == (0, 0):
            main.black_long_castle = False
        elif piece_that_has_to_move[0] == (7, 0):
            main.black_short_castle = False


def castle_rook_mover(
    move_count: int,
    mouse_grid_pos: Tuple[INT_RANGE, INT_RANGE],
    piece_that_has_to_move: Tuple[Tuple[INT_RANGE, INT_RANGE], str],
) -> None:
    row = 7 if move_count % 2 == 0 else 0
    own_color = "W" if move_count % 2 == 0 else "B"
    if piece_that_has_to_move[1][1:] != "King" or mouse_grid_pos not in [
        (6, row),
        (2, row),
    ]:
        return None
    if mouse_grid_pos == (6, row):
        main.occupied_squares.pop((7, row))
        main.occupied_squares[(5, row)] = f"{own_color}Rook"
    elif mouse_grid_pos == (2, row):
        main.occupied_squares.pop((0, row))
        main.occupied_squares[(3, row)] = f"{own_color}Rook"
    if own_color == "W":
        main.white_long_castle = main.white_short_castle = False
    elif own_color == "B":
        main.black_long_castle = main.black_short_castle = False


def playing_logic(
    mouse_grid_pos: Tuple[INT_RANGE, INT_RANGE],
    piece_that_has_to_move: Tuple[Tuple[INT_RANGE, INT_RANGE] | None, str | None],
) -> Tuple[
    Tuple[INT_RANGE | Literal[-1], INT_RANGE | Literal[-1]],
    Tuple[Tuple[INT_RANGE, INT_RANGE] | None, str | None],
]:
    """
    The main logic of moving the pieces and checking for checkmates/stalemates.

    Takes the user click square and the piece that can be move currently and takes appropriate actions.

    Parameters:
    ----------
    1. mouse_grid_pos : Tuple[INT_RANGE, INT_RANGE]
        The location of the user click mapped to a square.
    2. piece_that_has_to_be_moved : Tuple[Tuple[INT_RANGE, INT_RANGE] | None, str | None]
        A empty list if no piece has to be moved else a [location, piece_type] item.

    Returns:
    -------
    Tuple[
    Tuple[INT_RANGE | Literal[-1], INT_RANGE | Literal[-1]],
    Tuple[int, str],
    Tuple[Tuple[INT_RANGE, INT_RANGE] | None, str | None],
    ] :
        The updated versions of the arguments passed like :
        (mouse_grid_pos, game_state_data, piece_that_has_to_move)
    """
    game_state_data = (0, "NoSide")
    if main.move_list:
        # If move_list exists and user want to move.
        if mouse_grid_pos in main.move_list:
            main.occupied_squares.pop(piece_that_has_to_move[0])
            main.occupied_squares[mouse_grid_pos] = piece_that_has_to_move[1]
            castle_rook_mover(
                move_count=main.move_count,
                mouse_grid_pos=mouse_grid_pos,
                piece_that_has_to_move=piece_that_has_to_move,
            )
            castling_rights_manager(piece_that_has_to_move=piece_that_has_to_move)
            main.move_list = piece_that_has_to_move = []
            mouse_grid_pos = -1, -1
            main.move_count += 1
            game_state_data = game_state_determiner(move_count=main.move_count)
        # When user click pos is not somewhere moveable and also that the user has clicked somewhere after clicking the piece to move.
        elif mouse_grid_pos != piece_that_has_to_move[0]:
            main.logic(mouse_grid_pos=mouse_grid_pos)
            if main.move_list:
                piece_that_has_to_move = [
                    mouse_grid_pos,
                    main.occupied_squares[mouse_grid_pos],
                ]
            else:
                piece_that_has_to_move = []
                mouse_grid_pos = -1, -1
    # If no move_list exists meaning we have to check for user input.
    else:
        main.logic(mouse_grid_pos=mouse_grid_pos)
        if main.move_list:
            piece_that_has_to_move = [
                mouse_grid_pos,
                main.occupied_squares[mouse_grid_pos],
            ]
        else:
            piece_that_has_to_move = []

    return mouse_grid_pos, game_state_data, piece_that_has_to_move


SCREEN_SIZE = 800, 800
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Chess Game")

timer = pygame.time.Clock()
FPS = 120

FONT_TYPE = pygame.font.Font("Assets\\Font\\JetBrainsMono.ttf", 50)

BLACK = (0, 0, 0)
BOARD_IMG_POS = 0, 0

mouse_grid_pos = -1, -1
piece_that_has_to_move = []
# game_state_data[0] == 0 : Game should continue as normal.
# game_state_data[0] == 1 : Check-mate delivered game ended.
# game_state_data[0] == 2 : Game ended due to stalemate.
game_state_data = (0, "NoSide")
game_playing = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_grid_pos = mouse_pos_to_square_mapper(
                mouse_pos=pygame.mouse.get_pos()
            )
    if game_playing:
        mouse_grid_pos, game_state_data, piece_that_has_to_move = playing_logic(
            mouse_grid_pos=mouse_grid_pos, piece_that_has_to_move=piece_that_has_to_move
        )
    screen.fill(BLACK)
    screen.blit(AssetsLoader.board_image, BOARD_IMG_POS)
    piece_image_renderer(
        occupied_squares=main.occupied_squares, move_list=main.move_list
    )

    if game_state_data[0] == 2:
        msg = FONT_TYPE.render("Draw due to Stalemate", False, (0, 0, 0))
        screen.blit(msg, (100, 350))
        game_playing = False
    elif game_state_data[0] == 1:
        msg = FONT_TYPE.render(f"{game_state_data[1]} WINS!", False, (0, 0, 0))
        screen.blit(msg, (300, 350))
        game_playing = False

    pygame.display.flip()
    timer.tick(FPS)
