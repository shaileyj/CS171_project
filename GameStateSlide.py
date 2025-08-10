from GameStateView import GameStateView
from MinimaxTreeSample import MinimaxTreeSample

def GameStateSlide():
    """Main application entry point"""
    # Create minimax tree
    minimax_tree = MinimaxTreeSample(depth=1)


    # Create game state view with minimax integration
    game_view = GameStateView(minimax_tree)
    game_view.run()

if __name__ == "__main__":
    GameStateSlide()