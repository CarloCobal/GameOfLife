#This finds the best board without any animation and saves the boards to a txt file. It also saves the best score to a txt file. 

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# Define the size of the matrix
n = 10

# Define the size of the larger pattern
size = 10

# Generate a uniform pattern for the larger pattern
initial_pattern = np.random.choice([0, 1], size=(n,n))
bigger_board = np.block([[initial_pattern for _ in range(size)] for _ in range(size)])
saved_board = str(bigger_board)

# Initialize the best score
try:
    with open("savedBestScore.txt", "r+") as file:
        contents = file.read().strip()
        if contents:  # If the file is not empty
            best_score = float(contents)
        else:  # If the file is empty
            best_score = float('-inf')
except FileNotFoundError:
    with open("savedBestScore.txt", "w") as file:
        best_score = float('-inf')

# save the initial board to txt
with open("saved_board.txt", 'a') as s:
    s.write(saved_board) 

    p= 0.9999

    for i in range(bigger_board.shape[0]):
        for j in range(bigger_board.shape[1]):
            if bigger_board[i, j] == 0:
                bigger_board[i, j] = np.random.choice([0, 1], p=[p, 1-p])

    # Define the number of iterations
    num_iterations = 100

    # Define the current iteration
    current_iteration = 0

    def calculate_similarity(board, x, y, initial_grid_size):
        # Define the range of the grid to consider
        grid_range = range(-initial_grid_size, initial_grid_size + 1)
        
        # Initialize counters for similar and total cells
        similar_cells = 0
        total_cells = 0
        
        # Iterate over the cells in the grid
        for i in grid_range:
            for j in grid_range:
                # Skip the cell itself
                if i == 0 and j == 0:
                    continue
                
                # Calculate the coordinates of the neighbor cell
                neighbor_x = (x + i) % board.shape[0]
                neighbor_y = (y + j) % board.shape[1]
                
                # Increment the total cells counter
                total_cells += 1
                
                # If the neighbor cell is similar to the current cell, increment the similar cells counter
                if board[x, y] == board[neighbor_x, neighbor_y]:
                    similar_cells += 1
        
        # Calculate and return the similarity as the proportion of similar cells
        return similar_cells / total_cells

    def update(data):
        global bigger_board
        global current_iteration
        global best_score
        new_board = bigger_board.copy()
        total_similarity = 0
        for i in range(bigger_board.shape[0]):
            for j in range(bigger_board.shape[1]):
                # Get the coordinates of the eight neighbors
                neighbors = [(i-1, j-1), (i-1, j), (i-1, j+1),
                            (i, j-1),             (i, j+1),
                            (i+1, j-1), (i+1, j), (i+1, j+1)]
                # Count the number of live neighbors
                total = sum(bigger_board[x % bigger_board.shape[0], y % bigger_board.shape[1]] for x, y in neighbors)
                if bigger_board[i, j]  == 1:
                    if total < 2 or total > 3:
                        new_board[i, j] = 0
                else:
                    if total == 3:
                        new_board[i, j] = 1
                total_similarity += calculate_similarity(bigger_board, i, j, n)
        bigger_board = new_board
        current_iteration += 1
        if current_iteration >= num_iterations:
            total_sim = total_similarity / (bigger_board.shape[0] * bigger_board.shape[1])

            print("Final similarity score: ", total_sim)
            s.write(str(total_sim))
            # Update best scored board
            if total_sim > best_score:
                best_score = total_sim
                with open("savedBestScore.txt", 'w') as w:  # This will overwrite the old score
                    w.write(str(best_score))
                # Update best board if best scored
                with open("saved_bestBoard.txt", 'w') as b:  # This will overwrite the old board
                    b.write(str(saved_board))
            return
        return update(new_board)

    for i in range(100):
        s.write(str(i))
        s.write('\n') 
        update(bigger_board)
