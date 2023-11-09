import heapq
import random

# Constants for game elements
RABBIT = 'r'
BIG_RABBIT = 'R'
CARROT = 'c'
RABBIT_HOLE = 'O'
PATHWAY_STONE = '-'

# Constants for movement keys
MOVE_LEFT = 'a'
MOVE_RIGHT = 'd'
MOVE_UP = 'w'
MOVE_DOWN = 's'
PICK_CARROT = 'p'
JUMP = 'j'
QUIT = 'q'

# Initialize the game board
def initialize_board(size, num_carrots, num_holes):
    board = [['-' for _ in range(size)] for _ in range(size)]

    # Place rabbit
    rabbit_row = random.randint(0, size - 1)
    rabbit_col = random.randint(0, size - 1)
    board[rabbit_row][rabbit_col] = RABBIT

    # Place rabbit holes
    for _ in range(num_holes):
        hole_row = random.randint(0, size - 1)
        hole_col = random.randint(0, size - 1)
        while board[hole_row][hole_col] != PATHWAY_STONE:
            hole_row = random.randint(0, size - 1)
            hole_col = random.randint(0, size - 1)
        board[hole_row][hole_col] = RABBIT_HOLE

    # Place carrots
    for _ in range(num_carrots):
        carrot_row = random.randint(0, size - 1)
        carrot_col = random.randint(0, size - 1)
        while board[carrot_row][carrot_col] != PATHWAY_STONE:
            carrot_row = random.randint(0, size - 1)
            carrot_col = random.randint(0, size - 1)
        board[carrot_row][carrot_col] = CARROT

    return board, (rabbit_row, rabbit_col)

# Print the game board
def print_board(board):
    for row in board:
        print(' '.join(row))

# Check if a move is valid
def is_valid_move(board, row, col):
    if 0 <= row < len(board) and 0 <= col < len(board[0]):
        return True
    return False

# Check if the rabbit can pick up a carrot
def can_pick_carrot(board, rabbit_row, rabbit_col):
    adjacent_positions = [
        (rabbit_row - 1, rabbit_col),
        (rabbit_row + 1, rabbit_col),
        (rabbit_row, rabbit_col - 1),
        (rabbit_row, rabbit_col + 1),
    ]

    for row, col in adjacent_positions:
        if is_valid_move(board, row, col) and board[row][col] == CARROT:
            return True
    return False

# Check if the rabbit can jump over a rabbit hole
def can_jump(board, rabbit_row, rabbit_col):
    adjacent_positions = [
        (rabbit_row - 1, rabbit_col),
        (rabbit_row + 1, rabbit_col),
        (rabbit_row, rabbit_col - 1),
        (rabbit_row, rabbit_col + 1),
    ]

    for row, col in adjacent_positions:
        if is_valid_move(board, row, col) and board[row][col] == RABBIT_HOLE:
            return True
    return False

# Check if the rabbit has won the game
def has_won(board, rabbit_row, rabbit_col):
    return board[rabbit_row][rabbit_col] == RABBIT_HOLE

# Implement the A* search algorithm
def astar_search(board, start, end):
    def heuristic(node):
        x, y = node
        end_x, end_y = end
        return abs(x - end_x) + abs(y - end_y)  # Manhattan distance heuristic

    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {node: float('inf') for row in board for node in row}
    g_score[start] = 0

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = current[0] + dx, current[1] + dy
            neighbor = (new_x, new_y)

            if not is_valid_move(board, new_x, new_y) or board[new_x][new_y] == CARROT:
                continue

            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor)
                heapq.heappush(open_list, (f_score, neighbor))

    return None

def play_game():
    size = int(input("Enter the size of the game board: "))
    num_carrots = int(input("Enter the number of carrots: "))
    num_holes = int(input("Enter the number of rabbit holes: "))

    board, rabbit_pos = initialize_board(size, num_carrots, num_holes)
    holding_carrot = False

    print("Welcome to Mr. Bunny's Carrot Gathering Game!")
    while True:
        print_board(board)
        move = input("Enter your move (a/d/w/s/p/j/q): ").lower()

        if move == MOVE_LEFT:
            new_pos = (rabbit_pos[0], rabbit_pos[1] - 1)
        elif move == MOVE_RIGHT:
            new_pos = (rabbit_pos[0], rabbit_pos[1] + 1)
        elif move == MOVE_UP:
            new_pos = (rabbit_pos[0] - 1, rabbit_pos[1])
        elif move == MOVE_DOWN:
            new_pos = (rabbit_pos[0] + 1, rabbit_pos[1])
        elif move == PICK_CARROT:
            if can_pick_carrot(board, rabbit_pos[0], rabbit_pos[1]) and not holding_carrot:
                holding_carrot = True
                board[rabbit_pos[0]][rabbit_pos[1]] = BIG_RABBIT
            else:
                print("Cannot pick up a carrot.")
        elif move == JUMP:
            if can_jump(board, rabbit_pos[0], rabbit_pos[1]):
                print("Jumping over a rabbit hole!")
                board[rabbit_pos[0]][rabbit_pos[1]] = PATHWAY_STONE
                rabbit_pos = new_pos
            else:
                print("Cannot jump over a hole.")
        elif move == QUIT:
            print("Game over. You quit.")
            break
        else:
            print("Invalid move. Use a/d/w/s/p/j/q to move.")

        if is_valid_move(board, new_pos[0], new_pos[1]):
            if board[new_pos[0]][new_pos[1]] == CARROT and not holding_carrot:
                print("You need to pick up the carrot (p) first.")
            elif board[new_pos[0]][new_pos[1]] == RABBIT_HOLE and holding_carrot:
                board[new_pos[0]][new_pos[1]] = PATHWAY_STONE
                holding_carrot = False
                num_holes -= 1  # Decrease the number of remaining holes
                print_board(board)
                if num_holes == 0:
                    print("Congratulations! Mr. Bunny safely returned to his rabbit hole with the carrot!")
                    break
            else:
                board[rabbit_pos[0]][rabbit_pos[1]] = PATHWAY_STONE
                board[new_pos[0]][new_pos[1]] = RABBIT if not holding_carrot else BIG_RABBIT
                rabbit_pos = new_pos
        else:
            print("Invalid move. Mr. Bunny can't go that way.")

if __name__ == "__main__":
    play_game()
