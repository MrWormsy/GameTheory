import axelrod as axl

from random import random, randint

theStrategies = [axl.Defector(), axl.Cooperator()]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Create a board game with a n * n size
def createBoard(n):
    board = []

    for i in range(n):
        temp = []
        for j in range(n):

            # If we have the middle of the board we need to set a,n invader
            if (i == j) and (i <= n/2 <= i + 1):
                temp.append(theStrategies[0])
            else:
                temp.append(theStrategies[1])

        board.append(temp)

    return board

def getNeighbors(board, i, j):

    neighbors = []

    if i - 1 >= 0:
        neighbors.append(board[i - 1][j])

    if i + 1 < len(board):
        neighbors.append(board[i + 1][j])

    if j - 1 >= 0:
        neighbors.append(board[i][j - 1])

    if j + 1 < len(board):
        neighbors.append(board[i][j + 1])

    return neighbors




def playXTurn(board, x):

    tempBoard = []

    a = 0

    for i in range(len(board)):

        temp = []

        for j in range(len(board[0])):

            # We count the number of win of a strategy

            countA = 0
            countB = 0

            theBest = None

            neighbors = getNeighbors(board, i, j)

            contest = []

            # We loop the neighbors
            for n in neighbors:

                match = axl.Match([n, board[i][j]], 100)
                match.play()

                winner = match.winner()

                # If we dont have a winner we choose randomly between the two strategies
                if not winner:
                    if randint(1, 2) == 1:
                        contest.append(n)
                    else:
                        contest.append(board[i][j])
                else:
                    contest.append(winner)



                """

                # If we dont get a winner that means we need to choose randomly between the two strategies
                if not winner:
                    if randint(1, 2) == 1:
                        if str(n) == str(theStrategies[0]):
                            countA += 1
                        else:
                            countB += 1
                    else:
                        if str(board[i][j]) == str(theStrategies[0]):
                            countA += 1
                        else:
                            countB += 1
                else:
                    if str(winner) == str(theStrategies[0]):
                        countA += 1
                    else:
                        countB += 1

                """

            # Then we dont a competition to know with one if the best between all those strategies

            temp.append(theBest)

        tempBoard.append(temp)

    return tempBoard

# Get the best strategy by the highest score (if there is the best score multiple times we choose randomly between all)
def getBestStrategyByBestScore(matchs):
    # We first need to get the highest score

    highestScore = -1

    for m in matchs:
        for s in m[1]:
            if s > highestScore:
                highestScore = s

    # Then we need to get the strategy(ies) that has this highest score

    bestStrategies = []

    for m in matchs:
        for i in range(2):
            if m[1][i] == highestScore:
                bestStrategies.append(m[0][i])

    if len(bestStrategies) == 1:
        return bestStrategies[0]
    else:
        return bestStrategies[randint(0, len(bestStrategies) - 1)]


def playTurn(board):

    tempBoard = []

    a = 0

    for i in range(len(board)):

        temp = []

        for j in range(len(board[0])):
            theBest = None
            theBestScores = 0

            matchs = []

            neighbors = getNeighbors(board, i, j)

            contest = []

            # We loop the neighbors
            for n in neighbors:

                match = axl.Match([n, board[i][j]], 100)
                match.play()

                # We see which strategy get the best score
                matchs.append([[n, board[i][j]], match.final_score()])

            temp.append(getBestStrategyByBestScore(matchs))

        tempBoard.append(temp)

    return tempBoard

def printBoard(board):
    for b in board:
        formatedString = ""
        for b2 in b:
            if (str(b2) == str(theStrategies[0])):
                formatedString += (bcolors.WARNING +  '# ')
            else:
                formatedString += (bcolors.OKBLUE + 'X ')
        print(formatedString)
    print("")

def main():

    # Number of generations
    numberOfGeneration = 10
    sizeOfTheBoard = 9

    # We fist create the board
    board = createBoard(sizeOfTheBoard)
    printBoard(board)

    for i in range(numberOfGeneration):
        board = playTurn(board)
        printBoard(board)

if __name__ == '__main__':
    main()