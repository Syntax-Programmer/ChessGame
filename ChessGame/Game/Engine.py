"""
This module handles the creation of the all possible moveable
locations of a piece and checking for attacks from opponent pieces 
on any square.

Author: Anand Maurya
Github: Syntax-Programmer
Email: anand6308anand@gmail.com
"""

__author__ = "Anand Maurya/ Syntax-Programmer"
__email__ = "anand6308anand@gmail.com"


from typing import List, Tuple, Dict, Literal


INT_RANGE = Literal[0, 1, 2, 3, 4, 5, 6, 7]


def pawn_address(
    sq_index: Tuple[INT_RANGE, INT_RANGE], move_count: int
) -> Tuple[
    List[Tuple[INT_RANGE, INT_RANGE] | None], List[Tuple[INT_RANGE, INT_RANGE] | None]
]:
    """
    Creates a general movable locations of a pawn.

    Takes in a sq_index and creates all possible locations a pawn on that given sq_index can move to.\n
    OR\n
    An opponent pawn on the created locations can attack the provided sq_index.

    Parameters:
    ----------
    1. sq_index : Tuple[INT_RANGE, INT_RANGE]
        A location on the board w.r.t the address is to be made.
    2. move_count : int
        The move number going on.

    Returns:
    -------
    Tuple[\n
    List[Tuple[INT_RANGE, INT_RANGE] | None], \n
    List[Tuple[INT_RANGE, INT_RANGE] | None]\n
    ] :\n
        Creates two lists :\n
        1. List1 : A pawn on the provided sq_index can move to.\n
        2. List2 : A pawn on the provided sq_index can capture an opponent piece to,\n
                OR\n
                An opponent pawn on the created locations can attack the provided sq_index.
    """
    movement_direction = -1 if move_count % 2 == 0 else 1
    moving_address = [
        (sq_index[0], sq_index[1] + (step * movement_direction))
        for step in [1, 2]
        if sq_index[1] + (step * movement_direction) in range(8)
    ]
    capturing_address = [
        (sq_index[0] + step, sq_index[1] + movement_direction)
        for step in [1, -1]
        if sq_index[0] + step in range(8)
        and sq_index[1] + movement_direction in range(8)
    ]
    return moving_address, capturing_address


def knight_address(
    sq_index: Tuple[INT_RANGE, INT_RANGE]
) -> List[Tuple[INT_RANGE, INT_RANGE]]:
    """
    Creates a general movable locations of a knight.

    Takes in a sq_index and creates all possible locations a knight on that given sq_index can move to.\n
    OR\n
    An opponent knight on the created locations can attack the provided sq_index.

    Parameters:
    ----------
    1. sq_index : Tuple[INT_RANGE, INT_RANGE]
        A location on the board w.r.t the address is to be made.

    Returns:
    -------
    List[Tuple[INT_RANGE, INT_RANGE]] :
        Creates general move list where a knight on provided sq_index can move to.\n
        OR\n
        An opponent knight on the created squares can attack the given sq_index.
    """
    address = [
        (sq_index[0] + 2, sq_index[1] + 1),
        (sq_index[0] + 2, sq_index[1] - 1),
        (sq_index[0] - 2, sq_index[1] + 1),
        (sq_index[0] - 2, sq_index[1] - 1),
        (sq_index[0] + 1, sq_index[1] + 2),
        (sq_index[0] - 1, sq_index[1] + 2),
        (sq_index[0] + 1, sq_index[1] - 2),
        (sq_index[0] - 1, sq_index[1] - 2),
    ]
    return list(
        filter(
            lambda locations: locations[0] in range(8) and locations[1] in range(8),
            address,
        )
    )


