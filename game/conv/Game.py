from Map import Map
from Player import Player
import time

class Game:

    is_game_finished = False
    is_first_player_win = False
    is_second_player_win = False

    def __init__(self, first_player : Player, second_player : Player, register_moves : bool = False) -> None:
        self.__map = Map(8, 10)
        self.__first_player = first_player
        self.__second_player = second_player
        self.__fp_time = 0
        self.__sp_time = 0
        
        self.__register_moves = register_moves
        self.__first_player_states = []
        self.__second_player_states = []
    
    def play_game(self):
        is_first_player_move = True
        while not self.__map.is_end_of_game():
            start_time = time.time()
            move = self.__first_player.get_move(self.__map, True) if is_first_player_move else self.__second_player.get_move(self.__map, False)
            end_time = time.time()
            time_diff = end_time - start_time
            if is_first_player_move:
                self.__fp_time += time_diff
            else:
                self.__sp_time += time_diff
            if move.__class__ == list:
                if not move:
                    print(f'Moves were not generated, moves = {move}')
                self.__map.make_move(move[0], is_first_player_move)
                move.pop(0)
                while self.__map.is_continuous_move_possible() and move:
                    self.__map.make_move(move[0], is_first_player_move)
                    move.pop(0)
                if self.__map.is_continuous_move_possible():
                    print(f'Not enough moves generated')
                if move:
                    print(f'Moves not made: {move}')
                pass
            else:
                self.__map.make_move(move, is_first_player_move)
            if self.__register_moves:
                state = self.__map.get_points(is_first_player_move)
                self.__first_player_states.append(state) if is_first_player_move else self.__second_player_states.append(state)
            if not self.__map.is_continuous_move_possible() and not self.__map.is_end_of_game():
                is_first_player_move = not is_first_player_move
        self.is_game_finished = True
        self.decide_winner(is_first_player_move)

    def decide_winner(self, is_first_player_move : bool):
        if self.__map.is_goal(True):
            self.is_first_player_win = True
            return

        if self.__map.is_goal(False):
            self.is_second_player_win = True
            return

        if is_first_player_move: # current side can't make a move
            self.is_second_player_win = True
        else:
            self.is_first_player_win = True

    def get_winner_states(self) -> list[list[int]]:
        if not self.is_game_finished:
            return []
        return self.__first_player_states if self.is_first_player_win else self.__second_player_states

    def get_loser_states(self) -> list[list[int]]:
        if not self.is_game_finished:
            return []
        return self.__first_player_states if self.is_second_player_win else self.__second_player_states
    
    def get_stats(self):
        stats = []
        stats.append(f'\t{type(self.__first_player)}; move time = {self.__fp_time}')
        f_stats = self.__first_player.get_stats()
        if f_stats:
            for s in f_stats:
                stats.append(f'\t\t{s}')
        
        stats.append(f'\t{type(self.__second_player)}; move time = {self.__sp_time}')
        s_stats = self.__second_player.get_stats()
        if s_stats:
            for s in s_stats:
                stats.append(f'\t\t{s}')
        return stats