Chess Game

Overview:
This GUI-based chess game is a solo project developed by Anand Maurya (Syntax-Programmer) for learning purposes. The project aims to implement a fully functional chess game with a graphical user interface using Python.

Features:
  1. User-friendly graphical interface.
  2. Implemented chess logic including legal move generation and check detection.
  3. Supports basic chess functionalities such as castling and pawn promotion.
  4. Thoroughly tested for various edge cases to ensure correctness.
  5. Well-documented code with detailed comments explaining the logic behind each function.
  6. No external dependencies used, making it easy to set up and run.

Control Flow Summary:
  1. The game loop constantly checks for user clicks.
  2. When a click occurs, the mouse position is recorded and processed to represent a square on the board.
  3. The Logic function takes the grid location (e.g., (2, 5)) and checks if a move can be performed.
  4. If a move is not possible, the function ends.
  5. If a move is possible, the following steps are taken:
    1. Generate all theoretically possible moves.
    2. Remove squares with the same side pieces.
    3. Check each potential move to see if it would cause a check to the own king; if so, remove that square from the move address.
    4 .Return the processed move address.
  6. If the move address is empty, nothing happens.
  7. If the move address is not empty, the game waits for user input (click).
  8.If the user clicks on a square in the move address, the respective piece moves there.
  9. If the user clicks elsewhere, attempt to create a move address for the clicked location.
  10. If no move address could be created, reset all game state variables and wait for another click.
  11. If a move address is created, discard the previous one and display the new one.

How to Run
To run the game:

  1. Open the Main.py file.
  2. Execute the code.
  3. The chess game should start running.
     
Contribution Guidelines: 
  Contributions to the project are welcome! If you have any suggestions, bug fixes, or new features to add, please follow these steps:

  1. Fork the repository.
  2. Create a new branch for your feature or bug fix.
  3. Make your changes and test them thoroughly.
  4. Submit a pull request with a clear description of your changes.

Known Issues: 
  [List any known issues or limitations of the current implementation, if applicable.]

License:
  This project is licensed under the LICENSE.py. See the LICENSE file for details.

Contact:  
  For any issues or inquiries, please contact Anand Maurya at anand6308anand@gamil.com.