def king_address(
    sq_index: Tuple[INT_RANGE, INT_RANGE]
) -> List[Tuple[INT_RANGE, INT_RANGE]]:
    """
    Creates a general movable locations of a king.

    Takes in a sq_index and creates all possible locations a king on that given sq_index can move to.\n
    OR\n
    An opponent king on the created locations can attack the provided sq_index.

    Parameters:
    ----------
    1. sq_index : Tuple[INT_RANGE, INT_RANGE]
        A location on the board w.r.t the address is to be made.

    Returns:
    -------
    List[Tuple[INT_RANGE, INT_RANGE]] :
        Creates general move list where a king on provided sq_index can move to.\n
        OR\n
        An opponent king on the created squares can attack the given sq_index.
    """
    address = [
        (sq_index[0] + 1, sq_index[1]),
        (sq_index[0] - 1, sq_index[1]),
        (sq_index[0], sq_index[1] + 1),
        (sq_index[0], sq_index[1] - 1),
        (sq_index[0] + 1, sq_index[1] - 1),
        (sq_index[0] - 1, sq_index[1] - 1),
        (sq_index[0] - 1, sq_index[1] + 1),
        (sq_index[0] + 1, sq_index[1] + 1),
    ]
    return list(
        filter(
            lambda locations: locations[0] in range(8) and locations[1] in range(8),
            address,
        )
    )


def sliding_address_filter(
    constructor: Tuple[INT_RANGE, INT_RANGE],
    to_filter: List[Tuple[INT_RANGE, INT_RANGE]],
    occupied_squares: Dict[Tuple[INT_RANGE, INT_RANGE], str],
) -> List[Tuple[INT_RANGE, INT_RANGE] | None]:
    """
    Filter the given general address of a sliding piece.

    Takes in a generally made sliding address and restricts it to only those squares
    that the piece on the provided constructor can move to.

    Parameters:
    ----------
    1. constructor : Tuple[INT_RANGE, INT_RANGE]
        A location on the board w.r.t the address was made.
    2. to_filter : List[Tuple[INT_RANGE, INT_RANGE]]
        A address that was made w.r.t constructor and is to be filtered.
    3. occupied_squares : Dict[Tuple[INT_RANGE, INT_RANGE], str]
        A dictionary of all the occupied squares mapped to the piece occupying that square.

    Returns:
    -------
    List[Tuple[INT_RANGE, INT_RANGE]] :
        The filtered address only containing the reachable squares
    """
    left_reach_index = 0
    right_reach_index = len(to_filter) - 1
    constructor_index = to_filter.index(constructor)
    for indices in range(len(to_filter)):
        if indices < constructor_index and to_filter[indices] in occupied_squares:
            left_reach_index = indices
        if indices > constructor_index and to_filter[indices] in occupied_squares:
            right_reach_index = indices
            # Because we need the first occurrence of a piece to the right of the gives constructor.
            break
    to_filter = to_filter[left_reach_index : right_reach_index + 1]
    # Because a piece can't move to it's own location.
    to_filter.remove(constructor)
    return to_filter


def straight_sliding_address(
    sq_index: Tuple[INT_RANGE, INT_RANGE],
    occupied_squares: Dict[Tuple[INT_RANGE, INT_RANGE], str],
) -> Tuple[
    List[Tuple[INT_RANGE, INT_RANGE] | None], List[Tuple[INT_RANGE, INT_RANGE] | None]
]:
    """
    Creates a general movable locations of a rook/queen.

    Takes in a sq_index and creates all possible locations a rook/queen on that given sq_index can move to.\n
    OR\n
    An opponent rook/queen on the created locations can attack the provided sq_index.

    Parameters:
    ----------
    1. sq_index : Tuple[INT_RANGE, INT_RANGE]
        A location on the board w.r.t the address is to be made.
    2. occupied_squares : Dict[Tuple[INT_RANGE, INT_RANGE], str]
        A dictionary of all the occupied squares mapped to the piece occupying that square.

    Returns:
    -------
    Tuple[
    List[Tuple[INT_RANGE, INT_RANGE] | None], List[Tuple[INT_RANGE, INT_RANGE] | None]
    ] :\n
        Creates two lists :\n
        1. List1 : All the reachable squares in the same row as the rook/queen.\n
                OR\n
                An opponent rook/queen on the created locations can attack the provided sq_index.\n
        2. List2 : All the reachable squares in the same col as the rook/queen.\n
                OR\n
                An opponent rook/queen on the created locations can attack the provided sq_index.
    """
    # No out of the board indices filter needed because it is already controlled.
    piece_row = [(x_pos, sq_index[1]) for x_pos in range(8)]
    piece_col = [(sq_index[0], y_pos) for y_pos in range(8)]
    return (
        sliding_address_filter(
            constructor=sq_index, to_filter=piece_row, occupied_squares=occupied_squares
        ),
        sliding_address_filter(
            constructor=sq_index, to_filter=piece_col, occupied_squares=occupied_squares
        ),
    )


