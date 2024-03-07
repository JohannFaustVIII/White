from Map import Map
from Player import Player

# alpha-beta algorithm, an oponnent for NN to learn at the begin
class DefPlayer(Player):

   moves_memory = {}

   def __init__(self, depth : int = 1, verbose : bool = False, use_memory : bool = False) -> None:
      super().__init__()
      self.__depth = depth
      self.__verbose = verbose
      self.__use_memory = use_memory

   def get_move(self, map : Map, first_player : bool) -> list[int]:
      self.first_player = first_player
      computed_moves, _ = self.compute_moves(map, first_player, self.__depth)

      if self.__verbose:
         print(f'Def player moves = {computed_moves}')

      return computed_moves

   def compute_moves(self, map, first_player, depth, alpha : int = -10**7, beta : int = 10**7):

      if self.__use_memory:
         __state = map.get_points(first_player)
         t_state = tuple([tuple(s) for s in __state]) 
         if t_state in DefPlayer.moves_memory:
            saved_value = DefPlayer.moves_memory[t_state]
            if len(saved_value[1]) > depth and len(saved_value[0]) > 0:
               return saved_value


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

         alpha, beta, ignore, result, full_ignore = self.compute_alpha_and_beta(depth, alpha, beta, move_value)

         if full_ignore:
            while indexes and moves:
               map.revert_move(moves[-1][indexes[-1]], first_player)
               indexes.pop()
               moves.pop()
            return None, None

         if result != None:
            result = result + distance
         final_result, final_moves = self.compute_final(ignore, result, moves, indexes, compare_function, final_result, final_moves)

         map.revert_move(moves[-1][index], first_player)

         indexes[-1] += 1
         while indexes and moves and indexes[-1] >= len(moves[-1]):
            indexes.pop()
            moves.pop()
            
            if indexes and moves:
               map.revert_move(moves[-1][indexes[-1]], first_player)
               indexes[-1] += 1

      if depth == self.__depth and len(final_moves) == 0:
         print('DefPlayer chooses first possible move')
         final_moves = [map.get_possible_moves(first_player)]

      if self.__use_memory:
         __state = map.get_points(first_player)
         t_state = tuple([tuple(s) for s in __state])
         DefPlayer.moves_memory[t_state] = (final_moves, final_result)

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
         full_ignore = False

         if value == None:
            ignore_value = True

         if not ignore_value:
            if (self.__depth - depth) % 2 == 0:
               if value[0] > beta:
                  full_ignore = True
               else:
                  alpha = max(alpha, value[0])
            else:
               if value[0] < alpha:
                  full_ignore = True
               else:
                  beta = min(beta, value[0])

         return alpha, beta, ignore_value, value, full_ignore

   def compute_final(self, ignore, result, moves, indexes, compare_function, final_result, final_moves):
      if ignore:
         return final_result, final_moves
      
      if final_result == None:
         final_result = result
         final_moves = [moves[i][indexes[i]] for i in range(len(indexes))]
      else:
         index = 0
         while index < len(result) and index < len(final_result) and final_result[index] == result[index]:
            index += 1
         if index < len(final_result) and index < len(result):
            final_val = compare_function(final_result[index], result[index])

            if final_val == result[index]:
               final_result = result
               final_moves = [moves[i][indexes[i]] for i in range(len(indexes))]
         elif len(result) > len(final_result):
            final_result = result
            final_moves = [moves[i][indexes[i]] for i in range(len(indexes))]

      return final_result, final_moves
   
   def get_name(self) -> str:
      return "DefPlayer"