# Color-Maze puzzle is a single-agent grid-game played on a rectangular board that includes
# a maze. Initially, the agent is located on a single maze cell. The agent can move in four cardinal
# directions: up, down, right or left. Once a direction is chosen, the agent moves in that direction
# until it reaches a wall at once, and colors all the cells it travels over. Once a cell is colored, its
# color does not change. The goal is to color all the cells of the maze by moving the agent over
# them, while minimizing the total distance traveled by the agent.
import time

import heapq


#board is a two dimensional list of chars
board = []

size =12
#function to print the board
def printBoard(board):
    for i in range(size):
        for j in range(size):
            print(board[i][j], end = " ")
        print()

#function to check if the board is solved (checks if there are any 0s left on the board if not the board is solved)
def isSolved(board):
    for i in range(size):
        for j in range(size):
            if board[i][j] == "0":
                return False
    return True

#function to check if the move is valid (checks if the move is within the board and if the cell is not a wall)
def isValid(board, x, y):
    if x >= 0 and x < size and y >= 0 and y < size and board[x][y] != "X":
        return True
    return False

#function to get all the valid moves from a cell (returns a list of chars representing the valid moves u, d, l, r)
def getValidMoves(board, x, y):
    validMoves = []
    if isValid(board, x - 1, y):
        validMoves.append("u")
    if isValid(board, x + 1, y):
        validMoves.append("d")
    if isValid(board, x, y - 1):
        validMoves.append("l")
    if isValid(board, x, y + 1):
        validMoves.append("r")
    return validMoves

#get the position of the agent on the board
def getAgentPos(board):
    for i in range(size):
        for j in range(size):
            if board[i][j] == "S":
                return i, j




#cost function of a move (calculates how many cells the agent will color if it makes a move)
def cost(_board, move):
    x, y = getAgentPos(_board)
    count = 0
    if move == "u":
        while isValid(_board, x - 1, y):
            x -= 1
            count += 1
    if move == "d":
        while isValid(_board, x + 1, y):
            x += 1
            count += 1
    if move == "l":
        while isValid(_board, x, y - 1):
            y -= 1
            count += 1
    if move == "r":
        while isValid(_board, x, y + 1):
            y += 1
            count += 1
    return count



#heuristic function 1 (returns the number of 0s left on the board multiplied by 10000)
def heuristic1(board):
    count = 0
    for i in range(size):
        for j in range(size):
            if board[i][j] == "0":
                count += 1
    return count*5

#heuristic function 2 (returns the number of 0s left on the board)
def heuristic2(board):
    count = 0
    for i in range(size):
        for j in range(size):
            if board[i][j] == "0":
                count += 1
    return count

#heuristic function 3 (inadmissible heuristic function)


#function to make a move (changes the board and returns the new state of the board. the agent pos is where S is)
def makeMove(board,move):
    #copy the board
    newBoard = [row[:] for row in board]

    x, y = getAgentPos(board)
    #set the current cell to 1 
    newBoard[x][y] = "1"
    #set all the cells until a wall to 1 in the move direction and set the last cell to S
    
    if move == "u":
        while isValid(board, x - 1, y):
            x -= 1
            newBoard[x][y] = "1"
    if move == "d":
        while isValid(board, x + 1, y):
            x += 1
            newBoard[x][y] = "1"
    if move == "l":
        while isValid(board, x, y - 1):
            y -= 1
            newBoard[x][y] = "1"
    if move == "r":
        while isValid(board, x, y + 1):
            y += 1
            newBoard[x][y] = "1"
            
    newBoard[x][y] = "S"

        
    return newBoard

#function that plays the game using the moves in a list and prints the board after each move
def playGame(board, moves,willPrint = False):
    #print the initial board
    if willPrint:
        printBoard(board)
    for move in moves:
        if move in getValidMoves(board, getAgentPos(board)[0], getAgentPos(board)[1]):
            if willPrint:
                print("Move: ", move)
            board = makeMove(board, move)
            
        else:
            print("Invalid move")
        #print the board after each move
        if willPrint:
            printBoard(board)




#a* search algorithm using given heuristic function

