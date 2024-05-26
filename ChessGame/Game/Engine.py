import pygame
from typing import Tuple, List, Dict, Literal


def PawnAddress(
    sq_coords: Tuple[int, int], move_count: int
) -> Tuple[List[Tuple[int, int] | None], List[Tuple[int, int] | None]]:
    """
    Gives the general locations of a pawn movement.

    Args:
        sq_coords: Tuple[int, int] : A location on the board.
        move_count: int : The move number currently going on.

    Return:
        Tuple[List[Tuple[int, int] | None], List[Tuple[int, int] | None]] :
        Gives all the possible moves of a pawn separated into 2 lists:
        1. Locations a pawn on given sq_coord can move to.
        2. Locations a pawn on given sq_coords can capture to OR a opponent pawn on
        produced locations can attack given sq_coords.
    """
    moving_direction = -1 if move_count % 2 == 0 else 1
    moving_address = [
        (sq_coords[0], sq_coords[1] + (step * moving_direction))
        for step in [1, 2]
        if sq_coords[1] + (step * moving_direction) in range(8)
    ]
    capturing_address = [
        (sq_coords[0] + step, sq_coords[1] + moving_direction)
        for step in [1, -1]
        if sq_coords[0] + step in range(8)
        and sq_coords[1] + moving_direction in range(8)
    ]
    return moving_address, capturing_address


def KnightAddress(sq_coords: Tuple[int, int]) -> List[Tuple[int, int] | None]:
    """
    Gives the general locations of a knight movement.

    Args:
        sq_coords: Tuple[int, int] : A location on the board.

    Return:
        List[Tuple[int, int] | None] : Gives all the locations where:
        1. A knight on given sq_coord can move to.
        2. A opponent knight on produced locations can attack the given sq_coords.
    """
    address = [
        (sq_coords[0] + x_step, sq_coords[1] + y_step)
        for x_step, y_step in [
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (-1, 2),
            (1, -2),
            (-1, -2),
        ]
        if sq_coords[0] + x_step in range(8) and sq_coords[1] + y_step in range(8)
    ]
    return address


def KingAddress(sq_coords: Tuple[int, int]) -> List[Tuple[int, int] | None]:
    """
    Gives the general locations of a king movement.

    Args:
        sq_coords: Tuple[int, int] : A location on the board.

    Return:
        List[Tuple[int, int] | None] : Gives all the locations where:
        1. A king on given sq_coord can move to.
        2. A opponent king on produced locations can attack the given sq_coords.
    """
    address = [
        (sq_coords[0] + x_step, sq_coords[1] + y_step)
        for x_step, y_step in [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, -1),
            (-1, -1),
            (-1, 1),
            (1, 1),
        ]
        if sq_coords[0] + x_step in range(8) and sq_coords[1] + y_step in range(8)
    ]
    return address


def SlidingAddressFilter(
    to_filter: List[Tuple[int, int]],
    occupied_squares: Dict[Tuple[int, int], str],
    address_constructor: Tuple[int, int],
) -> List[Tuple[int, int]]:
    """
    Filter the general sliding piece address to only have squares that
    the sliding piece on address_constructor can reach.

    Args:
        to_filter: List[Tuple[int, int]] : An address of the sliding piece that needs to be filtered.
        occupied_square: Dict[Tuple[int, int], str] : The dictionary containing all
        the occupied squares on the board mapped to the piece type.
        address_constructor: Tuple[int,int] : A location on the board w.r.t the to_filter was made.

    Return:
        List[Tuple[int,int]] : Gives a filtered list of squares a sliding piece can
        theoretically reach.
    """
    constructor_index = to_filter.index(tuple(address_constructor))
    left_address = to_filter[:constructor_index]
    left_reach_index = 0
    right_address = to_filter[constructor_index + 1 :]
    right_reach_index = 8
    for locations in left_address[::-1]:
        if locations in occupied_squares:
            left_reach_index = to_filter.index(locations)
            break
    for locations in right_address:
        if locations in occupied_squares:
            right_reach_index = to_filter.index(locations)
            break
    to_filter = to_filter[left_reach_index : right_reach_index + 1]
    # Removing address_constructor because the sliding piece on the address_constructor can't move to its own location.
    # It was causing error with the AttackedBySlidingPiece.
    to_filter.remove(tuple(address_constructor))
    return to_filter


