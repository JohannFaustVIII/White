import tensorflow as tf
import numpy as np
import sklearn.model_selection
from Game import Game
from NNPlayer import NNPlayer
from StateData import StateData
from multiprocessing import Queue
from multiprocessing import Process
from Util import measure_time

class NNGame:
    
    __states_data = {}
    __process_queue = Queue()

    def train(self, file_name: str, iterations: int, discover : float, model_file: str, loops: int = 1, progressive : bool = False, discover_degradation  : float = 0.0, processes_to_spawn : int = 1):
        counter = 0
        while counter < loops:
            loop_file_name = NNGame.__get_progressive_file_name(progressive, file_name, counter)
            counter += 1
            print(f'Loop: {counter}, discover = {discover}')
            measure_time("generating games", lambda : self.generate_data(loop_file_name, iterations, discover, model_file, processes_to_spawn))
            measure_time("training session", lambda : self.__train(loop_file_name, model_file))
            discover = NNGame.__get_progressive_discovery(discover, discover_degradation)

    def __get_progressive_file_name(progressive : bool, file_name : str, counter : int) :
        if progressive:
            return file_name  + '_' + str(counter)
        else:
            return file_name

    def __get_progressive_discovery(actual_discovery: float, degradation: float) -> float:
        return max(0.01, actual_discovery - degradation)

    def __train(self, file_name: str, model_file: str):

        def internal_training():
            model = self.__load_model(model_file)
            X_train, y_train, X_valid, y_valid = self.__load_data(file_name)
            model.fit(X_train, y_train, batch_size = 128, epochs = 20, verbose = 1, validation_data=(X_valid, y_valid))
            model.save(model_file)
        
        proc = Process(target=internal_training)
        proc.start()
        proc.join()

    def __load_data(self, file_name: str, min_limit : float = -1.0, max_limit: float = 1.0):
        x = np.loadtxt(file_name+'x', delimiter=",")
        y = np.loadtxt(file_name+'y', delimiter=",")
        

        if min_limit > -1.0 or max_limit < 1.0:
            x_f = []
            y_f = []

            for i in range(len(y)):
                if min_limit <= y[i] <= max_limit:
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

    def generate_data(self, file_name: str, iterations: int, discover: float, model_file: str, processes : int = 1):
        if iterations > 0:
            NNPlayer.clean_memory()
            self.__states_data = measure_time("loading states from file", lambda : StateData.load_states(file_name))
            proc_list = []
            for i in range(processes):
                process = Process(target=self.__play_games, args=(iterations, discover, model_file, str(i)))
                proc_list.append(process)
                process.start()
            print('Joining states')
            for i in range(processes):
                states = self.__process_queue.get()
                for key, value in states.items():
                    if key not in self.__states_data:
                        self.__states_data[key] = value
                    else:
                        self.__states_data[key].add(value)
            print('Finished joining states')
            print('Joining processes')
            for p in proc_list:
                p.join()
            print('Finished joining processes')
            StateData.save_states(self.__states_data, file_name)
        
    def __play_games(self, iterations: int, discover: float, model_file : str, name : str = ''):
        model = self.__load_model(model_file)
        states_data = {}
        player = NNPlayer(model, discover)

        for i in range(iterations):
            if i % 100 == 0:
                print(f'{name} Game {i}')
            game = Game(player, player, True)
            game.play_game()
            self.__update_states(states_data, StateData.increase_wins, game.get_winner_states())
            self.__update_states(states_data, StateData.increase_loses, game.get_loser_states())
        
        print(f'{name} Finished playing games. Putting games into queue.')
        self.__process_queue.put(states_data)
        print(f'{name} Finished putting games into queue.')

    def __load_model(self, file: str):
        new_model = tf.keras.models.load_model(file)
        return new_model
    
    def __update_states(self, states_data, increase, states : list[list[int]]) -> None:
        for state in states:
            state_name = StateData.state_to_string(state)
            if state_name not in states_data:
                state_to_update = StateData(state)
                states_data[state_name] = state_to_update
            else:
                state_to_update = states_data[state_name]
            increase(self=state_to_update)