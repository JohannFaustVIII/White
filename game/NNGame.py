class NNGame:
    pass

    # what is the idea?
    # 1. load NN, a single one, from a file, or create it (optional parameter? no, check if file exists, if is, load, if not, only to save later)
    # 2. create two players using NN
    # 3. loop given number of times
    # 3.1. play the game (create an object and play, turned on registering of moves)
    # 3.2. get losing and wining states (based on the game result)
    # 3.3. update statistics, compute the percent of wins in given position (between 0 and 1)
    # 4. train NN with the statistics
    # 5. save NN after training
    # 6. save stats? and maybe load them before? at some point, stats should be dropped, as more experienced NN would be, to think
    # 7. go back to point 2? (it needs to be a loop too to stop at given point, or another thread, and send a signal to stop, gracefully, to think)