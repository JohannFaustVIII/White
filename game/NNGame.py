from Game import Game
from NNPlayer import NNPlayer
from StateData import StateData

class NNGame:
    
    __states_data = {}

    def train(self, discover : float):
        # 1. load NN, a single one, from a file, or create it (optional parameter? no, check if file exists, if is, load, if not, only to save later)
        model = None # placeholder
        player = NNPlayer(model, discover) # to think: discover should be flexible and change between iterations, and... do we need two players?
        for i in range(0, 100): #TODO: change number of iterations
            game = Game(player, player, True)
            game.play_game()
            self.__update_states(StateData.increase_wins, game.get_winner_states())
            self.__update_states(StateData.increase_loses, game.get_loser_states())

        # 4. train NN with the statistics
        # 5. save NN after training
        # 6. save stats? and maybe load them before? at some point, stats should be dropped, as more experienced NN would be, to think
        # 7. go back to point 2? (it needs to be a loop too to stop at given point, or another thread, and send a signal to stop, gracefully, to think)

    def generate_data(self, file_name: str, iterations: int, discover: float):
        self.__states_data = {}
        self.__play_games(iterations, discover)
        self.__save_games(file_name, iterations)
        self.__states_data = {}
        
    def __play_games(self, iterations: int, discover: float):
        model = None # placeholder
        player = NNPlayer(model, discover)
        for i in range(iterations):
            print(f'Game {i}')
            game = Game(player, player, True)
            game.play_game()
            self.__update_states(StateData.increase_wins, game.get_winner_states())
            self.__update_states(StateData.increase_loses, game.get_loser_states())

    def __save_games(self, file_name: str, iterations: int):
        print('Saving games')
        with open(file_name+"x", "w") as filex:
            with open(file_name+"y", "w") as filey:
                for key, value in self.__states_data.items():
                    filex.write(f"{','.join([c for c in key])}\n")
                    filey.write(f"{value.get_win_percentage()}\n")
        print('Done')

    def __update_states(self, increase, states : list[list[int]]) -> None:
        for state in states:
            state_name = StateData.state_to_string(state)
            if state_name not in self.__states_data:
                state_to_update = StateData(state)
                self.__states_data[state_name] = state_to_update
            else:
                state_to_update = self.__states_data[state_name]
            increase(self=state_to_update)