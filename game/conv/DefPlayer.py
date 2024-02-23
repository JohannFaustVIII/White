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
      final_result = -10**7 if (self.__depth - depth) % 2 == 0 else 10**7 

      moves = [map.get_possible_moves(first_player)]
      indexes = [0]

      while moves:

         index = indexes[-1]

         map.make_move(moves[-1][index], first_player)

         if map.is_end_of_game():
            if map.is_goal(first_player): # is it correct?
               move_value = 10**3 if (self.__depth - depth) % 2 == 0 else -10**3
            else:
               move_value = -10**3 if (self.__depth - depth) % 2 == 0 else 10**3
            final_result = compare_function(final_result, move_value)
            if move_value == final_result:
               final_moves = [moves[i][indexes[i]] for i in range(len(indexes))]
         elif map.is_continuous_move_possible():
            moves.append(map.get_possible_moves(first_player))
            indexes.append(0)
            continue
         elif depth <= 1:
            side_to_compute = first_player if (self.__depth - depth) % 2 == 0 else not first_player

            dist_map = map.get_distance_map()

            _cf = max if side_to_compute else min

            gate = _cf([k[1] for k in dist_map.keys()])

            keys = [k for k in dist_map.keys() if k[1] == gate]

            _min_dist = min([dist_map[k] for k in keys])
            _res = -1 * _min_dist

            result = _res
            final_result = compare_function(final_result, result)
            if result == final_result:
               final_moves = [moves[i][indexes[i]] for i in range(len(indexes))]
            pass
         else:
            _, result = self.compute_moves(map, not first_player, depth - 1, alpha, beta)

            # TODO: FIX BELOW AND FIX FOR INSTANT WIN OPTION
            if (self.__depth - depth) % 2 == 0:
               if result > beta:
                  while moves:
                     _ei = indexes[-1]
                     _em = moves[-1][_ei]
                     map.revert_move(_em, first_player)
                     indexes.pop()
                     moves.pop()
                  return final_moves, final_result
               alpha = max(alpha, result)
            else:
               if result < alpha:
                  while moves:
                     _ei = indexes[-1]
                     _em = moves[-1][_ei]
                     map.revert_move(_em, first_player)
                     indexes.pop()
                     moves.pop()
                  return final_moves, final_result
               beta = min(beta, result)    

            final_result = compare_function(final_result, result)
            if result == final_result:
               final_moves = [moves[i][indexes[i]] for i in range(len(indexes))]

         map.revert_move(moves[-1][index], first_player)

         indexes[-1] += 1
         while indexes and moves and indexes[-1] >= len(moves[-1]):
            indexes.pop()
            moves.pop()
            
            if indexes and moves:
               map.revert_move(moves[-1][indexes[-1]], first_player)
               indexes[-1] += 1

      # return the best, currently saved option

      return final_moves, final_result