def diagonal_sliding_address(
    sq_index: Tuple[INT_RANGE, INT_RANGE],
    occupied_squares: Dict[Tuple[INT_RANGE, INT_RANGE], str],
) -> Tuple[
    List[Tuple[INT_RANGE, INT_RANGE] | None], List[Tuple[INT_RANGE, INT_RANGE] | None]
]:
    """
    Creates a general movable locations of a bishop/queen.

    Takes in a sq_index and creates all possible locations a bishop/queen on that given sq_index can move to.
    OR
    An opponent bishop/queen on the created locations can attack the provided sq_index.

    Parameters:
    ----------
    1. sq_index : Tuple[INT_RANGE, INT_RANGE]
        A location on the board w.r.t the address is to be made.
    2. occupied_squares : Dict[Tuple[INT_RANGE, INT_RANGE], str]
        A dictionary of all the occupied squares mapped to the piece occupying that square.

    Returns:
    -------
    Tuple[
    List[Tuple[INT_RANGE, INT_RANGE] | None], List[Tuple[INT_RANGE, INT_RANGE] | None]
    ] :\n
        Creates two lists :\n
        1. List1 : All the reachable squares in the same anti-diagonal as the bishop/queen.\n
                OR\n
                An opponent rook/queen on the created locations can attack the provided sq_index.\n
        2. List2 : All the reachable squares in the same main-diagonal as the bishop/queen.\n
                OR\n
                An opponent rook/queen on the created locations can attack the provided sq_index.
    """
    piece_diagonal1 = [
        (sq_index[0] + step, sq_index[1] - step)
        for step in range(-7, 8)
        if sq_index[0] + step in range(8) and sq_index[1] - step in range(8)
    ]
    piece_diagonal2 = [
        (sq_index[0] + step, sq_index[1] + step)
        for step in range(-7, 8)
        if sq_index[0] + step in range(8) and sq_index[1] + step in range(8)
    ]
    return (
        sliding_address_filter(
            constructor=sq_index,
            to_filter=piece_diagonal1,
            occupied_squares=occupied_squares,
        ),
        sliding_address_filter(
            constructor=sq_index,
            to_filter=piece_diagonal2,
            occupied_squares=occupied_squares,
        ),
    )


