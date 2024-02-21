if __name__ == "__main__":
  import sys
  from ConsolePlayer import ConsolePlayer 
  from Game import Game

  side = sys.argv[1]
  if side[0] == 'd':
    from DefPlayer import DefPlayer

    side = side[1:]
    is_first_player = side == "1"

    first_player = ConsolePlayer(name = "First player") if is_first_player else DefPlayer(depth = 3, verbose = True)
    second_player = ConsolePlayer(name = "Second player") if not is_first_player else DefPlayer(depth = 3, verbose = True)
  
  else:
    is_first_player = side == "1"
    model_file = sys.argv[2]


    import tensorflow as tf
    from NNPlayer import NNPlayer

    model = tf.keras.models.load_model(model_file)
    model.summary()

    first_player = ConsolePlayer(name = "First player") if is_first_player else NNPlayer(model, 0.0, verbose = True, extra_verbose = True)
    second_player = ConsolePlayer(name = "Second player") if not is_first_player else NNPlayer(model, 0.0, verbose = True, extra_verbose = True)

  game = Game(first_player, second_player, False)
  game.play_game()

  print(f"First player win = {game.is_first_player_win}")
  print(f"Second player win = {game.is_second_player_win}")