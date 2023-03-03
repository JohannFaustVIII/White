from functools import reduce


class StateData:

    __loses = 0
    __wins = 0

    def __init__(self, state : list[int]):
        self.__state = state
        pass
    
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
        return self.__wins/sum if sum != 0 else 0

    def get_state(self) -> list[int]:
        return self.__state

    def state_to_string(state : list[int]) -> str:
        return reduce(lambda x, y: str(x) + str(y), state)
    
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
        print("Loading data from a file.")
        file_x_name = file_name + "x"
        file_loses_name = file_name + "loses"
        file_wins_name = file_name + "wins"

        result = {}

        try:
            with open(file_x_name) as file_x:
                with open(file_loses_name) as file_loses:
                    with open(file_wins_name) as file_wins:
                        lines_x = file_x.readlines()
                        lines_loses = file_loses.readlines()
                        lines_wins = file_wins.readlines()

                        for i in range(len(lines_x) - 1):
                            vector = [int(c) for c in lines_x[i].strip().split(",")]
                            loses = int(lines_loses[i].strip())
                            wins = int(lines_wins[i].strip())

                            state = StateData(vector)
                            state.__loses = loses
                            state.__wins = wins

                            key = StateData.state_to_string(vector)

                            result[key] = state
                        
                        print("Loading finished succesfully.")
        except Exception as e:
            print("Exception occurred during loading data.")
            print(e)
        finally:
            return result