class IsAttacked:
    """
    This class determines if a given square or the king is attacked by any opponent pieces on the chessboard.

    Attributes:
    ----------
    1. occupied_squares : Dict[Tuple[INT_RANGE, INT_RANGE], str]
        A dictionary of all the occupied squares mapped to the piece occupying that square.
    2. white_king_location : Tuple[INT_RANGE, INT_RANGE]
        The location of the white king.
    3. black_king_location : Tuple[INT_RANGE, INT_RANGE]
        The location of the black king.
    """

    def __init__(
        self, occupied_squares: Dict[Tuple[INT_RANGE, INT_RANGE], str]
    ) -> None:
        """
        Initializes an IsAttacked object.

        Parameters:
        ----------
        1. occupied_squares : Dict[Tuple[INT_RANGE, INT_RANGE], str]
            A dictionary of all the occupied squares mapped to the piece occupying that square.
        """
        self.occupied_squares = occupied_squares
        self.white_king_location = (4, 7)
        self.black_king_location = (4, 0)

    def attacked_by_non_sliding_pieces(
        self, location_to_check: Tuple[INT_RANGE, INT_RANGE], move_count: int
    ) -> bool:
        """
        Checks if the provided location_to_check is attacked by a pawn or a knight.

        Takes the location_to_check and creates all valid addresses and then checks for
        attacking piece in them.

        Parameters:
        ----------
        1. location_to_check : Tuple[INT_RANGE, INT_RANGE]
            A location on the board that has to be checked.
        2. move_count : int
            The move number going on.

        Returns:
        -------
        bool :
            True if the provided location_to_check is attacked by a pawn or a knight.
        """
        sq_pawn_attacking = pawn_address(
            sq_index=location_to_check, move_count=move_count
        )[1]
        sq_knight_attacking = knight_address(sq_index=location_to_check)
        opponent_color = "B" if move_count % 2 == 0 else "W"
        return any(
            self.occupied_squares.get(locations) == f"{opponent_color}Pawn"
            for locations in sq_pawn_attacking
        ) or any(
            self.occupied_squares.get(locations) == f"{opponent_color}Knight"
            for locations in sq_knight_attacking
        )

    def attacked_by_sliding_pieces(
        self, location_to_check: Tuple[INT_RANGE, INT_RANGE], move_count: int
    ) -> bool:
        """
        Checks if the provided location_to_check is attacked by a rook or a bishop or a queen.

        Takes the location_to_check and creates all valid addresses and then checks for
        attacking piece in them.

        Parameters:
        ----------
        1. location_to_check : Tuple[INT_RANGE, INT_RANGE]
            A location on the board that has to be checked.
        2. move_count : int
            The move number going on.

        Returns:
        -------
        bool :
            True if the provided location_to_check is attacked by a rook or a bishop or a queen.
        """
        piece_row, piece_col = straight_sliding_address(
            sq_index=location_to_check, occupied_squares=self.occupied_squares
        )
        piece_diagonal1, piece_diagonal2 = diagonal_sliding_address(
            sq_index=location_to_check, occupied_squares=self.occupied_squares
        )
        # The if-else used to correct the indexation error in empty address(if empty address was created).
        sq_straight_sliding_attacking, sq_diagonal_sliding_attacking = (
            ((piece_row[0], piece_row[-1]) if piece_row else ())
            + ((piece_col[0], piece_col[-1]) if piece_col else ()),
            ((piece_diagonal1[0], piece_diagonal1[-1]) if piece_diagonal1 else ())
            + ((piece_diagonal2[0], piece_diagonal2[-1]) if piece_diagonal2 else ()),
        )
        opponent_color = "B" if move_count % 2 == 0 else "W"
        return any(
            self.occupied_squares.get(locations)
            in [f"{opponent_color}Rook", f"{opponent_color}Queen"]
            for locations in sq_straight_sliding_attacking
        ) or any(
            self.occupied_squares.get(locations)
            in [f"{opponent_color}Bishop", f"{opponent_color}Queen"]
            for locations in sq_diagonal_sliding_attacking
        )

    def attacked_by_king(
        self, location_to_check: Tuple[INT_RANGE, INT_RANGE], move_count: int
    ) -> bool:
        """
        Checks if the provided location_to_check is attacked by a king.

        Takes the location_to_check and creates all valid addresses and then checks for
        attacking piece in them.

        Parameters:
        ----------
        1. location_to_check : Tuple[INT_RANGE, INT_RANGE]
            A location on the board that has to be checked.
        2. move_count : int
            The move number going on.

        Returns:
        -------
        bool :
            True if the provided location_to_check is attacked by a king.
        """
        opponent_color = "B" if move_count % 2 == 0 else "W"
        from_king_attacking = king_address(sq_index=location_to_check)
        return any(
            self.occupied_squares.get(locations) == f"{opponent_color}King"
            for locations in from_king_attacking
        )

    def is_own_king_attacked(self, move_count: int) -> bool:
        """
        Checks if the king of the current side is attacked.

        Takes the move count to determine the side and check if the king of that side is attacked.

        Parameters:
        ----------
        1. move_count : int
            The move number going on.

        Returns:
        -------
        bool :
            True if the king of the current side is attacked by every piece other than a king.
        """
        king_location = (
            self.white_king_location
            if move_count % 2 == 0
            else self.black_king_location
        )
        own_color = "W" if move_count % 2 == 0 else "B"
        # Check if the current king location is in consistent with the actual data.
        # If not then it corrects it.
        # Done like this to save computation.
        if self.occupied_squares.get(king_location) != f"{own_color}King":
            for locations in self.occupied_squares:
                if self.occupied_squares[locations] == f"{own_color}King":
                    king_location = locations
                    if own_color == "W":
                        self.white_king_location = locations
                    else:
                        self.black_king_location = locations
                    break
        return self.attacked_by_non_sliding_pieces(
            location_to_check=king_location, move_count=move_count
        ) or self.attacked_by_sliding_pieces(
            location_to_check=king_location, move_count=move_count
        )


