from functools import reduce
import numpy as np

class StateData:

    __loses = 0
    __wins = 0

    def __init__(self):
        pass
    
    def add(self, state) -> None:
        self.__loses = self.__loses + state.__loses
        self.__wins = self.__wins + state.__wins

    def increase_loses(self) -> None:
        self.__loses = self.__loses + 1
    
    def increase_wins(self) -> None:
        self.__wins = self.__wins + 1

    def get_wins(self) -> int:
        return self.__wins
    
    def get_loses(self) -> int:
        return self.__loses

    def get_win_percentage(self) -> float:
        sum = self.__loses + self.__wins
        value = self.__loses * (-1) + self.__wins * 1
        return value/sum if sum != 0 else 0

    def state_to_string(state : list[list[int]]) -> str:
        flat_list = list(np.concatenate(state).flat)
        return reduce(lambda x, y: str(x) + str(y), flat_list)
    
    def string_to_state(state: str, map_width: int) -> list[list[int]]:
        flat_list = [int(c) for c in state]
        return StateData.one_dim_to_two_dim(flat_list, map_width)
    
    def one_dim_to_two_dim(flat_list: list[int], map_width: int) -> list[list[int]]:
        line_length = (map_width + 1) * 3
        return [flat_list[x:x+line_length] for x in range(0, len(flat_list), line_length)]

    def save_states(states : dict, file_name : str) -> None:
        print('Saving games')
        with open(file_name+"x", "w") as filex:
            with open(file_name+"y", "w") as filey:
                with open(file_name+"loses", "w") as file_loses:
                    with open(file_name+"wins", "w") as file_wins:
                        for key, value in states.items():
                            filex.write(f"{','.join([c for c in key])}\n")
                            filey.write(f"{value.get_win_percentage()}\n")
                            file_loses.write(f"{value.__loses}\n")
                            file_wins.write(f"{value.__wins}\n")
        print('Done')

    def load_states(file_name : str) -> dict:

        file_x_name = file_name + "x"
        file_loses_name = file_name + "loses"
        file_wins_name = file_name + "wins"

        result = {}

        try:
            with open(file_x_name) as file_x:
                with open(file_loses_name) as file_loses:
                    with open(file_wins_name) as file_wins:
                        lines_x = file_x.readlines()[0:-1]
                        lines_loses = file_loses.readlines()[0:-1]
                        lines_wins = file_wins.readlines()[0:-1]

                        vector_list = [x.strip().replace(',','') for x in lines_x]
                        loses_list = [int(lose.strip()) for lose in lines_loses]
                        wins_list = [int(win.strip()) for win in lines_wins]

                        result = {StateData.state_to_string(vector_list[i]) : StateData.createStateData(loses_list[i], wins_list[i]) for i in range(len(lines_x))}

                        print("Loading finished succesfully.")
        except Exception as e:
            print("Exception occurred during loading data.")
            print(e)
        finally:
            return result
        
    def createStateData(loses, wins):
        state = StateData()
        state.__loses = loses
        state.__wins = wins
        return state