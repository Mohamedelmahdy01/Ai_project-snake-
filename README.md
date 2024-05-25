# Snake Game with AI

This is a Snake game implemented in Python using the Pygame library. It includes an AI agent that controls the movement of the snake using the A* algorithm to find the shortest path to the food.

## Features

- Classic Snake gameplay where the player controls the snake to eat food and grow longer.
- AI-controlled snake that autonomously navigates the game board to reach the food.
- Random spawning of food after the snake consumes it.
- Game over when the snake collides with itself or the boundaries of the game board.

## Files

- **snake_game.py**: This file contains the main implementation of the Snake game, including the game loop, user input handling, drawing functions, and game over logic.
- **snake_ai.py**: This file implements the AI agent for controlling the snake's movement using the A* algorithm. It calculates the shortest path to the food and guides the snake accordingly.
  
## How to Play

- Use the arrow keys (UP, DOWN, LEFT, RIGHT) to control the movement of the snake.
- The snake will automatically move in the direction chosen by the AI when playing with AI control.
- Avoid colliding with the walls or the snake's own body.
- Eat food to grow longer and increase your score.

## Installation

1. Install Python if you haven't already. You can download it from [python.org](https://www.python.org/downloads/).
2. Install Pygame by running `pip install pygame` in your terminal or command prompt.
3. Clone this repository to your local machine using `[git clone https://github.com/your-username/snake-game.git](https://github.com/Mohamedelmahdy01/Ai_project-snake-.git)`.

## Usage

1. Navigate to the directory where the files are located.
2. Run the Snake game by executing `python snake_game.py` in your terminal or command prompt.
3. Enjoy playing the game!

## Credits

- The Pygame library: [pygame.org](https://www.pygame.org/)
- The A* algorithm implementation: [Wikipedia - A* search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
- Snake game implementation reference: [Invent with Python - Making Games with Python & Pygame](https://inventwithpython.com/pygame/chapter6.html)
- Snake game implementation reference (code): [Invent with Python - wormy.py](https://inventwithpython.com/wormy.py)

---



