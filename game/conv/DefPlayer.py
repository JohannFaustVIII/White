from Map import Map
from Player import Player

# alpha-beta algorithm, an oponnent for NN to learn at the begin
class DefPlayer(Player):

   def __init__(self, depth : int = 1, verbose : bool = False) -> None:
      super().__init__()
      self.__depth = depth
      self.__verbose = verbose

   def get_move(self, map : Map, first_player : bool) -> list[int]:
      computed_moves, _ = self.compute_moves(map, first_player, self.__depth)

      if self.__verbose:
         print(f'Def player moves = {computed_moves}')

      return computed_moves

   def compute_moves(self, map, first_player, depth, alpha : int = -10**7, beta : int = 10**7):

      compare_function = max if (self.__depth - depth) % 2 == 0 else min # we want to maximize, when the enemy wants to minimize
      final_moves = []
      final_result = -10**7 if (self.__depth - depth) % 2 == 0 else 10**7 # FIXME: WHAT IF NO OPTION IS GENERATED?

      moves = [map.get_possible_moves(first_player)]
      indexes = [0]

      while moves:

         index = indexes[-1]

         map.make_move(moves[-1][index], first_player)

         if map.is_end_of_game():
            if map.is_goal(first_player): # is it correct?
               move_value = 10**3 + depth if (self.__depth - depth) % 2 == 0 else -10**3 - depth
            else:
               move_value = -10**3 - depth if (self.__depth - depth) % 2 == 0 else 10**3 + depth
         elif map.is_continuous_move_possible():
            moves.append(map.get_possible_moves(first_player))
            indexes.append(0)
            continue
         elif depth <= 1:
            move_value = self.compute_distance_to_own_gate(depth, first_player, map)


            
         else:
            _, move_value = self.compute_moves(map, not first_player, depth - 1, alpha, beta)

         alpha, beta, ignore, result = self.compute_alpha_and_beta(depth, alpha, beta, move_value)
         final_result, final_moves = self.compute_final(ignore, result, moves, indexes, compare_function, final_result, final_moves)

         map.revert_move(moves[-1][index], first_player)

         indexes[-1] += 1
         while indexes and moves and indexes[-1] >= len(moves[-1]):
            indexes.pop()
            moves.pop()
            
            if indexes and moves:
               map.revert_move(moves[-1][indexes[-1]], first_player)
               indexes[-1] += 1

      return final_moves, final_result
   
   def compute_distance_to_own_gate(self, depth, first_player, map):
         side_to_compute = first_player if (self.__depth - depth) % 2 == 0 else not first_player

         dist_map = map.get_distance_map()

         compare_function = max if side_to_compute else min

         gate_y = compare_function([k[1] for k in dist_map.keys()])

         keys = [k for k in dist_map.keys() if k[1] == gate_y]

         _min_dist = min([dist_map[k] for k in keys])
         move_value = -1 * _min_dist

         return move_value


   def compute_alpha_and_beta(self, depth, alpha, beta, value):
         ignore_value = False

         if value == 10**7 or value == -10**7:
            ignore_value = True

         if not ignore_value:
            if (self.__depth - depth) % 2 == 0:
               if value > beta:
                  ignore_value = True
               else:
                  alpha = max(alpha, value)
            else:
               if value < alpha:
                  ignore_value = True
               else:
                  beta = min(beta, value)

         return alpha, beta, ignore_value, value

   def compute_final(self, ignore, result, moves, indexes, compare_function, final_result, final_moves):
      if ignore:
         return final_result, final_moves
      
      final_result = compare_function(final_result, result)
      if result == final_result:
         final_moves = [moves[i][indexes[i]] for i in range(len(indexes))]

      return final_result, final_moves