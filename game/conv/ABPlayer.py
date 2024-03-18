from Map import Map
from Player import Player

# alpha-beta algorithm, an oponnent for NN to learn at the begin
class ABPlayer(Player):

   moves_memory = {}
   
   def __init__(self, depth : int = 1, verbose : bool = False, use_memory : bool = False) -> None:
      super().__init__()
      self.__depth = depth
      self.__verbose = verbose
      self.__use_memory = use_memory

      self.__memory_reads = 0
      self.__memory_returns = 0
      self.__memory_saves = 0
      self.__depth_counter = {3 : 0, 2 : 0, 1 : 0, 0 : 0}

   def get_move(self, map : Map, first_player : bool) -> list[int]:
      self.first_player = first_player
      starting_map = map.get_tuple_state(first_player)
      computed_moves, _ = self.compute_moves(map, first_player, self.__depth)
      end_map = map.get_tuple_state(first_player)

      if any(starting_map[i] != end_map[i] for i in range(len(starting_map))):
         print(f'~~~ {self.get_name()} changed map!!! ~~~')

      if self.__verbose:
         print(f'{self.get_name()} moves = {computed_moves}')

      return computed_moves

   def compute_moves(self, map, first_player, depth, alpha : int = -10**7, beta : int = 10**7):

      if self.__use_memory:
         t_state = map.get_tuple_state(first_player)
         saved_value = self.get_from_memory(t_state)
         if saved_value:
            self.__memory_reads += 1
            if len(saved_value[1]) > depth and len(saved_value[0]) > 0:
               if self.__verbose:
                  print(f'{self.get_name()} - Value read and returned from memory.')
               self.__memory_returns += 1
               return saved_value
            else:
               if self.__verbose:
                  print(f'{self.get_name()} - Value read, but not returned.')

      self.__depth_counter[depth] += 1

      distance = [self.compute_distance(depth, first_player, map)]

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

         if map.is_end_of_game():
            if map.is_goal(self.first_player): # is it correct?
               move_value = [10**3]
            else:
               move_value = [-10**3]
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
         if self.__verbose:
            print('{self.get_name()} chooses first possible move')
         final_moves = [map.get_possible_moves(first_player)]

      if self.__use_memory:
         self.__memory_saves += 1
         if self.__verbose:
            print(f'{self.get_name()} - Value saved into memory.')
         t_state = map.get_tuple_state(first_player)
         self.put_in_memory(t_state, (final_moves, final_result))

      return final_moves, final_result
   
   def compute_distance(self, depth, first_player, map):
         pass


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
      pass
   
   def get_stats(self) -> list:
      __result =  [
         f'End memory size: {self.get_memory_size()}', 
         f'Memory reads: {self.__memory_reads}',
         f'Memory returns: {self.__memory_returns}',
         f'Memory saves: {self.__memory_saves}',
      ]

      __result += [f'Depth {k} calls: {self.__depth_counter[k]}' for k in self.__depth_counter.keys()]

      return __result
   
   def get_from_memory(self, state):
      pass

   def put_in_memory(self, state, value):
      pass

   def get_memory_size(self):
      pass