class MoveList(IsAttacked):
    """
    This class determines all the possible locations that a piece on the provided square
    can move to.

    Attributes:
    ----------
    1. occupied_squares : Dict[Tuple[INT_RANGE, INT_RANGE], str]
        A dictionary of all the occupied squares mapped to the piece occupying that square.
    2. white_king_location : Tuple[INT_RANGE, INT_RANGE]
        The location of the white king.
    3. black_king_location : Tuple[INT_RANGE, INT_RANGE]
        The location of the black king.
    4. white_short_castle : bool
        The right of wether the white side can castle short.
    5. white_long_castle : bool
        The right of wether the white side can castle long.
    6. black_short_castle : bool
        The right of wether the black side can castle short.
    7. black_long_castle : bool
        The right of wether the black side can castle long.
    """

    def __init__(
        self, occupied_squares: Dict[Tuple[INT_RANGE, INT_RANGE], str]
    ) -> None:
        """
        Initializes an MoveList object.

        Parameters:
        ----------
        1. occupied_squares : Dict[Tuple[INT_RANGE, INT_RANGE], str]
            A dictionary of all the occupied squares mapped to the piece occupying that square.
        """
        self.white_short_castle = self.white_long_castle = True
        self.black_short_castle = self.black_long_castle = True
        super().__init__(occupied_squares=occupied_squares)

    def squares_that_put_king_in_check_remover(
        self,
        piece_location: Tuple[INT_RANGE, INT_RANGE],
        to_filter: List[Tuple[INT_RANGE, INT_RANGE] | None],
        move_count: int,
    ) -> List[Tuple[INT_RANGE, INT_RANGE] | None]:
        """
        Filters out all the squares that put king in check.

        The functions removes all the squares to which the piece on the provided piece_location
        if moves to puts their own king in check.

        Parameters:
        ----------
        1. piece_location : Tuple[INT_RANGE, INT_RANGE]
            A location of the piece w.r.t the to_filter was made.
        2. to_filter : List[Tuple[INT_RANGE, INT_RANGE] | None]
            A address that was made w.r.t piece_location.
        3. move_count : int
            The move number going on.

        Returns:
        -------
        List[Tuple[INT_RANGE, INT_RANGE] | None] :
            A single list of all the possible squares that piece on the provided piece_location
            can finally move to.
        """
        occupied_squares_cache = self.occupied_squares.copy()
        piece_present = self.occupied_squares[piece_location]
        for location in to_filter[:]:
            self.occupied_squares.pop(piece_location)
            self.occupied_squares[location] = piece_present
            if self.is_own_king_attacked(move_count=move_count):
                to_filter.remove(location)
            self.occupied_squares = occupied_squares_cache.copy()
        return to_filter

    def pawn_move_list(
        self, piece_location: Tuple[INT_RANGE, INT_RANGE], move_count: int
    ) -> List[Tuple[INT_RANGE, INT_RANGE] | None]:
        """
        Creates all the possible locations a piece on provided piece_location can move to.

        The general address of a pawn is filtered to remove squares holding the same side piece,
        squares that put the king in check and finally gives the list of locations a pawn on the
        provided piece_location can move to.

        Parameters:
        ----------
        1. piece_location : Tuple[INT_RANGE, INT_RANGE]
            A location of the piece w.r.t the address is to be made.
        2. move_count : int
            The move number going on.

        Returns:
        -------
        List[Tuple[INT_RANGE, INT_RANGE] | None] :
            A final list of locations that a pawn on the provided sq_index can move to.
        """
        own_color = "W" if move_count % 2 == 0 else "B"
        moving_list, capturing_list = pawn_address(
            sq_index=piece_location, move_count=move_count
        )
        if moving_list[0] in self.occupied_squares:
            moving_list.clear()
        elif moving_list[1] in self.occupied_squares or not (
            (piece_location[1] == 6 and own_color == "W")
            or (piece_location[1] == 1 and own_color == "B")
        ):
            moving_list.pop(1)
        capturing_list = list(
            filter(
                lambda locations: locations in self.occupied_squares
                and self.occupied_squares[locations][0] != own_color,
                capturing_list,
            )
        )
        return self.squares_that_put_king_in_check_remover(
            piece_location=piece_location, to_filter=moving_list, move_count=move_count
        ) + self.squares_that_put_king_in_check_remover(
            piece_location=piece_location,
            to_filter=capturing_list,
            move_count=move_count,
        )

    def knight_move_list(
        self, piece_location: Tuple[INT_RANGE, INT_RANGE], move_count: int
    ) -> List[Tuple[INT_RANGE, INT_RANGE] | None]:
        """
        Creates all the possible locations a piece on provided piece_location can move to.

        The general address of a knight is filtered to remove squares holding the same side piece,
        squares that put the king in check and finally gives the list of locations a knight on the
        provided piece_location can move to.

        Parameters:
        ----------
        1. piece_location : Tuple[INT_RANGE, INT_RANGE]
            A location of the piece w.r.t the address is to be made.
        2. move_count : int
            The move number going on.

        Returns:
        -------
        List[Tuple[INT_RANGE, INT_RANGE] | None] :
            A final list of locations that a knight on the provided sq_index can move to.
        """
        own_color = "W" if move_count % 2 == 0 else "B"
        move_list = knight_address(sq_index=piece_location)
        move_list = list(
            filter(
                lambda locations: locations not in self.occupied_squares
                or self.occupied_squares[locations][0] != own_color,
                move_list,
            )
        )
        return self.squares_that_put_king_in_check_remover(
            piece_location=piece_location, to_filter=move_list, move_count=move_count
        )

    def king_move_list(
        self, piece_location: Tuple[INT_RANGE, INT_RANGE], move_count: int
    ) -> List[Tuple[INT_RANGE, INT_RANGE] | None]:
        """
        Creates all the possible locations a piece on provided piece_location can move to.

        The general address of a king is filtered to remove squares holding the same side piece,
        squares that put the king in check and finally gives the list of locations a king on the
        provided piece_location can move to.

        Parameters:
        ----------
        1. piece_location : Tuple[INT_RANGE, INT_RANGE]
            A location of the piece w.r.t the address is to be made.
        2. move_count : int
            The move number going on.

        Returns:
        -------
        List[Tuple[INT_RANGE, INT_RANGE] | None] :
            A final list of locations that a king on the provided sq_index can move to.
        """

        def castle_move_list_maker(
            move_count: int,
        ) -> List[Tuple[INT_RANGE, INT_RANGE] | None]:
            """
            Creates those location where king moves to in a castle.

            Creates the general move_list and then filters it out according to the
            conditions of castling.

            Parameters:
            ----------
            1. move_count : int
                The move number going on.

            Returns:
            -------
            List[Tuple[INT_RANGE, INT_RANGE] | None] :
                A list of locations where the king can possibly castle to.
            """
            castle_table = {
                "W": {
                    (6, 7): [[(5, 7), (6, 7)], [(4, 7), (5, 7), (6, 7)]],
                    (2, 7): [[(3, 7), (2, 7), (1, 7)], [(4, 7), (3, 7), (2, 7)]],
                },
                "B": {
                    (6, 0): [[(5, 0), (6, 0)], [(4, 0), (5, 0), (6, 0)]],
                    (2, 0): [[(3, 0), (2, 0), (1, 0)], [(4, 0), (3, 0), (2, 0)]],
                },
            }
            short_right, long_right = (
                (self.white_short_castle, self.white_long_castle)
                if move_count % 2 == 0
                else (
                    self.black_short_castle,
                    self.black_long_castle,
                )
            )
            own_color = "W" if move_count % 2 == 0 else "B"
            row = 7 if move_count % 2 == 0 else 0
            move_list = [(6, row), (2, row)]
            if not short_right:
                move_list.pop(0)
            if not long_right:
                move_list.pop(-1)
            castle_data = castle_table[own_color]
            for locations in move_list[:]:
                castle_type_data = castle_data[locations]
                if any(
                    squares in self.occupied_squares for squares in castle_type_data[0]
                ) or any(
                    self.attacked_by_king(
                        location_to_check=squares, move_count=move_count
                    )
                    or self.attacked_by_non_sliding_pieces(
                        location_to_check=squares, move_count=move_count
                    )
                    or self.attacked_by_sliding_pieces(
                        location_to_check=squares, move_count=move_count
                    )
                    for squares in castle_type_data[1]
                ):
                    move_list.remove(locations)
            return move_list

        own_color = "W" if move_count % 2 == 0 else "B"
        move_list = king_address(sq_index=piece_location)
        move_list = list(
            filter(
                lambda locations: (
                    locations not in self.occupied_squares
                    or self.occupied_squares[locations][0] != own_color
                )
                and not self.attacked_by_king(
                    location_to_check=locations, move_count=move_count
                )
                and not self.attacked_by_non_sliding_pieces(
                    location_to_check=locations, move_count=move_count
                )
                and not self.attacked_by_sliding_pieces(
                    location_to_check=locations, move_count=move_count
                ),
                move_list,
            )
        )
        return move_list + castle_move_list_maker(move_count=move_count)

    def sliding_pieces_move_list(
        self,
        piece_location: Tuple[INT_RANGE, INT_RANGE],
        move_count: int,
        piece_type: Literal["s", "d"],
    ) -> List[Tuple[INT_RANGE, INT_RANGE] | None]:
        """
        Creates all the possible locations a piece on provided piece_location can move to.

        The general address of a rook/queen/bishop is filtered to remove squares holding the same side piece,
        squares that put the king in check and finally gives the list of locations a rook/queen/bishop on the
        provided piece_location can move to.

        Parameters:
        ----------
        1. piece_location : Tuple[INT_RANGE, INT_RANGE]
            A location of the piece w.r.t the address is to be made.
        2. move_count : int
            The move number going on.

        Returns:
        -------
        List[Tuple[INT_RANGE, INT_RANGE] | None] :
            A final list of locations that a rook/queen/bishop on the provided sq_index can move to.
        """
        own_color = "W" if move_count % 2 == 0 else "B"
        move_list1, move_list2 = (
            straight_sliding_address(
                sq_index=piece_location, occupied_squares=self.occupied_squares
            )
            if piece_type == "s"
            else diagonal_sliding_address(
                sq_index=piece_location, occupied_squares=self.occupied_squares
            )
        )
        move_list1, move_list2 = list(
            filter(
                lambda locations: locations not in self.occupied_squares
                or self.occupied_squares[locations][0] != own_color,
                move_list1,
            )
        ), list(
            filter(
                lambda locations: locations not in self.occupied_squares
                or self.occupied_squares[locations][0] != own_color,
                move_list2,
            )
        )
        return self.squares_that_put_king_in_check_remover(
            piece_location=piece_location,
            to_filter=move_list1,
            move_count=move_count,
        ) + self.squares_that_put_king_in_check_remover(
            piece_location=piece_location,
            to_filter=move_list2,
            move_count=move_count,
        )


