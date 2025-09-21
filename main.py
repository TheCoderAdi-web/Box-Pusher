import json

# Printing the Game Grid
def print_grid(player_x, player_y, box_x, box_y, goal_x, goal_y, grid_size, level) -> None:
    print("\033c", end="") # Print Statement to Clear the Console / Terminal
    print("To progress to the next level, push the box (☐) onto the goal (G).")
    print(f"Player: P | Box: ☐ | Goal: G")
    print(f"Level {level}")
    level_grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
    level_grid[player_y][player_x] = "P"
    level_grid[goal_y][goal_x] = "G"
    level_grid[box_y][box_x] = "☐"
    for row in level_grid:
        print(" ".join(row))

# Handling Player Movement
def move_player(player_x, player_y, direction, grid_size) -> tuple:
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
def box_collision_player(box_x, box_y, player_x, player_y, last_input, grid_size) -> tuple:
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
def box_collision_goal(box_x, box_y, goal_x, goal_y) -> bool:
    if box_x == goal_x and box_y == goal_y:
        return True
    else:
        return False

# Updating the Grid Based on Player Input
def update_grid(player_x, player_y, box_x, box_y, goal_x, goal_y, grid_size, game_started) -> tuple:
    level_clear = False
    if game_started == True:
        move = input("Enter your move (w/a/s/d) or 'q' to quit: ").lower()
        last_input = move

        # Updating Player Position
        player_x, player_y = move_player(player_x, player_y, move, grid_size)

        # Updating Box Position if Player Pushes It
        box_x, box_y = box_collision_player(box_x, box_y, player_x, player_y, last_input, grid_size)

        # Update Level Clear State if the Box Collides with the Goal
        if box_collision_goal(box_x, box_y, goal_x, goal_y):
            level_clear = True

        # Quitting the Game if the Player Inputs 'q'
        if move == "q":
            print("Quitting the game...")
            print("Thanks for playing!")
            exit()

    return player_x, player_y, box_x, box_y, level_clear

# Running the Sokoban Game
if __name__ == "__main__":
    level = 1
    level_clear = False

    # Load Levels from the JSON file
    try:
        with open('levels.json', 'r') as f:
            levels = json.load(f)
            print("Levels loaded successfully.")
    except FileNotFoundError:
        print("Error: levels.json not found!")
        exit()

    game = True

    # Start the Game Based on User Input
    start = input("Start the Sokoban game? (y/n): ").lower()
    if start != 'y':
        game = False
    else:
        game = True

    # Main Game Loop
    while game:
        # Load Current Level Data
        level_data = levels[level - 1]

        # Printing the Level Grid and Updating it Based on Player Input
        print_grid(level_data['player_x'], level_data['player_y'], level_data['box_x'], level_data['box_y'], level_data['goal_x'], level_data['goal_y'], level_data['grid_size'], level)
        level_data['player_x'], level_data['player_y'], level_data['box_x'], level_data['box_y'], level_clear = update_grid(level_data['player_x'], level_data['player_y'], level_data['box_x'], level_data['box_y'], level_data['goal_x'], level_data['goal_y'], level_data['grid_size'], True)
        print_grid(level_data['player_x'], level_data['player_y'], level_data['box_x'], level_data['box_y'], level_data['goal_x'], level_data['goal_y'], level_data['grid_size'], level)

        # Advance to the Next Level if Current Level is Cleared
        if level_clear & (level < len(levels)):
            level += 1
        else:
            if level_clear & (level == len(levels)): # The Last Level has been Cleared if this IF condition is met
                print("Congratulations! You've completed all levels!")
                game = False