def AxialAddress(
    sq_coords: Tuple[int, int], occupied_squares: Dict[Tuple[int, int], str]
) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    """
    Gives the general locations of a rook/queen movement.

    Args:
        sq_coords: Tuple[int, int] : A location on the board.
        occupied_square: Dict[Tuple[int, int], str] : The dictionary containing all
        the occupied squares on the board mapped to the piece type.

    Return:
        Tuple[List[Tuple[int, int] | None], List[Tuple[int, int] | None]] : Gives 2 lists:
        1. All locations on the same row as the given sq_coords
        where a rook/queen CAN REACH.
        2. All locations on the same col as the given sq_coords
        where a rook/queen CAN REACH.
    """
    x_address = [(x_pos, sq_coords[1]) for x_pos in range(8)]
    y_address = [(sq_coords[0], y_pos) for y_pos in range(8)]
    return SlidingAddressFilter(
        to_filter=x_address,
        occupied_squares=occupied_squares,
        address_constructor=sq_coords,
    ), SlidingAddressFilter(
        to_filter=y_address,
        occupied_squares=occupied_squares,
        address_constructor=sq_coords,
    )


def QuadrantalAddress(
    sq_coords: Tuple[int, int], occupied_squares: Dict[Tuple[int, int], str]
) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    """
    Gives the general locations of a bishop/queen movement.

    Args:
        sq_coords: Tuple[int, int] : A location on the board.
        occupied_square: Dict[Tuple[int, int], str] : The dictionary containing all
        the occupied squares on the board mapped to the piece type.

    Return:
        Tuple[List[Tuple[int, int] | None], List[Tuple[int, int] | None]] : Gives 2 lists:
        1. All locations on the same anti-diagonal as the given sq_coords
        where a bishop/queen CAN REACH.
        2. All locations on the same main-diagonal as the given sq_coords
        where a bishop/queen CAN REACH.
    """
    anti_diagonal_address = [
        (sq_coords[0] + step, sq_coords[1] - step)
        for step in range(-7, 8)
        if sq_coords[0] + step in range(8) and sq_coords[1] - step in range(8)
    ]
    main_diagonal_address = [
        (sq_coords[0] + step, sq_coords[1] + step)
        for step in range(-7, 8)
        if sq_coords[0] + step in range(8) and sq_coords[1] + step in range(8)
    ]
    return SlidingAddressFilter(
        to_filter=anti_diagonal_address,
        occupied_squares=occupied_squares,
        address_constructor=sq_coords,
    ), SlidingAddressFilter(
        to_filter=main_diagonal_address,
        occupied_squares=occupied_squares,
        address_constructor=sq_coords,
    )


