from game import Game

class Simulation:
    """
    Manages the simulation of multiple blackjack games.
    """
    def __init__(self, game: Game, verbose: bool = False) -> None:
        self.game = game
        self.verbose = verbose

    def run(self, rounds: int) -> None:
        """
        Run the simulation for a specified number of rounds.
        """
        if self.verbose:
            print(f"Starting simulation for {rounds} rounds")

        for _ in range(rounds):
            self.game.play_round()
            if self.verbose:
                print(f"Completed round {_ + 1}")

        print(f"Simulation completed")