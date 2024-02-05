from NNGame import NNGame
import datetime

game = NNGame()
start = datetime.datetime.now().replace(microsecond=0)
game.train('generated_states/monday/epsilon_1_games.st', 100, 0.5, 'saved_model/conva_2', 1, False, 0.1, 4, epochs = 100)
end = datetime.datetime.now().replace(microsecond=0)

print(f"Training finished in {end-start}")