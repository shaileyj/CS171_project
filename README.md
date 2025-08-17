# Minimax Tree project
## Team Members: Shailey Joseph, My Nguyen
The minimax algorithm is a decision-making algorithm commonly used in game theory and artificial intelligence for the two-player zero-sum game. This project helps you understand how the algorithm works by:
- Playing an interactive tile capture game
- Visualizing the minimax decision tree in real-time
- Observing how game states change with each move
- Understanding the step-by-step evaluation process

## Part 1- Get Started
  ### Step 1: Play the game
  Start by exploring the tile capture game in **'TileCaptureGame.py'**
  - Familiarize yourself with the game mechanics
  - Understand the rules and objectives
  - Try different strategies and observe the outcomes

  The game rule:
  - Two players will take turns to pick a tile on the 5x5 board. They are allowed to choose the tile that is adjacent to their previous tiles.
  - Players will occupy the opponents’ tiles if the number of their tiles adjacent to an opponent’s tile is greater than 1 tile.
  - Whoever has a greater number of tiles when no more empty tiles are left is the winner.
  
  ### Step 2: Explore the Minimax Visualization
  Once you understand the game, examine the minimax tree visualization in **'minimax.py'** 
  - Click "->","D" or "space" to navigate
  - Watch the tree construction process step by step
  - Observe how each node represents a game state
  - Follow the algorithm's decision-making process
  - Notice how the tree evaluates different possible moves

## Part 2 - Interactive Portion
  ### Step 1: Explore Heuristics
  - Explore different heuristics for the game state in **'GameWithHeuristic.py'**
  - Try out three different heuristics and see the values of different moves in the game according to each heuristic
  - Think about these questions:
    - Which one(s) is more efficient when the board is empty?
    - Which one(s) is more efficient when the board is mostly full?
    - Which one(s) helps you win faster?

  ### Step 2: Fill out Minimax Tree
  - Fill out a minimax tree by running **'fill_minimax_tree.py'**
  - The user can input the correct value for a highlighted node in the minimax tree one at a time
  - If their input is incorrect, they can try again
  - The user will fill out the entire minimax tree, and gain a better understanding of the minimax algorithm

## What you will learn
- Tree Structure: ** How game states form a decision tree
- Step by Step Execution: Watch the algorithm work step by step
- Decision Path: Follow the optimal move selection

## File Structure
**'TileCaptureGame.py'** - Interactive tile capture game
**'minimax.py'** - Minimax tree visualization
**'main.py'** - Decision-makeing process 




