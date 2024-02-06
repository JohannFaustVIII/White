from NNGame import NNGame
import datetime

game = NNGame()
start = datetime.datetime.now().replace(microsecond=0)
game.train(
    file_name='generated_states/monday/dzeta_1_games.st', 
    iterations = 25, 
    discover = 0.25, 
    model_file='saved_model/conva_2', 
    loops = 20, 
    progressive = False, 
    discover_degradation=0.01, 
    processes_to_spawn=4, 
    epochs = 10)
end = datetime.datetime.now().replace(microsecond=0)

print(f"Training finished in {end-start}")