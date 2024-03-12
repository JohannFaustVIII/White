import tensorflow as tf
import numpy as np
import sklearn.model_selection
from Game import Game
from NNPlayer import NNPlayer
from DefPlayer import DefPlayer
from StateData import StateData
from multiprocessing import Queue
from multiprocessing import Process
from Util import measure_time

class NNGame:
    
    __states_data = {}
    __process_queue = Queue()

    def train(self, file_name: str, games_per_process: int, discover : float, model_file: str, loops: int = 1, progressive : bool = False, discover_degradation  : float = 0.0, processes_to_spawn : int = 1, epochs : int = 100):
        counter = 0
        NNGame.__show_model_summary(model_file)

        while counter < loops:
            loop_file_name = NNGame.__get_progressive_file_name(progressive, file_name, counter)
            counter += 1
            print(f'Loop: {counter}, discover = {discover}')
            measure_time("generating games", lambda : self.generate_data(loop_file_name, games_per_process, discover, model_file, processes_to_spawn))
            measure_time("training session", lambda : self.__train(loop_file_name, model_file, epochs))
            discover = NNGame.__get_progressive_discovery(discover, discover_degradation)

    def __show_model_summary(model_file : str):
        
        def internal_print():
            model = tf.keras.models.load_model(model_file)
            print('-'*10 + 'Model summary' + '-'*10)
            model.summary()
            print('-'*30)

        proc = Process(target=internal_print)
        proc.start()
        proc.join()

    def __get_progressive_file_name(progressive : bool, file_name : str, counter : int) :
        if progressive:
            return file_name  + '_' + str(counter)
        else:
            return file_name

    def __get_progressive_discovery(actual_discovery: float, degradation: float) -> float:
        return max(0.01, actual_discovery - degradation)

    def __train(self, file_name: str, model_file: str, ep : int):

        def internal_training():
            model = self.__load_model(model_file)
            X_train, y_train, X_valid, y_valid = self.__load_data(file_name)
            model.fit(X_train, y_train, batch_size = 128, epochs = ep, verbose = 1, validation_data=(X_valid, y_valid))
            model.save(model_file)
        
        proc = Process(target=internal_training)
        proc.start()
        proc.join()

    def __load_data(self, file_name: str, min_limit : float = -1.0, max_limit: float = 1.0):
        x = np.loadtxt(file_name+'x', delimiter=",")
        y = np.loadtxt(file_name+'y', delimiter=",")
        
        x = np.array([StateData.one_dim_to_two_dim(s, 8) for s in x])

        x, y = NNGame.__filter_by_limits(x, y, min_limit, max_limit)

        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.2)

        x_train = tf.convert_to_tensor(x_train)
        x_test = tf.convert_to_tensor(x_test)
        y_train = tf.convert_to_tensor(y_train)
        y_test = tf.convert_to_tensor(y_test)

        return x_train, y_train, x_test, y_test
    
    def __filter_by_limits(x, y, min_limit : float, max_limit: float):
        if min_limit > -1.0 or max_limit < 1.0:
            x_f = []
            y_f = []

            for i in range(len(y)):
                if min_limit <= y[i] <= max_limit:
                    x_f.append(x[i])
                    y_f.append(y[i])
            
            x = np.array(x_f)
            y = np.array(y_f)

        return (x, y)

    def generate_data(self, file_name: str, iterations: int, discover: float, model_file: str, processes : int = 1):
        if iterations > 0:
            NNPlayer.clean_memory()
            self.__states_data = measure_time("loading states from file", lambda : StateData.load_states(file_name))
            proc_list = self.__spawn_playing_processes(iterations, discover, model_file, processes)
            self.__read_states_from_processes(proc_list)
            self.__join_processes(proc_list)
            StateData.save_states(self.__states_data, file_name)
        
    def __spawn_playing_processes(self, iterations: int, discover: float, model_file: str, processes : int):
        proc_list = []
        for i in range(processes):
            process = Process(target=self.__play_games, args=(iterations, discover, model_file, str(i)))
            proc_list.append(process)
            process.start()
        return proc_list
    
    def __read_states_from_processes(self, processes_list):
        print('Joining states')
        for _ in processes_list:
            states = self.__process_queue.get()
            for key, value in states.items():
                if key not in self.__states_data:
                    self.__states_data[key] = value
                else:
                    self.__states_data[key].add(value)
        print('Finished joining states')

    def __join_processes(self, processes_list):
        print('Joining processes')
        for p in processes_list:
            p.join()
        print('Finished joining processes')
        
    # TODO: think how to speed it up (or accelerate DefPlayer?)
    def __play_games(self, iterations: int, discover: float, model_file : str, name : str = ''):
        model = self.__load_model(model_file)
        states_data = {}
        nn_player = NNPlayer(model, discover)
        def_player = DefPlayer(depth = 2, use_memory = True)

        for i in range(iterations):
            first_player = nn_player if i % 2 == 0 else def_player
            second_player = nn_player if i % 2 == 1 else def_player


            self.__print_game_number(name, i)
            game = Game(first_player, second_player, True)
            game.play_game()
            self.__print_winner(name, i, game, first_player, second_player)
            self.__update_states(states_data, StateData.increase_wins, game.get_winner_states())
            self.__update_states(states_data, StateData.increase_loses, game.get_loser_states())
        
        print(f'{name} Finished playing games. Putting games into queue.')
        self.__process_queue.put(states_data)
        print(f'{name} Finished putting games into queue.')

    def __load_model(self, file: str):
        new_model = tf.keras.models.load_model(file)
        return new_model

    def __print_game_number(self, name: str, number: int):
        if number % 1 == 0:
            print(f'Process={name}: Game number:{number}')
    
    def __print_winner(self, name: str, number: int, game: Game, first_player, second_player):
        print(f"Process={name}: Game {number} won by {first_player.get_name() if game.is_first_player_win else second_player.get_name()}\n{game.get_stats()}")
    
    def __update_states(self, states_data, increase, states : list[list[int]]) -> None:
        for state in states:
            state_name = StateData.state_to_string(state)
            if state_name not in states_data:
                state_to_update = StateData()
                states_data[state_name] = state_to_update
            else:
                state_to_update = states_data[state_name]
            increase(self=state_to_update)