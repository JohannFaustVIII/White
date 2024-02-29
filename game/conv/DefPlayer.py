from Map import Map
from Player import Player

# alpha-beta algorithm, an oponnent for NN to learn at the begin
class DefPlayer(Player):

   def __init__(self, depth : int = 1, verbose : bool = False) -> None:
      super().__init__()
      self.__depth = depth
      self.__verbose = verbose

   def get_move(self, map : Map, first_player : bool) -> list[int]:
      self.first_player = first_player
      computed_moves, _ = self.compute_moves(map, first_player, self.__depth)

      if self.__verbose:
         print(f'Def player moves = {computed_moves}')

      return computed_moves

   def compute_moves(self, map, first_player, depth, alpha : int = -10**7, beta : int = 10**7):

      distance = [self.compute_distance_to_own_gate(depth, first_player, map)]

      if depth == 0:
         return None, distance

      compare_function = max if (self.__depth - depth) % 2 == 0 else min # we want to maximize, when the enemy wants to minimize
      final_moves = []
      final_result = None

      moves = [map.get_possible_moves(first_player)]
      indexes = [0]

      while moves:

         index = indexes[-1]

         map.make_move(moves[-1][index], first_player)

         is_final = False
         if map.is_end_of_game():
            if map.is_goal(self.first_player): # is it correct?
               move_value = [10**3]
            else:
               move_value = [-10**3]
            is_final = True
         elif map.is_continuous_move_possible():
            moves.append(map.get_possible_moves(first_player))
            indexes.append(0)
            continue
         else:
            
            _, move_value = self.compute_moves(map, not first_player, depth - 1, alpha, beta)
            if depth == self.__depth:
               print(f'Depth = {depth}, moves = {[moves[i][indexes[i]] for i in range(len(indexes))]}, move_value = {move_value}, distance = {distance}')

         alpha, beta, ignore, result = self.compute_alpha_and_beta(depth, alpha, beta, move_value)
         # if is_final:
         #    print(depth, alpha, beta, ignore, result)
         if result != None:
            result = result + distance
         if depth == self.__depth:
            print(f'Previous final_result = {final_result}, final_moves = {final_moves}')
         final_result, final_moves = self.compute_final(ignore, result, moves, indexes, compare_function, final_result, final_moves)
         if depth == self.__depth:
            print(f'New final_result = {final_result}, final_moves = {final_moves}')

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

         if value == None:
            ignore_value = True

         # TODO: fix the code below, as it doesn't optimize anything
         # if not ignore_value:
         #    if (self.__depth - depth) % 2 == 0:
         #       if value[0] > beta:
         #          ignore_value = True
         #       else:
         #          alpha = max(alpha, value[0])
         #    else:
         #       if value[0] < alpha:
         #          ignore_value = True
         #       else:
         #          beta = min(beta, value[0])

         return alpha, beta, ignore_value, value

   def compute_final(self, ignore, result, moves, indexes, compare_function, final_result, final_moves):
      if ignore:
         return final_result, final_moves
      
      if final_result == None:
         final_result = result
         final_moves = [moves[i][indexes[i]] for i in range(len(indexes))]
      else:
         index = 0
         while index < len(final_result) and final_result[index] == result[index]:
            index += 1
         if index < len(final_result):
            final_val = compare_function(final_result[index], result[index])

            if final_val == result[index]:
               final_result = result
               final_moves = [moves[i][indexes[i]] for i in range(len(indexes))]

      return final_result, final_moves