def aStarSearch(board, heuristic):
    frontier = []
    totalNumberOfExpandedNodes = 0
    visited = set()  # visited set to keep track of visited states
    heapq.heappush(frontier, (0, 0, (board, [])))  # frontier is a priority queue with the priority being the f-value and g-value

    while frontier:
        _, g_score, (current_board, current_moves) = heapq.heappop(frontier) # pop the state with the lowest f-value (expand the node from the frontier)

        totalNumberOfExpandedNodes += 1
        
        # convert the board to a tuple so it can be added to the visited set
        current_board_tuple = tuple(map(tuple, current_board))
        
        if current_board_tuple in visited:  # if the current board is already visited, skip it
            continue  
        
        visited.add(current_board_tuple)  # add to visited set

        if isSolved(current_board):  # if the current board is solved, return the moves (path to the solution)
            return current_moves, g_score, totalNumberOfExpandedNodes
        
        ############################
        # expanding the frontier ###
        ############################

        moves = getValidMoves(current_board, getAgentPos(current_board)[0], getAgentPos(current_board)[1])
        
        for move in moves:
            new_board = makeMove(current_board, move)
            new_moves = current_moves + [move]
            new_g_score = g_score + cost(current_board, move)  # Update the g_score 

            priority = new_g_score + heuristic(new_board)  # f-value = g-value + h-value
            heapq.heappush(frontier, (priority, new_g_score, (new_board, new_moves)))  # Include the updated g_score to break ties

    return "No solution found"



from memory_profiler import memory_usage
import time

def benchmarker(filename, heuristic):
    file = open(filename, "r")
    size = int(file.readline())
    board = []
    for i in range(size):
        board.append(list(file.readline().strip()))
    file.close()

    def wrapper():
        return aStarSearch(board, heuristic)

    start_time = time.time()
    mem_usage, (moves, totalCost,totalExpandedNodes ) = memory_usage((wrapper,), max_usage=True, retval=True)
    end_time = time.time()

    print("Time of "+ filename+": ", end_time - start_time)
    print("Total cost of "+ filename+": ", totalCost)
    print("Peak memory usage of "+ filename+": ", mem_usage, "MiB")
    print("Total expanded nodes of "+ filename+": ", totalExpandedNodes)

    playGame(board, moves)

    return end_time - start_time, totalCost, mem_usage, totalExpandedNodes


def findSmallestRectangle(board):
    #find the smallest rectangle that contains all the 0s
    minX = size
    minY = size
    maxX = 0
    maxY = 0
    for i in range(size):
        for j in range(size):
            if board[i][j] == "0":
                if i < minX:
                    minX = i
                if i > maxX:
                    maxX = i
                if j < minY:
                    minY = j
                if j > maxY:
                    maxY = j

    return minX, minY, maxX, maxY

def countCellsFromFile(filename):
    file = open(filename, "r")
    size = int(file.readline())
    board = []
    for i in range(size):
        board.append(list(file.readline().strip()))
    file.close()
    
    #find the smallest rectangle that contains all the 0s
    minX, minY, maxX, maxY = findSmallestRectangle(board)

    #count the cells in the rectangle
    return (maxX - minX + 1) * (maxY - minY + 1)
        





