from Map import Map
from Player import Player

# alpha-beta algorithm, an oponnent for NN to learn at the begin
class DefPlayer(Player):

   def __init__(self, depth : int = 1) -> None:
      super().__init__()
      self.__depth = depth

   def get_moves(self, map : Map, first_player : bool) -> list[int]:
      computed_moves = self.compute_moves(map, first_player, self.__depth)

      pass

   def compute_moves(self, map, first_player, depth):

      # TODO: it lacks alpha-beta optimization, it requires alpha and beta levels, to drop further checks if not possible to pick

      compare_function = max if (depth - _d) % 2 == 0 else min # we want to maximize, when the enemy wants to minimize
      final_moves = []
      final_result = -10**7 if (depth - _d) % 2 == 0 else 10**7 


      for k in map.get_possible_moves(first_player):
         
         map.make_move(k, first_player)

         # compute how good the move is

         if map.is_end_of_game():
            # check who win, as it may be the best/worst option
            pass
         else:
            _d = depth
            _f = first_player

            while map.is_continuous_move_possible():
               # and here should be the loop to go as deep as possible
               # after reaching "the end" - move not possible or end of game
               # it should be evaluated
               #  - if end of game, it is pretty easy
               #  - if enemy's move, THEN should be the method called for the player
               # after that, move one step backward, and check other options
               # repeat the process of reaching "the end" and evaluation
               # DFS with extra steps 
               pass

            if not map.is_continuous_move_possible():
               _d -= 1
               _f = not first_player
            
            if _d == 0:
               # compute how good the current state is for us
               pass
            else:
               # and below is a problem, because of possible method call limit
               _res = self.compute_moves(map, _f, _d) # the result should be saved, it will be moves + value
               # and then, it will be k + _res and compare with other options?


         map.revert_move(k, first_player)


      # return the best, currently saved option



      pass