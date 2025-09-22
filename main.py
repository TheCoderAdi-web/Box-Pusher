"""
FOR CLARITY:
In the JSON file, all dictionaries contain level data with the following keys:
"player_x", "player_y", "box_x", "box_y", "goal_x", "goal_y", and "grid_size".
All of the dictionaries are stored in a list, with each dictionary representing a different level.
"""

import json
from dataclasses import dataclass

"""
Data Class for Level Representation
"""
@dataclass
class Level:
    player_x: int
    player_y: int
    box_x: int
    box_y: int
    goal_x: int
    goal_y: int
    grid_size: int

def print_grid(level: Level, level_num: int) -> None:
    """
    Prints the current state of the game grid for the given level.
    """
    print("\033c", end="") # Clear the Console
    print("To progress to the next level, push the box (☐) onto the goal (G).")
    print(f"Player: P | Box: ☐ | Goal: G")
    print(f"Level {level_num}")
    grid = [["." for _ in range(level.grid_size)] for _ in range(level.grid_size)]
    grid[level.player_y][level.player_x] = "P"
    grid[level.goal_y][level.goal_x] = "G"
    grid[level.box_y][level.box_x] = "☐"
    for row in grid:
        print(" ".join(row))

# Handling Player Movement
def move_player(player_x: int, player_y: int, direction: str, grid_size: int) -> tuple:
    if direction == "w" and player_y > 0:
        player_y -= 1
    elif direction == "s" and player_y < grid_size - 1:
        player_y += 1
    elif direction == "a" and player_x > 0:
        player_x -= 1
    elif direction == "d" and player_x < grid_size - 1:
        player_x += 1
    return player_x, player_y

# Pushing the Box if the Player Moves into its Position
def box_collision_player(box_x: int, box_y: int, player_x: int, player_y: int, last_input: str, grid_size: int) -> tuple:
    if player_x == box_x and player_y == box_y:
        if last_input == "w" and box_y > 0:
            box_y -= 1
        elif last_input == "s" and box_y < grid_size - 1:
            box_y += 1
        elif last_input == "a" and box_x > 0:
            box_x -= 1
        elif last_input == "d" and box_x < grid_size - 1:
            box_x += 1

    return box_x, box_y

# Handling Collision between the Box and the Goal
def box_collision_goal(box_x: int, box_y: int, goal_x: int, goal_y: int) -> bool:
    return box_x == goal_x and box_y == goal_y

# Quitting the Game
def quit(move: str) -> None:
    """
    Quits the game directly by raising a SystemExit Exception if the player inputs 'q'.
    """
    if move == "q":
        print("Quitting the game...")
        print("Thanks for playing!")
        raise SystemExit()

# Updating the Grid Based on Player Input
def update_grid(level: Level, game_started: bool) -> tuple[Level, bool]:
    """
    Processes player input and updates the level state. Returns the updated Level and whether the level is cleared.
    """
    level_clear = False
    if game_started:
        move = input("Enter your move (w/a/s/d) or 'q' to quit: ").lower()
        last_input = move
        # Update player position
        new_player_x, new_player_y = move_player(level.player_x, level.player_y, move, level.grid_size)
        # Update box position if needed
        new_box_x, new_box_y = box_collision_player(level.box_x, level.box_y, new_player_x, new_player_y, last_input, level.grid_size)
        # Check for goal
        if box_collision_goal(new_box_x, new_box_y, level.goal_x, level.goal_y):
            level_clear = True
        # Check for quit
        quit(move)
        # Return updated Level instance
        updated_level = Level(
            player_x=new_player_x,
            player_y=new_player_y,
            box_x=new_box_x,
            box_y=new_box_y,
            goal_x=level.goal_x,
            goal_y=level.goal_y,
            grid_size=level.grid_size
        )
        return updated_level, level_clear
    return level, level_clear

def load_levels(file_name: str) -> list[Level]:
    """
    Loads levels from a JSON file and returns them as a list of Level instances.
    """
    try:
        with open(file_name, 'r') as f:
            levels_data = json.load(f)
            print("Levels loaded successfully.")
            return [Level(**level_dict) for level_dict in levels_data]
    except FileNotFoundError:
        print("Error: levels.json not found!")
        raise SystemExit()

# Update and Print the Grid
def print_and_update_grid(level: Level, level_num: int) -> tuple[Level, bool]:
    """
    Prints the current grid, processes player input, updates positions, and prints the updated grid.
    Returns the updated Level and whether the level is cleared.
    """
    print_grid(level, level_num)
    updated_level, level_clear = update_grid(level, True)
    print_grid(updated_level, level_num)
    return updated_level, level_clear

def main() -> None:
    level_num = 1
    levels = load_levels('levels.json')
    game = True
    start = input("Start the Sokoban game? (y/n): ").lower()
    if start != 'y':
        game = False
    # Main Game Loop
    while game:
        # Get Level instance for current level
        current_level = levels[level_num - 1]
        level_clear = False
        # Loop for the current level until cleared
        while not level_clear:
            current_level, level_clear = print_and_update_grid(current_level, level_num)
        # Advance to the Next Level if Current Level is Cleared
        if level_num < len(levels):
            level_num += 1
        else:
            print("Congratulations! You've completed all levels!")
            game = False

# Running the Sokoban Game
if __name__ == "__main__":
    main()