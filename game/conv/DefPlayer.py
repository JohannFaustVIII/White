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

      compare_function = max if (self.__depth - depth) % 2 == 0 else min # we want to maximize, when the enemy wants to minimize
      final_moves = []
      final_result = -10**7 if (self.__depth - depth) % 2 == 0 else 10**7 

      moves = [map.get_possible_moves(first_player)]
      indexes = [0]

      while moves:

         index = indexes[-1]

         map.make_move(moves[-1][index], first_player)

         if map.is_continuous_move_possible():
            moves.append(map.get_possible_moves(first_player))
            indexes = [0]
            continue
         
         # evaluate position, but what if depth is 0?
         if depth > 1:
            _res = self.compute_moves(map, not first_player, depth - 1)
         else:
            # this requires to analyze the situation on the map
            # and save it in an variable
            pass
         map.revert_move(moves[-1][index], first_player)

         indexes[-1] += 1
         while indexes and moves and indexes[-1] >= len(moves[-1]):
            indexes.pop()
            moves.pop()
            
            map.revert_move(moves[-1][indexes[-1]], first_player)
            indexes[-1] += 1

      # return the best, currently saved option

      pass