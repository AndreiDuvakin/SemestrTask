[🇷🇺 Русский](README_RU.md)

# Two foxes and twenty chickens

## About the project

This is a graphical board game implemented in Python using the PyQt6 framework.
The project was completed as part of the academic course MDK.02.01 Software Development Technology (specialization 09.02.07 Information Systems and Programming).

## Report

The report is in the file [Report.pdf](Report.pdf)

## Purpose of creation

- Reinforcing object-oriented programming skills.
- Mastering the graphical interface.
- Implementing game logic with AI opponents.
- Practicing working with events, buttons, icons, and interface redrawing.
- Developing team development and code documentation skills.

## Rules of the game

### Playing field

- The playing field is shaped like a cross, measuring 7x7 squares.
- At the start of the game, the board contains:
  - 2 foxes in the upper center
  - 20 chickens, distributed throughout the board

### Moves
#### Chickens (player)
- Move one step:
  - up
  - left
  - right
- Cannot move down or diagonally.

#### Foxes (computer)
- Move one step in any direction (up, down, left, right).
- Can eat chickens:
If there's an empty space one space behind a chicken (horizontally or vertically), the fox jumps over the chicken and eats it.
- The fox must eat if given the choice.

### Victory / Defeat
- The player (chickens) wins if the chickens occupy the 9 squares that form the top square of the board.
- The foxes win if they eat 12 chickens (the remaining chickens are not enough to win).
- 
## Interface

- Fixed-size graphic window.
- Cell buttons display icons:
  - Chicken
  - Fox
  - Empty cell
- When a chicken is selected, available moves are highlighted in green.
- After each player's turn, the foxes automatically take turns.

## Fox logic

The fox tries sequentially:
1. To eat a chicken in all 4 jumping directions.
2. If eating is impossible, it randomly moves to an adjacent free cell.

## License
MIT. See file [LICENSE](LICENSE).