class Main(MoveList):
    """
    This class is the main class that interfaces with the user input.

    Attributes:
    ----------
    1. occupied_squares : Dict[Tuple[INT_RANGE, INT_RANGE], str]
        A dictionary of all the occupied squares mapped to the piece occupying that square.
    2. white_king_location : Tuple[INT_RANGE, INT_RANGE]
        The location of the white king.
    3. black_king_location : Tuple[INT_RANGE, INT_RANGE]
        The location of the black king.
    4. move_count : int
        The current move number going on.
    5. white_short_castle : bool
        The right of wether the white side can castle short.
    6. white_long_castle : bool
        The right of wether the white side can castle long.
    7. black_short_castle : bool
        The right of wether the black side can castle short.
    8. black_long_castle : bool
        The right of wether the black side can castle long.
    9. move_list : List[Tuple[INT_RANGE, INT_RANGE] | None]
        The locations of possible movable locations of a given piece.
    """

    def __init__(self) -> None:
        """
        Initializes an Main object.
        """
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
        self.move_list = []
        self.move_list_mapping_table = {
            "Pawn": lambda location, move_count: self.pawn_move_list(
                piece_location=location, move_count=move_count
            ),
            "Rook": lambda location, move_count: self.sliding_pieces_move_list(
                piece_location=location,
                move_count=move_count,
                piece_type="s",
            ),
            "Knight": lambda location, move_count: self.knight_move_list(
                piece_location=location, move_count=move_count
            ),
            "Bishop": lambda location, move_count: self.sliding_pieces_move_list(
                piece_location=location,
                move_count=move_count,
                piece_type="d",
            ),
            "Queen": lambda location, move_count: self.sliding_pieces_move_list(
                piece_location=location,
                move_count=move_count,
                piece_type="s",
            )
            + self.sliding_pieces_move_list(
                piece_location=location,
                move_count=move_count,
                piece_type="d",
            ),
            "King": lambda location, move_count: self.king_move_list(
                piece_location=location, move_count=move_count
            ),
        }
        super().__init__(occupied_squares=self.occupied_squares)

    def logic(self, mouse_grid_pos: Tuple[INT_RANGE, INT_RANGE]) -> None:
        """
        This function takes in a user click pos and creates appropriate move list.

        Takes the user click pos and determines if the click is valid to act upon,
        if yes then then creates the appropriate move_list else the click is ignored.

        Parameters:
        ----------
        1. mouse_grid_pos: Tuple[INT_RANGE, INT_RANGE]
            The click of them user mapped to a certain square on the board.
        """

        own_color = "W" if self.move_count % 2 == 0 else "B"
        if (
            mouse_grid_pos not in self.occupied_squares
            or self.occupied_squares[mouse_grid_pos][0] != own_color
        ):
            self.move_list = []
        else:
            self.move_list = self.move_list_mapping_table[
                self.occupied_squares[mouse_grid_pos][1:]
            ](location=mouse_grid_pos, move_count=self.move_count)