class Attacked:
    """Checks if the given square is attacked by the specified pieces."""

    def __init__(
        self,
        occupied_squares: Dict[Tuple[int, int], str],
    ) -> None:
        self.occupied_squares = occupied_squares
        # NOTE: Line 114 and 320 are affected by the list type of the variables,
        # so type conversion to a tuple has been done to correct the error.
        self.WKing_location = [4, 7]
        self.BKing_location = [0, 7]

    def AttackedByNonSlidingPieces(
        self, location_to_check: Tuple[int, int], move_count: int
    ) -> bool:
        """
        Checks if the given location_to_check is attacked by a
        pawn or a knight.

        Args:
            location_to_check: Tuple[int, int] : The board coord to be check for
            if it is attacked.
            move_count: int : The move number currently going on.

        Return:
            bool : Gives True if the given location_to_check is attacked by
            a pawn or a knight.
        """
        opponent_color = "B" if move_count % 2 == 0 else "W"
        from_pawn_attacking = PawnAddress(
            sq_coords=location_to_check, move_count=move_count
        )[1]
        from_knight_attacking = KnightAddress(sq_coords=location_to_check)
        return any(
            self.occupied_squares.get(locations) == f"{opponent_color}Pawn"
            for locations in from_pawn_attacking
        ) or any(
            self.occupied_squares.get(locations) == f"{opponent_color}Knight"
            for locations in from_knight_attacking
        )

    def AttackedBySlidingPieces(
        self, location_to_check: Tuple[int, int], move_count: int
    ) -> bool:
        """
        Checks if the given location_to_check is attacked by a
        rook or a bishop or a queen.

        Args:
            location_to_check: Tuple[int, int] : The board coord to be check for
            if it is attacked.
            move_count: int : The move number currently going on.

        Return:
            bool : Gives True if the given location_to_check is attacked by a
            rook or a bishop or a queen..
        """
        opponent_color = "B" if move_count % 2 == 0 else "W"
        from_x_address, from_y_address = AxialAddress(
            sq_coords=location_to_check, occupied_squares=self.occupied_squares
        )
        from_13_address, from_24_address = QuadrantalAddress(
            sq_coords=location_to_check, occupied_squares=self.occupied_squares
        )
        from_axial_attacking, from_quadrantal_attacking = (
            (from_x_address[0], from_x_address[-1])
            + (from_y_address[0], from_y_address[-1]),
            (from_13_address[0], from_13_address[-1])
            + (from_24_address[0], from_24_address[-1]),
        )
        return any(
            self.occupied_squares.get(locations)
            in [f"{opponent_color}Rook", f"{opponent_color}Queen"]
            for locations in from_axial_attacking
        ) or any(
            self.occupied_squares.get(locations)
            in [f"{opponent_color}Bishop", f"{opponent_color}Queen"]
            for locations in from_quadrantal_attacking
        )

    # Separated AttackedByKing as in some cases it is not needed.
    def AttackedByKing(
        self, location_to_check: Tuple[int, int], move_count: int
    ) -> bool:
        """
        Checks if the given location_to_check is attacked by a
        king.

        Args:
            location_to_check: Tuple[int, int] : The board coord to be check for
            if it is attacked.
            move_count: int : The move number currently going on.

        Return:
            bool : Gives True if the given location_to_check is attacked by a
            king.
        """
        opponent_color = "B" if move_count % 2 == 0 else "W"
        from_king_attacking = KingAddress(sq_coords=location_to_check)
        return any(
            self.occupied_squares.get(locations) == f"{opponent_color}King"
            for locations in from_king_attacking
        )

    # Attacked by king is excluded as kings can't attack
    # other kings.
    def IsOwnKingAttacked(self, move_count: int) -> bool:
        """
        Checks if the current player's king is attacked by
        any piece other that king.

        Args:
            move_count: int : The move number currently going on.

        Return:
            bool : Gives True if the player's king is attacked by
            any piece other than king.
        """
        own_color = "W" if move_count % 2 == 0 else "B"
        king_location = (
            self.WKing_location if own_color == "White" else self.BKing_location
        )
        if self.occupied_squares.get(tuple(king_location)) != f"{own_color}King":
            for location, piece_type in self.occupied_squares.items():
                if piece_type == f"{own_color}King":
                    king_location[:] = location
        return self.AttackedByNonSlidingPieces(
            location_to_check=king_location, move_count=move_count
        ) or self.AttackedBySlidingPieces(
            location_to_check=king_location, move_count=move_count
        )