if __name__ == '__main__':

    #benchmark the a* search algorithm using heuristic1 for the following files
    #easy_level1.txt, easy_level2.txt, easy_level3.txt, easy_level4.txt, easy_level5.txt
    #normal_level1.txt, normal_level2.txt, normal_level3.txt, normal_level4.txt, normal_level5.txt
    #hard_level1.txt, hard_level2.txt, hard_level3.txt, hard_level4.txt, hard_level5.txt

    #ask the user if they want to benchmark the a* search algorithm
    benchmark = input("Do you want to benchmark the a* search algorithm? (y/n) ") == "y"

    if benchmark:
    
        heuristic1TimeData = []
        heuristic1CostData = []
        heuristic1MemoryData = []
        heuristic1ExpandedNodesData = []

        heuristic2TimeData = []
        heuristic2CostData = []
        heuristic2MemoryData = []
        heuristic2ExpandedNodesData = []

        levelCellCountdata=[]
        print("Heuristic 1 results:")


        #get all level file cell counts
        for i in range(1,6):
            levelCellCountdata.append(countCellsFromFile("easy_level" + str(i) + ".txt"))
        for i in range(1,6):
            levelCellCountdata.append(countCellsFromFile("normal_level" + str(i) + ".txt"))
        for i in range(1,6):
            levelCellCountdata.append(countCellsFromFile("hard_level" + str(i) + ".txt"))

        totalTime = 0
        for i in range(1,6):
            timeOfLevel,costOfLevel,memoryOfLevel,expandedNodesOfLevel= benchmarker("easy_level" + str(i) + ".txt", heuristic1)
            totalTime+= timeOfLevel
            heuristic1CostData.append(costOfLevel)
            heuristic1TimeData.append(timeOfLevel)
            heuristic1MemoryData.append(memoryOfLevel)
            heuristic1ExpandedNodesData.append(expandedNodesOfLevel)
            
            board = []

        for i in range(1,6):
            timeOfLevel,costOfLevel,memoryOfLevel,expandedNodesOfLevel= benchmarker("normal_level" + str(i) + ".txt", heuristic1)
            totalTime+= timeOfLevel
            heuristic1CostData.append(costOfLevel)
            heuristic1TimeData.append(timeOfLevel)
            heuristic1MemoryData.append(memoryOfLevel)
            heuristic1ExpandedNodesData.append(expandedNodesOfLevel)
            board = []

        for i in range(1,6):
            timeOfLevel,costOfLevel,memoryOfLevel,expandedNodesOfLevel = benchmarker("hard_level" + str(i) + ".txt", heuristic1)
            totalTime+= timeOfLevel
            heuristic1CostData.append(costOfLevel)
            heuristic1TimeData.append(timeOfLevel)
            heuristic1MemoryData.append(memoryOfLevel)
            heuristic1ExpandedNodesData.append(expandedNodesOfLevel)
            board = []

        print("Total time of Heuristic 1: ", totalTime)
        totalTime = 0
        print("Heuristic 2 results:")

        for i in range(1,6):
            timeOfLevel,costOfLevel,memoryOfLevel,expandedNodesOfLevel= benchmarker("easy_level" + str(i) + ".txt", heuristic2)
            totalTime+= timeOfLevel
            heuristic2CostData.append(costOfLevel)
            heuristic2TimeData.append(timeOfLevel)
            heuristic2MemoryData.append(memoryOfLevel)
            heuristic2ExpandedNodesData.append(expandedNodesOfLevel)
            board = []

        for i in range(1,6):
            timeOfLevel,costOfLevel,memoryOfLevel,expandedNodesOfLevel= benchmarker("normal_level" + str(i) + ".txt", heuristic2)
            totalTime+= timeOfLevel
            heuristic2CostData.append(costOfLevel)
            heuristic2TimeData.append(timeOfLevel)
            heuristic2MemoryData.append(memoryOfLevel)
            heuristic2ExpandedNodesData.append(expandedNodesOfLevel)
            board = []


        for i in range(1,6):
            timeOfLevel,costOfLevel,memoryOfLevel,expandedNodesOfLevel= benchmarker("hard_level" + str(i) + ".txt", heuristic2)
            totalTime+= timeOfLevel
            heuristic2CostData.append(costOfLevel)
            heuristic2TimeData.append(timeOfLevel)
            heuristic2MemoryData.append(memoryOfLevel)
            heuristic2ExpandedNodesData.append(expandedNodesOfLevel)
            board = []

        print("Total time of Heuristic 2: ", totalTime)




        print("Heuristic 1 cost data: ", heuristic1CostData)
        print("Heuristic 1 time data: ", heuristic1TimeData)
        print("Heuristic 1 memory data: ", heuristic1MemoryData)
        print("############################################")
        print("Heuristic 2 cost data: ", heuristic2CostData)
        print("Heuristic 2 time data: ", heuristic2TimeData)
        print("Heuristic 2 memory data: ", heuristic2MemoryData)

        #plot the results of the benchmark for memory usage, time and cost
        import matplotlib.pyplot as plt
        import numpy as np

        # Sample arrays


        # Plotting for cost
        plt.figure()
        plt.plot(range(len(heuristic1CostData)), heuristic1CostData, color='blue', label='Heuristic 1', marker='o')
        plt.plot(range(len(heuristic2CostData)), heuristic2CostData, color='red', label='Heuristic 2', marker='x')
        plt.xlabel('Level')
        plt.ylabel('Total Cost')
        plt.title('Cost Comparison')
        plt.legend()
        plt.savefig('benchmarkResults/costs.png')


        # Plotting for time
        plt.figure()
        plt.yscale('log')
        plt.plot(range(len(heuristic1TimeData)), heuristic1TimeData, color='blue', label='H1 time', marker='o')
        plt.plot(range(len(heuristic2TimeData)), heuristic2TimeData, color='red', label='H2 time', marker='x')
        plt.xlabel('Level')
        plt.ylabel('Time')
        plt.title('Time Comparison')
        plt.legend()

        plt.savefig('benchmarkResults/times.png')


        # Plotting for memory usage
        plt.figure()
        plt.yscale('log')
        plt.plot(range(len(heuristic1MemoryData)), heuristic1MemoryData, color='blue', label='H1 memory use', marker='o')
        plt.plot(range(len(heuristic2MemoryData)), heuristic2MemoryData, color='red', label='H2 memory use', marker='x')
        plt.xlabel('Level')
        plt.ylabel('Memory Usage')
        plt.title('Memory Usage Comparison')
        plt.legend()
        plt.savefig('benchmarkResults/memory.png')


        #plot the expanded notes data
        plt.figure()
        plt.plot(range(len(heuristic1ExpandedNodesData)), heuristic1ExpandedNodesData, color='blue', label='Heuristic 1', marker='o')
        plt.plot(range(len(heuristic2ExpandedNodesData)), heuristic2ExpandedNodesData, color='red', label='Heuristic 2', marker='x')
        plt.xlabel('Level')
        plt.ylabel('Total Expanded Nodes')
        plt.title('Expanded Nodes Comparison')
        plt.legend()
        plt.savefig('benchmarkResults/expandedNodes.png')



        #plot all of the data using a table
        fig, ax = plt.subplots()
        # hide axes
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')
        data = []
        for i in range(5):
            data.append(["easy_level" + str(i + 1) + ".txt", levelCellCountdata[i], heuristic1CostData[i], heuristic1TimeData[i], heuristic1MemoryData[i], heuristic2CostData[i], heuristic2TimeData[i], heuristic2MemoryData[i],heuristic1ExpandedNodesData[i],heuristic2ExpandedNodesData[i]])
        for i in range(5):
            data.append(["normal_level" + str(i + 1) + ".txt", levelCellCountdata[i+5], heuristic1CostData[i+5], heuristic1TimeData[i+5], heuristic1MemoryData[i+5], heuristic2CostData[i+5], heuristic2TimeData[i+5], heuristic2MemoryData[i+5],heuristic1ExpandedNodesData[i+5],heuristic2ExpandedNodesData[i+5]])
        for i in range(5):
            data.append(["hard_level" + str(i + 1) + ".txt", levelCellCountdata[i+10], heuristic1CostData[i+10], heuristic1TimeData[i+10], heuristic1MemoryData[i+10], heuristic2CostData[i+10], heuristic2TimeData[i+10], heuristic2MemoryData[i+10],heuristic1ExpandedNodesData[i+10],heuristic2ExpandedNodesData[i+10]])

        column_labels = ["Level", "Cell Count", "H1 Cost", "H1 Time", "H1 Memory", "H2 Cost", "H2 Time", "H2 Memory","H1 Expanded Nodes","H2 Expanded Nodes"]
        ax.table(cellText=data, colLabels=column_labels, loc='center')
        fig.tight_layout()
        plt.savefig('benchmarkResults/table.png',dpi = 300)





#this was used for testing if the game is played correctly

#play the ggame by player input
#while not isSolved(board):
#    printBoard(board)
#    move = input("Enter a move: ")
#    if move in getValidMoves(board, getAgentPos(board)[0], getAgentPos(board)[1]):
#        totalCost += cost(board, move)
#        board = makeMove(board, move)
#    else:
#        print("Invalid move")


    exit = input("Do you want to exit? (y/n) ") == "n"
    while exit:
        #ask the user for the level file
        level = input("Enter the level file: ")
        file = open(level, "r")
        size = int(file.readline())
        board = []
        for i in range(size):
            board.append(list(file.readline().strip()))
        file.close()
        #play the game using the a* search algorithm with heuristic 2
        moves, totalCost,totalExpanedNodes = aStarSearch(board, heuristic2)
        playGame(board, moves,True)
        print("Total cost: ", totalCost)
        print("Total expanded nodes: ", totalExpanedNodes)
        #ask the user if they want to exit
        exit = input("Do you want to exit? (y/n) ") == "n"

