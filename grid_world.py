import pygame
import numpy as np

# Constants
GRID_SIZE = 5
A_POS = (0, 1)
A_PRIME_POS = (4, 1)
B_POS = (0, 3)
B_PRIME_POS = (2, 3)
A_REWARD = 10
B_REWARD = 7
DISCOUNT_FACTOR = 0.98
NUM_ITERATIONS = 50

# Actions: up, down, left, right
ACTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Initialize values
values = np.zeros((GRID_SIZE, GRID_SIZE))

# Value iteration algorithm
for iter in range(NUM_ITERATIONS):
    new_values = np.zeros((GRID_SIZE, GRID_SIZE))
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            max_value = float('-inf')
            for _, action in enumerate(ACTIONS):
                reward = 0
                new_x, new_y = i + action[0], j + action[1]
                if (i, j) == A_POS:
                    new_x, new_y = A_PRIME_POS
                    reward = A_REWARD
                elif (i, j) == B_POS:
                    new_x, new_y = B_PRIME_POS
                    reward = B_REWARD
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    new_value = reward + DISCOUNT_FACTOR * values[new_x, new_y]
                    if new_value > max_value:
                        max_value = new_value
            new_values[i, j] = max_value
    values = new_values
    print(f'Iteration {iter+1}')
    print(values)

# Initialize Pygame
pygame.init()
CELL_SIZE = 100
GRID_WIDTH = GRID_SIZE * CELL_SIZE
GRID_HEIGHT = GRID_SIZE * CELL_SIZE
WINDOW_SIZE = (GRID_WIDTH, GRID_HEIGHT)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Optimal Policy Visualization')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

def draw_up_arrow(position):
    '''
    Draw centered up arrow.
    '''
    arrow_x, arrow_y = position[0], position[1] + CELL_SIZE // 4  # Start from 1/4 down the cell
    end_y = position[1] - CELL_SIZE // 4  # End at 1/4 up the cell
    arrow_pos = (arrow_x, arrow_y)
    pygame.draw.line(WINDOW, BLACK, arrow_pos, (arrow_x, end_y), 5)
    pygame.draw.polygon(WINDOW, BLACK, [(arrow_x - 5, end_y), (arrow_x + 5, end_y),
                                         (arrow_x, end_y - 10)])

def draw_down_arrow(position):
    '''
    Draw centered down arrow.
    '''
    arrow_x, arrow_y = position[0], position[1] - CELL_SIZE // 4  # Start from 3/4 down the cell
    end_y = position[1] + CELL_SIZE // 4  # End at 1/4 down the next cell
    arrow_pos = (arrow_x, arrow_y)
    pygame.draw.line(WINDOW, BLACK, arrow_pos, (arrow_x, end_y), 5)
    pygame.draw.polygon(WINDOW, BLACK, [(arrow_x - 5, end_y), (arrow_x + 5, end_y),
                                         (arrow_x, end_y + 10)])

def draw_left_arrow(position):
    '''
    Draw centered left arrow.
    '''
    arrow_x, arrow_y = position[0] + CELL_SIZE // 4, position[1]  # Start from 1/4 right of the cell
    end_x = position[0] - CELL_SIZE // 4  # End at 1/4 left of the cell
    arrow_pos = (arrow_x, arrow_y)
    pygame.draw.line(WINDOW, BLACK, arrow_pos, (end_x, arrow_y), 5)
    pygame.draw.polygon(WINDOW, BLACK, [(end_x, arrow_y - 5), (end_x, arrow_y + 5),
                                         (end_x - 10, arrow_y)])

# Function to draw right arrow
def draw_right_arrow(position):
    '''
    Draw centered right arrow.
    '''
    arrow_x, arrow_y = position[0] - CELL_SIZE // 4, position[1]  # Start from 3/4 right of the cell
    end_x = position[0] + CELL_SIZE // 4  # End at 1/4 right of the next cell
    arrow_pos = (arrow_x, arrow_y)
    pygame.draw.line(WINDOW, BLACK, arrow_pos, (end_x, arrow_y), 5)
    pygame.draw.polygon(WINDOW, BLACK, [(end_x, arrow_y - 5), (end_x, arrow_y + 5),
                                         (end_x + 10, arrow_y)])

def get_best_action(values, cell):
    '''
    Get best action based on iteration values.
    '''
    i, j = cell
    max_value = float('-inf')
    best_action = -1
    # Check up
    if i > 0 and values[i - 1, j] > max_value:
        max_value = values[i - 1, j]
        best_action = 0
    
    # Check down
    if i < GRID_SIZE - 1 and values[i + 1, j] > max_value:
        max_value = values[i + 1, j]
        best_action =  1
    
    # Check left
    if j > 0 and values[i, j - 1] > max_value:
        max_value = values[i, j - 1]
        best_action =  2
    
    # Check right
    if j < GRID_SIZE - 1 and values[i, j + 1] > max_value:
        max_value = values[i, j + 1]
        best_action = 3

    return best_action
    
def draw_arrows(values):
    '''
    Draw optimal policy with arrows using iteration values.
    '''
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            arrow_position = ((j * CELL_SIZE) + CELL_SIZE // 2, (i * CELL_SIZE) + CELL_SIZE // 2)  # Center of the cell
            if (i, j) == A_POS or (i, j) == B_POS:
                draw_up_arrow(arrow_position)
                draw_down_arrow(arrow_position)
                draw_left_arrow(arrow_position)
                draw_right_arrow(arrow_position)
            action = get_best_action(values, (i, j))
            if action == 0:  # Up
                draw_up_arrow(arrow_position)
            elif action == 1:  # Down
                draw_down_arrow(arrow_position)
            elif action == 2:  # Left
                draw_left_arrow(arrow_position)
            elif action == 3:  # Right
                draw_right_arrow(arrow_position)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear the screen
    WINDOW.fill(WHITE)
    
    # Draw the grid lines
    for i in range(GRID_SIZE):
        pygame.draw.line(WINDOW, GRAY, (0, i * CELL_SIZE), (GRID_WIDTH, i * CELL_SIZE))
        pygame.draw.line(WINDOW, GRAY, (i * CELL_SIZE, 0), (i * CELL_SIZE, GRID_HEIGHT))
    
    # Draw arrows indicating the optimal policy
    draw_arrows(values)
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
