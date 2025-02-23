import pygame
import numpy as np
import random
# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 100
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
REWARDS = [
    [-1,-1,-100,-100,-100,-100],
    [-100,-1,-1,-1,-100,-100],
    [-100,-1,-100,-1,-100,-100],
    [-100,-1,-1,-1,-1,-100],
    [-1,-1,-1,-1,-1,-1],
    [-1,-100,-1,-100,-100,100]
]
start_points = [[0,0],[0,1],[1,1]]
goal_points = [[5,5],[5,0],[5,2]]
# Maze layout (1 = wall, 0 = path)
MAZE = [
    [0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0]
]

# Player starting position
player_x, player_y = 0, 0
goal_x, goal_y = 0, 5  # Goal position

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Q-learning parameters
alpha = 0.9 # The learning rate (How much new info overides old info)
gamma = 0.9 # Discount factor (Long term rewards are as important as immediate rewards)
epsilon = 1   # Randomness
epsilon_decay = 0.001 # epsilon will decrease by this factor on every episode.
min_epsilon = 0.01 # At least 1% chance of taking an random action
max_steps = 10 # max number of steps the Agent can take per episode
visited_states = {}
q_table = np.zeros((ROWS*COLS,4))

def render_state(player_x,player_y):
    screen.fill(WHITE)
    # Draw maze
    for row in range(ROWS):
        for col in range(COLS):
            if MAZE[row][col] == 1:
                pygame.draw.rect(screen, BLACK, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw player
    pygame.draw.rect(screen, BLUE, (player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw goal
    #pygame.draw.rect(screen, GREEN, (goal_x * TILE_SIZE, goal_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    pygame.draw.circle(screen,GREEN,center=(goal_x*TILE_SIZE + TILE_SIZE//2 , goal_y*TILE_SIZE + TILE_SIZE//2 ),radius=TILE_SIZE//2)
    # Event handling
    return pygame

def display_game(pygame,time=10):
    pygame.display.flip()
    pygame.time.delay(time)

def make_move(state):
    if random.uniform(0,1) < epsilon:
        return random.randint(0,3)
    else:
        return np.argmax(q_table[state,:])
visited_states = {}
def calculate_reward(x,y):
    if (not (x >=0 and y >=0 and x<ROWS and y < COLS)):
        return -100
    return REWARDS[x][y]

def calculate_state(old_state,x,y):
    next_state = (x)*COLS + y
    reward = calculate_reward(x,y)

    if (not (x >=0 and y >=0 and x<ROWS and y < COLS and MAZE[x][y] == 0 )):
        return old_state , reward
    visited_states[next_state] = visited_states.get(next_state, 0) + 1
    revisit_penalty = -0.15 * visited_states[next_state] 
    return next_state , reward +revisit_penalty

def get_start_pos():
    y , x = random.choice(start_points)
    return x , y

def get_goal_pos():
    y , x = random.choice(goal_points)
    return x , y

episodes = 50 
steps = 100
i = 0
# Game loop
# left -> 0
# right -> 1
# down -> 2
# up -> 3
while i < episodes:
    rand = 0
    player_y , player_x = start_points[rand]
    pygame = render_state(player_x,player_y)
    reward = REWARDS[player_y][player_x]
    state = (player_y)*COLS + player_x
    goal_y , goal_x =  goal_points[rand]
    print(f"Running Episode {i+1}/{episodes}\r",end="",flush=True)
    for step in range(steps):
        new_x, new_y = player_x, player_y
        action = make_move(state)
        
        if action == 0:
            new_x -= 1
        elif action== 1:
            new_x += 1
        elif action == 3:
            new_y -= 1
        elif action == 2:
            new_y += 1
        
        
        # Check for wall collision
        next_state, reward = calculate_state(state,new_y,new_x)
        #print(f"state= {state}, next_state = {next_state}, reward = {reward}")
        if next_state != state:
            player_x , player_y = new_x,new_y
        old_value = q_table[state,action]
        next_max = np.max(q_table[next_state,:])
        # Q-learning Algorithm
        q_table[state,action] = (1-alpha)*old_value + alpha*(reward+gamma*next_max)
        state = next_state
        pygame = render_state(player_x,player_y)
        display_game(pygame,50)
        # Check if the player reaches the goal
        if player_x == goal_x and player_y == goal_y:
            print("Congratulations! You reached the goal!")
            break
            # running = False
    epsilon = max(min_epsilon,epsilon*epsilon_decay)
    i += 1
print(q_table)
j = 0
# Ai playing the game
while(j<1):
    rand = 0
    player_y , player_x = start_points[rand]
    reward = REWARDS[player_y][player_x]
    state = (player_y)*COLS + player_x
    goal_y , goal_x =  goal_points[rand]
    print(f"AI episode = {j}")
    for step in range(steps):
        new_x , new_y = player_x , player_y
        action = np.argmax(q_table[state,:])
        print(f"Action = {action}")
        if action == 0:
            new_x -= 1
        elif action== 1:
            new_x += 1
        elif action == 3:
            new_y -= 1
        elif action == 2:
            new_y += 1
        
        # Check for wall collision
        next_state ,  reward = calculate_state(state,new_y,new_x)
        print(f"state= {state}, next_state = {next_state}, reward = {reward}")
        if next_state != state:
            player_x , player_y = new_x,new_y
        pygame = render_state(player_x,player_y)
        display_game(pygame,100)
        state = next_state

        if player_x == goal_x and player_y == goal_y:
            print("Congratulations! You reached the goal!")
            break

    j +=1

pygame.quit()
