from Game import Game
from NNPlayer import NNPlayer
from game.StateData import StateData

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

    def __update_states(self, increase : function, states : list[list[int]]) -> None:
        for state in states:
            state_name = StateData.state_to_string(state)
            state_to_update = self.__states_data[state_name]
            if not state_to_update:
                state_to_update = StateData(state)
                self.__states_data[state_name] = state_to_update
            increase(self=state_to_update)