from NNGame import NNGame
import datetime

game = NNGame()
start = datetime.datetime.now().replace(microsecond=0)
game.train(
    file_name='generated_states/monday/c3_2_games.st', 
    games_per_process = 25, 
    discover = 0.5,
    discover_degradation=0.08,  
    model_file='saved_model/conva_3', 
    loops = 5, 
    progressive = True, 
    processes_to_spawn=4, 
    epochs = 20)
end = datetime.datetime.now().replace(microsecond=0)

print(f"Training finished in {end-start}")