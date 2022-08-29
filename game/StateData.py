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

    def get_win_percentage(self) -> float:
        sum = self.__loses + self.__wins
        return self.__wins/sum if sum != 0 else 0

    def get_state(self) -> list[int]:
        return self.__state

    def state_to_string(state : list[int]) -> str:
        return reduce(lambda x, y: str(x) + str(y), state)