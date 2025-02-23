import numpy as np

maze_size = 64
maze = np.ones((maze_size, maze_size), dtype=int)

# Create an open path using a random walk from (1,1) to (62,62)
np.random.seed(42)  # For reproducibility
x, y = 1, 1
maze[x, y] = 0  # Start position

while (x, y) != (62, 62):
    direction = np.random.choice(["up", "down", "left", "right"])
    if direction == "up" and x > 1:
        x -= 1
    elif direction == "down" and x < maze_size - 2:
        x += 1
    elif direction == "left" and y > 1:
        y -= 1
    elif direction == "right" and y < maze_size - 2:
        y += 1
    maze[x, y] = 0  # Mark as part of the path

# Add some additional open spaces to make the maze solvable
for _ in range(500):
    rx, ry = np.random.randint(1, maze_size - 1, size=2)
    maze[rx, ry] = 0

# Print maze as a matrix
for row in maze:
    print(" ".join(map(str, row)))
