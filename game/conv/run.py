from NNGame import NNGame
import datetime

game = NNGame()
start = datetime.datetime.now().replace(microsecond=0)
game.train(
    file_name='generated_states/monday/dzeta_1_games.st', 
    games_per_process = 200, 
    discover = 0.05,
    discover_degradation=0,  
    model_file='saved_model/conva_2', 
    loops = 1, 
    progressive = True, 
    processes_to_spawn=4, 
    epochs = 10)
end = datetime.datetime.now().replace(microsecond=0)

print(f"Training finished in {end-start}")