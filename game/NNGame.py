import tensorflow as tf
import numpy as np
import sklearn.model_selection
from Game import Game
from NNPlayer import NNPlayer
from StateData import StateData

class NNGame:
    
    __states_data = {}

    def train(self, file_name: str, iterations: int, discover : float, model_file: str, loops: int = 1, progressive : bool = False):
        counter = 0
        model = self.__load_model(model_file)
        while counter < loops:
            loop_file_name = NNGame.__get_progressive_file_name(progressive, file_name, counter)
            counter += 1
            print(f'Loop: {counter}')
            self.generate_data(loop_file_name, iterations, discover, model)
            self.__train(model, loop_file_name, model_file)

    def __load_model(self, file: str):
        new_model = tf.keras.models.load_model(file)
        new_model.summary()
        return new_model

    def __get_progressive_file_name(progressive : bool, file_name : str, counter : int) :
        if progressive:
            return file_name  + '_' + str(counter)
        else:
            return file_name
        
    def __train(self, model, file_name: str, model_file: str):
        X_train, y_train, X_valid, y_valid = self.__load_data(file_name)
        model.fit(X_train, y_train, batch_size = 128, epochs = 20, verbose = 1, validation_data=(X_valid, y_valid))
        model.save(model_file)

    def __load_data(self, file_name: str, min_limit : float = 0.0, max_limit: float = 1.0):
        x = np.loadtxt(file_name+'x', delimiter=",")
        y = np.loadtxt(file_name+'y', delimiter=",")
        

        if min_limit > 0.0 or max_limit < 1.0:
            x_f = []
            y_f = []

            for i in range(len(y)):
                if y[i] > 0.3:
                    x_f.append(x[i])
                    y_f.append(y[i])
            
            x = np.array(x_f)
            y = np.array(y_f)

        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.2)

        x_train = tf.convert_to_tensor(x_train)
        x_test = tf.convert_to_tensor(x_test)
        y_train = tf.convert_to_tensor(y_train)
        y_test = tf.convert_to_tensor(y_test)

        return x_train, y_train, x_test, y_test

    def generate_data(self, file_name: str, iterations: int, discover: float, model = None):
        if iterations > 0:
            self.__states_data = StateData.load_states(file_name)
            self.__play_games(iterations, discover, model)
            StateData.save_states(self.__states_data, file_name)
        
    def __play_games(self, iterations: int, discover: float, model = None):
        player = NNPlayer(model, discover)
        for i in range(iterations):
            print(f'Game {i}')
            game = Game(player, player, True)
            game.play_game()
            self.__update_states(StateData.increase_wins, game.get_winner_states())
            self.__update_states(StateData.increase_loses, game.get_loser_states())

    def __update_states(self, increase, states : list[list[int]]) -> None:
        for state in states:
            state_name = StateData.state_to_string(state)
            if state_name not in self.__states_data:
                state_to_update = StateData(state)
                self.__states_data[state_name] = state_to_update
            else:
                state_to_update = self.__states_data[state_name]
            increase(self=state_to_update)