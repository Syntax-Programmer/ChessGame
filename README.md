This is a GUI based Chess game.

__autor__: Anand Maurya/ Syntax-Programmer

This code was a solo project meant for learning purposes.
This code has made me learn so many crucial concepts and I plan on updating it adding new features.

Each function is well-documented and has important comments where needed.
If any better ways are availiable I would be more than welcom to learn.
As I am a beginner I don't currently use any significant modules. So the code might be imporved upon.


To run:
  1. Open the Main.py file.
  2. Run the code.
  3. The game should be up running.
  If any issues found please contact.


Basic summary of the code:
  1. The game loop is running and constantly checks for user clicks.
  2. If click is performed the mouse pos is recorded and proccessed to represent a square:
      Eg:
         (259, 555) is proccessed to (2, 5)
  3. The main.Logic function takes the grid location(Eg:(2,5)) and checks if a move can be performed or not.
  4. If a move is not possible then the function ends.
  5. if a move is possible then:
       1. We create a general all theoretically possible moves.
       2. We remove those squares from the general move address that are the same side pieces.
       3. Then we check for each created location that if moving there may cause check to our own king,
          if yes then we remove that square from the move address.
       4. We return the finally proccessed move address. Note: This address can be a empty list also.
       Note:
         1. The functions not associated to a class create the general address of the piece.
         2. The class Attacked() checks if a provide square is attacked by any opponent piece.
         3. The class MoveAddress() inherits from Attacked() and creates he final proccessed address.
         4. The class MoveAddress() is inherited by class Main() which interfaces with the user.
  6. If move address created is a empty list then nothing shall happen.
  7. If move address cretated has squares then if then till the user does not click nothing will happen.
  8. If user clicked on a square that is in the move address then the respective piece moves there.
  9. If user clicked somewhere else then we try to create a move address for the clicked location.
  10. If no move address could be crafted the all the game state variables are reset and we again look for click.
  11. If move address is made then we discard the previos one and begin displaying the new one.

Important Points:
  1. The functions in the Main.py file has global scope privileges.
  2. No functions or method under any circumstance should have access to the global scope of Main.py.

Each function is tried and tested with every case possible.
Still if any issuses persist please refer to the documentation or contact me.
  
  
