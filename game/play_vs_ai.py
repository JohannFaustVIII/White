if __name__ == "__main__":
  import sys
  import tensorflow as tf

  from ConsolePlayer import ConsolePlayer 
  from NNPlayer import NNPlayer
  from Game import Game

  is_first_player = sys.argv[1] == "1"
  model_file = sys.argv[2]


  model = tf.keras.models.load_model(model_file)
  model.summary()

  first_player = ConsolePlayer(name = "First player") if is_first_player else NNPlayer(model, 0.0, verbose = True)
  second_player = ConsolePlayer(name = "Second player") if not is_first_player else NNPlayer(model, 0.0, verbose = True)

  game = Game(first_player, second_player, False)
  game.play_game()

  print(f"First player win = {game.is_first_player_win}")
  print(f"Second player win = {game.is_second_player_win}")