class MoveAddress(Attacked):
    """Class Creates all the possible valid moves of a piece."""

    def __init__(self, occupied_squares: Dict[Tuple[int], str]) -> None:
        super().__init__(occupied_squares)

    def SquaresThatPutKingInCheckRemover(
        self,
        piece_coords: Tuple[int, int],
        to_filter: List[Tuple[int, int] | None],
        move_count: int,
    ) -> List[Tuple[int, int] | None]:
        """
        Filter all squares out to which the piece on given piece_coords moves
        to puts their own king in check.

        Args:
            piece_coords: Tuple[int, int] : The location of the pawn piece to
            be modified.
            to_filter: List[Tuple[int, int] | None] : The list of all moveable locations of
            given piece on piece_coords.
            move_count: int : The move number currently going on.

        Return:
            List[Tuple[int, int] | None] : All the filtered locations.
        """
        occupied_square_cache = self.occupied_squares.copy()
        piece_on_coords = self.occupied_squares[piece_coords]
        for locations in to_filter[:]:
            self.occupied_squares.pop(piece_coords)
            self.occupied_squares[locations] = piece_on_coords
            if self.IsOwnKingAttacked(move_count=move_count):
                to_filter.remove(locations)
            self.occupied_squares = occupied_square_cache.copy()
        return to_filter

    def PawnMoveAddress(
        self, piece_coords: Tuple[int, int], move_count: int
    ) -> List[Tuple[int, int] | None]:
        """
        Creates all possible locations a pawn can move to.

        Args:
            piece_coords: Tuple[int, int] : The location of the pawn piece to
            be modified.
            move_count: int : The move number currently going on.

        Return:
            List[Tuple[int, int] | None] : Gives all the possible squares a pawn on given
            piece_coords can move to.
        """
        own_color = "W" if move_count % 2 == 0 else "B"
        moving_address, capturing_address = PawnAddress(
            sq_coords=piece_coords, move_count=move_count
        )
        if not moving_address:
            pass
        elif moving_address[0] in self.occupied_squares:
            moving_address.clear()
        elif moving_address[1] in self.occupied_squares or not (
            (piece_coords[1] == 6 and own_color == "W")
            or (piece_coords[1] == 1 and own_color == "B")
        ):
            moving_address.pop(1)
        for locations in capturing_address[:]:
            if (
                locations not in self.occupied_squares
                or self.occupied_squares[locations][0] == own_color
            ):
                capturing_address.remove(locations)
        return self.SquaresThatPutKingInCheckRemover(
            piece_coords=piece_coords,
            to_filter=moving_address,
            move_count=move_count,
        ) + self.SquaresThatPutKingInCheckRemover(
            piece_coords=piece_coords,
            to_filter=capturing_address,
            move_count=move_count,
        )

    def KnightMoveAddress(
        self, piece_coords: Tuple[int, int], move_count: int
    ) -> List[Tuple[int, int] | None]:
        """
        Creates all possible locations a knight can move to.

        Args:
            piece_coords: Tuple[int, int] : The location of the knight piece to
            be modified.
            move_count: int : The move number currently going on.

        Return:
            List[Tuple[int, int] | None] : Gives all the possible squares a knight on given
            piece_coords can move to.
        """
        own_color = "W" if move_count % 2 == 0 else "B"
        move_address = KnightAddress(sq_coords=piece_coords)
        for locations in move_address[:]:
            if (
                locations in self.occupied_squares
                and self.occupied_squares[locations][0] == own_color
            ):
                move_address.remove(locations)
        return self.SquaresThatPutKingInCheckRemover(
            piece_coords=piece_coords,
            to_filter=move_address,
            move_count=move_count,
        )

    # Not used the  self.SquaresThatPutKingInCheckRemover because,
    # it is not needed and produces unexpected results.
    def KingMoveAddress(
        self, piece_coords: Tuple[int, int], move_count: int
    ) -> List[Tuple[int, int] | None]:
        """
        Creates all possible locations a king can move to.

        Args:
            piece_coords: Tuple[int, int] : The location of the king piece to
            be modified.
            move_count: int : The move number currently going on.

        Return:
            List[Tuple[int, int] | None] : Gives all the possible squares a king on given
            piece_coords can move to.
        """
        own_color = "W" if move_count % 2 == 0 else "B"
        move_address = KingAddress(sq_coords=piece_coords)
        for locations in move_address[:]:
            if (
                (
                    locations in self.occupied_squares
                    and self.occupied_squares[locations][0] == own_color
                )
                or self.AttackedByKing(
                    location_to_check=locations, move_count=move_count
                )
                or self.AttackedByNonSlidingPieces(
                    location_to_check=locations, move_count=move_count
                )
                or self.AttackedBySlidingPieces(
                    location_to_check=locations, move_count=move_count
                )
            ):
                move_address.remove(locations)
        return move_address

    def SlidingAddressMaker(
        self,
        piece_coords: Tuple[int, int],
        move_count: int,
        piece_type: Literal["Ax", "Qu"],
    ) -> List[Tuple[int, int] | None]:
        """
        Creates all possible locations a pawn can move to.

        Args:
            piece_coords: Tuple[int, int] : The location of the pawn piece to
            be modified.
            move_count: int : The move number currently going on.
            piece_type: Literal["Ax", "Qu"] : If the piece is straight moving["Ax"] or
            diagonal moving["Qu"]

        Return:
            List[Tuple[int, int] | None] : Gives all the possible squares a pawn on given
            piece_coords can move to.
        """
        own_color = "W" if move_count % 2 == 0 else "B"
        address1, address2 = (
            AxialAddress(sq_coords=piece_coords, occupied_squares=self.occupied_squares)
            if piece_type == "Ax"
            else QuadrantalAddress(
                sq_coords=piece_coords, occupied_squares=self.occupied_squares
            )
        )
        for addresses in [address1, address2]:
            for location_index in [0, -1]:
                if not addresses:
                    continue
                if (
                    addresses[location_index] in self.occupied_squares
                    and self.occupied_squares[addresses[location_index]][0] == own_color
                ):
                    addresses.pop(location_index)
        return self.SquaresThatPutKingInCheckRemover(
            piece_coords=piece_coords,
            to_filter=address1,
            move_count=move_count,
        ) + self.SquaresThatPutKingInCheckRemover(
            piece_coords=piece_coords,
            to_filter=address2,
            move_count=move_count,
        )


