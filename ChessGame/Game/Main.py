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
def CheckMateChecker(
    move_count: int,
) -> Tuple[bool | None, Literal["NoSide", "W", "B"]]:
    """
    Checks if the given side(move_count) is checkmated by opponent.

    Args:
        move_count: int : The move number currently going on.

    Return:
        Tuple[bool, str] : Returns [0]:False if no action, True if checkmated, None if stalemate.
                            [1]: "NoSide" if no action, opponent side if checkmate, own side if stalemate.
    """
    own_color = "W" if move_count % 2 == 0 else "B"
    opponent_color = "B" if own_color == "W" else "W"
    # This address has all the move address of every piece.
    # If this is non-empty means a move is possible and no checkmate or stalemate is possibles.
    all_piece_move_address = []
    # Going through all pieces.
    # Here created a list slice to avoid KeysChangedDuringIteration error.
    # The changing of keys is temporary and WILL revert back.
    for piece_item in list(main.occupied_squares.items())[:]:
        if piece_item[1][0] == own_color:
            # Creating appropriate address and extending them to all_piece_move_address.
            if piece_item[1][1:] == "Pawn":
                all_piece_move_address.extend(
                    main.PawnMoveAddress(
                        piece_coords=piece_item[0], move_count=move_count
                    )
                )
            elif piece_item[1][1:] == "Knight":
                all_piece_move_address.extend(
                    main.KnightMoveAddress(
                        piece_coords=piece_item[0], move_count=move_count
                    )
                )
            elif piece_item[1][1:] == "King":
                all_piece_move_address.extend(
                    main.KingMoveAddress(
                        piece_coords=piece_item[0], move_count=move_count
                    )
                )
            elif piece_item[1][1:] == "Rook":
                all_piece_move_address.extend(
                    main.SlidingMoveAddress(
                        piece_coords=piece_item[0],
                        move_count=move_count,
                        piece_type="Ax",
                    )
                )
            elif piece_item[1][1:] == "Bishop":
                all_piece_move_address.extend(
                    main.SlidingMoveAddress(
                        piece_coords=piece_item[0],
                        move_count=move_count,
                        piece_type="Qu",
                    )
                )
            elif piece_item[1][1:] == "Queen":
                all_piece_move_address.extend(
                    main.SlidingMoveAddress(
                        piece_coords=piece_item[0],
                        move_count=move_count,
                        piece_type="Ax",
                    )
                    + main.SlidingMoveAddress(
                        piece_coords=piece_item[0],
                        move_count=move_count,
                        piece_type="Qu",
                    )
                )
        # If all_piece_move_address is even filled with 1 location then no checkmate or stalemate.
        # This breaks as soon as one location is found saving computation.
        if all_piece_move_address:
            return (False, "NoSide")
    # If no movable locations are found then.
    if not all_piece_move_address:
        # If no piece can move and king is in check then checkmate.
        if main.IsOwnKingAttacked(move_count=move_count):
            return (True, opponent_color)
        # Else stalemate.
        return (None, own_color)

main = Main()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
board_img = pygame.image.load("Assets\\BoardImg.png")
board_img = pygame.transform.scale(board_img, (WIDTH, HEIGHT))

timer = pygame.time.Clock()
FPS = 120

FONT_TYPE = pygame.font.Font("Assets\\Font\\JetBrainsMono.ttf", 75)
FONT_POS = 250, 350

BLACK = (0, 0, 0)

game_continue = True
mouse_grid_pos = -1, -1
piece_that_has_to_move_data = []
check_mate_item = (False, "NoSide")
while True:
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
    if main.move_address and game_continue:
        # Checks if the click is in move_address meaning the move is to be performed.
        if mouse_grid_pos in main.move_address:
            main.occupied_squares.pop(piece_that_has_to_move_data[0])
            main.occupied_squares.update(
                {mouse_grid_pos: piece_that_has_to_move_data[1]}
            )
            main.move_address = []
            piece_that_has_to_move_data = []
            mouse_grid_pos = -1, -1
            # If the move has been done then turn change
            main.move_count += 1
            check_mate_item = CheckMateChecker(move_count=main.move_count)
        # If the user has not performed a move but has clicked a square.
        elif mouse_grid_pos != piece_that_has_to_move_data[0]:
            # We redo the logic to check if the new pos the user has clicked is a valid piece.
            # This creates the new move address if the same side piece is clicked.
            main.Logic(mouse_grid_pos=mouse_grid_pos)
            # If move address gets created then we remake the move data and move the piece in the next iteration.
            if main.move_address:
                piece_that_has_to_move_data = [
                    mouse_grid_pos,
                    main.occupied_squares[mouse_grid_pos],
                ]
            # If no move address is created that is no valid movable piece is clicked then the conditions reset and
            # we again wait for a click
            else:
                main.move_address = []
                piece_that_has_to_move_data = []
                mouse_grid_pos = -1, -1
    elif not main.move_address and game_continue:
        main.Logic(mouse_grid_pos=mouse_grid_pos)
        if main.move_address:
            piece_that_has_to_move_data = [
                mouse_grid_pos,
                main.occupied_squares[mouse_grid_pos],
            ]
        else:
            piece_that_has_to_move_data = []
    # These place the pieces and their move markers.
    PieceImagePlacer(
        loaded_images=main.loaded_images, occupied_squares=main.occupied_squares
    )
    MoveMarkerPlacer(move_address=main.move_address)
    if check_mate_item[0] is None:
        msg = FONT_TYPE.render("Draw due to Stalemate", False, (0, 0, 0))
        screen.blit(msg, FONT_POS)
        game_continue = False
    elif check_mate_item[0]:
        msg = FONT_TYPE.render(f"{check_mate_item[1]} WINS!", False, (0, 0, 0))
        screen.blit(msg, FONT_POS)
        game_continue = False
    pygame.display.flip()
    timer.tick(FPS)

pygame.quit()