class Main(MoveAddress):
    """
    The main class that interfaces with the user.
    """

    def __init__(self) -> None:
        self.occupied_squares = {
            (0, 6): "WPawn",
            (1, 6): "WPawn",
            (2, 6): "WPawn",
            (3, 6): "WPawn",
            (4, 6): "WPawn",
            (5, 6): "WPawn",
            (6, 6): "WPawn",
            (7, 6): "WPawn",
            (0, 7): "WRook",
            (7, 7): "WRook",
            (1, 7): "WKnight",
            (6, 7): "WKnight",
            (2, 7): "WBishop",
            (5, 7): "WBishop",
            (3, 7): "WQueen",
            (4, 7): "WKing",
            (0, 1): "BPawn",
            (1, 1): "BPawn",
            (2, 1): "BPawn",
            (3, 1): "BPawn",
            (4, 1): "BPawn",
            (5, 1): "BPawn",
            (6, 1): "BPawn",
            (7, 1): "BPawn",
            (0, 0): "BRook",
            (7, 0): "BRook",
            (1, 0): "BKnight",
            (6, 0): "BKnight",
            (2, 0): "BBishop",
            (5, 0): "BBishop",
            (3, 0): "BQueen",
            (4, 0): "BKing",
        }
        self.move_count = 0
        self.move_address = []
        super().__init__(occupied_squares=self.occupied_squares)
        pieces = ["Pawn", "Rook", "Knight", "Bishop", "Queen", "King"]
        self.loaded_images = []
        img_size = 65, 65
        for side in "WB":
            for piece_type in pieces:
                path = f"Assets\\Pieces\\{side}Pieces\\{side}{piece_type}.png"
                image = pygame.image.load(path)
                self.loaded_images.append(pygame.transform.scale(image, img_size))

    def Logic(self, mouse_grid_pos: Tuple[int, int]) -> None:
        """
        Generates appropriate possible moves of the piece on the
        given mouse grid pos.

        Args:
            mouse_grid_pos: Tuple[int, int] : The grid location of the user click.

        Return:
            None : None
        """
        own_color = "W" if self.move_count % 2 == 0 else "B"
        if (
            mouse_grid_pos not in self.occupied_squares
            or self.occupied_squares[mouse_grid_pos][0] != own_color
        ):
            self.move_address = []
        elif self.occupied_squares[mouse_grid_pos][1:] == "Pawn":
            self.move_address = self.PawnMoveAddress(
                piece_coords=mouse_grid_pos, move_count=self.move_count
            )
        elif self.occupied_squares[mouse_grid_pos][1:] == "Knight":
            self.move_address = self.KnightMoveAddress(
                piece_coords=mouse_grid_pos, move_count=self.move_count
            )
        elif self.occupied_squares[mouse_grid_pos][1:] == "King":
            self.move_address = self.KingMoveAddress(
                piece_coords=mouse_grid_pos, move_count=self.move_count
            )
        elif self.occupied_squares[mouse_grid_pos][1:] == "Rook":
            self.move_address = self.SlidingAddressMaker(
                piece_coords=mouse_grid_pos, move_count=self.move_count, piece_type="Ax"
            )
        elif self.occupied_squares[mouse_grid_pos][1:] == "Bishop":
            self.move_address = self.SlidingAddressMaker(
                piece_coords=mouse_grid_pos, move_count=self.move_count, piece_type="Qu"
            )
        elif self.occupied_squares[mouse_grid_pos][1:] == "Queen":
            self.move_address = self.SlidingAddressMaker(
                piece_coords=mouse_grid_pos, move_count=self.move_count, piece_type="Ax"
            ) + self.SlidingAddressMaker(
                piece_coords=mouse_grid_pos, move_count=self.move_count, piece_type="Qu"
            )
