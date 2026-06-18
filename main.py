# NOTE:
# input question color: (0,255,255)
# input answer color: (74,134,232)
# error word color: (255,0,0)
# error message color: (200,0,0)

# TODO:
# add codes e.g. 1

from time import sleep
import sys
from copy import deepcopy

# GENERAL FUNCTIONS THAT I NEED TO USE

def colored_txt(text, rgb:tuple, highlight:bool=False):
    r, g, b = rgb[0], rgb[1], rgb[2]
    if highlight:
        if rgb == (0,0,0):
            return text
        return f"\033[48;2;{r};{g};{b}m{text}\033[0m"
    return f"\x1b[38;2;{r};{g};{b}m{text}\x1b[0m"

def change_col(rgb: tuple):
    r, g, b = rgb[0], rgb[1], rgb[2]
    return f"\x1b[38;2;{r};{g};{b}m"

def clear_screen():
    sys.stdout.write('\033c')
    sys.stdout.flush()

# PLAYER OBJECT + FUNCTIONS

class Player():
    def __init__(self, num, colors):
        self.num = num + 1
        self.color = colors[self.num]
        self.blocks = [[[[1]], [[1,1]], [[1,1,1]], [[1,1,1,1]], [[1,1,1,1,1]]], [[[1,1],[0,1]], [[1,1,1],[0,0,1]], [[1,1,1],[0,1,0]], [[1,1],[1,1]], [[1,1,0],[0,1,1]], [[1,1,1,1],[1,0,0,0]], [[1,1,1,0],[0,0,1,1]], [[1,1,1],[0,1,1]], [[0,1,0,0],[1,1,1,1],[0,0,0,0]]], [[[1,1,1],[0,0,1],[0,0,1]], [[0,1,1],[1,1,0],[1,0,0]], [[1,1,0],[0,1,0],[0,1,1]], [[1,1],[0,1],[1,1]], [[0,1,0],[1,1,1],[0,1,0]], [[1,1,0],[0,1,1],[0,1,0]], [[0,0,1],[1,1,1],[0,0,1]]]]
        
        self.dead = False

        sleep(0.5)
        self.firstTurn = True
        self.name = self.getName()
        print()
    
    def getName(self):
        return input(colored_txt(f"Player {self.num} name:\n", self.color)+change_col((74,134,232)))
    
    def turn(self, board):
        self.displayName()
        self.displayBlocks()

        possible = None

        while possible in [False, None]:
            if possible == False:
                print(f"{colored_txt("ERROR", (255,0,0))}{colored_txt(": position not possible", (200,0,0))}")

            sleep(1)
            row, block = self.chooseBlock()

            sleep(1)
            rotated = self.displayRotations(row, block)

            sleep(0.5)
            rotation = self.chooseRotation()

            sleep(1)
            pos = self.getBlockPos()

            possible, boardCopy = self.checkBlock(rotated[rotation], pos, board)
        
        self.blocks[row].pop(block)

        if possible:
            board = deepcopy(boardCopy)
        
        self.firstTurn = False
        
        return board
    
    def displayName(self):
        printStuff = " "*int(50 - len(self.name)/2) + self.name
        print(colored_txt(printStuff, self.color))
        print()
    
    def displayBlocks(self):
        printStuff = []

        for section in range(len(self.blocks)): # for each section so the user can see easier
            printStuff.append("")
            for i in range(len(self.blocks[section][0])): # for each row in the first item in the list (all have same length)
                printStuff.append("")

                for block in deepcopy(self.blocks[section]): # for each block in the section
                    for b in range(len(block[i])): # for each pixel in the row of the block
                        block[i][b] = colored_txt("  ", [(0,0,0), self.color][block[i][b]], True)

                    printStuff[-1] += "".join(block[i])
                    printStuff[-1] += "  "

        printStuff.append("")

        printStuff.pop(0)

        # to add the numbers + align them
        for line in range(len(printStuff)):
            if line in [0, 2, 5]:
                printStuff[line] = f"{[1,1,2,2,2,3][line]}:  " + printStuff[line]
            
            else:
                printStuff[line] = "    " + printStuff[line]

        for i in printStuff:
            print(i)

    def chooseBlock(self):
        row = input(colored_txt(f"Chosen block row: (type 'help' for rules)\n", (0,255,255))+change_col((74,134,232)))

        while not row in ["1","2","3"]:
            print()

            if row == "help":
                printRules()

            else:
                print(colored_txt("ERROR", (255,0,0))+colored_txt(": block row must be in the range 1-3", (200,0,0)))
                print()

            row = input(colored_txt(f"Chosen block row: (type 'help' for rules)\n", (0,255,255))+change_col((74,134,232)))
        
        row = int(row)
        row -= 1

        print()

        sleep(0.5)

        block = input(colored_txt(f"Chosen block (count from left):\n", (0,255,255))+change_col((74,134,232)))

        while not (block.isdigit() and int(block) >= 1 and int(block) <= len(self.blocks[row])):
            print()
            print(colored_txt("ERROR", (255,0,0))+colored_txt(f": block number must be in the range 1-{len(self.blocks[row])}", (200,0,0)))
            print()
            block = input(colored_txt(f"Chosen block (count from left):\n", (0,255,255))+change_col((74,134,232)))

        block = int(block)
        block -= 1

        print()

        return row, block

    def getBlockPos(self):
        pos = input(colored_txt(f"Enter code of the top left pixel of the block\ne.g. AT, CP (case not sensitive):\n", (0,255,255))+change_col((74,134,232)))

        while not (len(pos) == 2 and pos.isalpha() and pos[0].lower() in "abcdefghijklmnopqrst" and pos[1].lower() in "abcdefghijklmnopqrst"):
            print()
            print(colored_txt("ERROR", (255,0,0))+colored_txt(": code must be 2 characters long, consisting of 2 letters", (200,0,0)))
            print()
            pos = input(colored_txt(f"Enter code of the top left pixel of the block\ne.g. AT, CP (case not sensitive):\n", (0,255,255))+change_col((74,134,232)))
        
        pos = ("abcdefghijklmnopqrst".index(pos[0].lower()), "abcdefghijklmnopqrst".index(pos[1].lower()))

        print()

        return pos

    def displayRotations(self, row, block):
        blocks = []
        next = deepcopy(self.blocks[row][block])

        for i in range(4):
            blocks.append(deepcopy(next))
            next = [list(r) for r in zip(*next[::-1])]

        printStuff = []
        
        length = 0
        for i in blocks:
            if len(blocks) > length:
                length = len(blocks)
        
        OGblocks = deepcopy(blocks)
                
        for i in range(length):
            printStuff.append("")

            for block in blocks: # for each block in the section
                if len(block) > i:
                    for b in range(len(block[i])): # for each pixel in the row of the block
                        block[i][b] = colored_txt("  ", [(0,0,0), self.color][block[i][b]], True)
                else:
                    block.append(list(block[0]))
                    for b in range(len(block[0])): # for each pixel in the row of the block
                        block[i][b] = colored_txt("  ", (0,0,0), True)

                printStuff[-1] += "".join(block[i])
                printStuff[-1] += "  "

        printStuff.append("")
        
        for i in range(len(blocks)):
            printStuff[-1] += str(i+1) + " "*(len(blocks[i][0])*2+1)

        for i in printStuff:
            if not i.strip() == "":
                print(i)
        
        print()

        return OGblocks

    def chooseRotation(self):
        rotation = input(colored_txt(f"Chosen rotation (1-4): (type 'help' for rules)\n", (0,255,255))+change_col((74,134,232)))

        while not rotation in ["1","2","3","4"]:
            print()

            if rotation == "help":
                printRules()

            else:
                print(colored_txt("ERROR", (255,0,0))+colored_txt(": rotation must be in the range 1-4", (200,0,0)))
                print()

            rotation = input(colored_txt(f"Chosen rotation (1-4): (type 'help' for rules)\n", (0,255,255))+change_col((74,134,232)))
        
        rotation = int(rotation)
        rotation -= 1

        print()

        return rotation

    def checkBlock(self, block, pos, board):
        chosenBlock = block

        boardCopy = deepcopy(board)

        for y in range(len(chosenBlock)):
            for x in range(len(chosenBlock[y])):
                try:
                    boardCopy[y+pos[1]][x+pos[0]] = chosenBlock[y][x] * self.num
                except:
                    return False, board
        
        # boardCopy = new. board = old
        possible = [checkOverlap(boardCopy, board), checkCorner(boardCopy, board, self.num, self.firstTurn), checkNoSide(boardCopy, board, self.num)]
        
        if all(possible):
            return True, boardCopy
        else:
            return False, board

    def checkDead(self, board):
        for row in range(len(self.blocks)):
            for block in range(len(self.blocks[row])):
                for y in range(len(board)):
                    for x in range(len(board[y])):
                        possible, boardCopy = self.checkBlock(self.blocks[row][block], (x,y), board)
                        if possible:
                            return
        
        self.dead = True
        return

def checkOverlap(boardCopy, board):
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] != boardCopy[y][x] and board[y][x] != 0:
                return False

    return True

def checkCorner(boardCopy, board, n, firstTurn):
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] != boardCopy[y][x]:
                if firstTurn:
                    if y in [19, 0] and x in [19, 0]:
                        return True
                    
                else:
                    check_max_y = y < 19
                    check_max_x = x < 19
                    check_min_y = y > 0
                    check_min_x = x > 0

                    if  check_max_y and check_max_x and board[y+1][x+1] == n or \
                        check_max_y and check_min_x and board[y+1][x-1] == n or \
                        check_min_y and check_max_x and board[y-1][x+1] == n or \
                        check_min_y and check_min_x and board[y-1][x-1] == n:

                        return True

    return False

def checkNoSide(boardCopy, board, n):
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] != boardCopy[y][x]:
                if  y < 19 and board[y+1][x] == n or \
                    y > 0  and board[y-1][x] == n or \
                    x < 19 and board[y][x+1] == n or \
                    x > 0  and board[y][x-1] == n:
                    
                    return False
    
    return True

# MY FUNCTIONS FOR STRUCTURED PROGRAMMING

def setup(colors):
    printSetup()

    totalPlayers = getPlayers()

    currentPlayer = 0

    board = []
    for y in range(20):
        board.append([])
        for _ in range(20):
            board[y].append(0)

    sleep(0.5)
    players = []
    for i in range(totalPlayers):
        players.append(Player(i, colors))

    return board, players, totalPlayers, currentPlayer, False

def printSetup():
    banner = f"""
=====================================================================================================
             ||    {colored_txt("      ", (0,0,255),True)}      {colored_txt("  ", (0,255,0),True)}          {colored_txt("    ", (0,255,0),True)}      {colored_txt("  ", (255,0,0),True)}  {colored_txt("  ", (255,0,0),True)}   {colored_txt("  ", (255,0,0),True)}    {colored_txt("  ", (255,0,0),True)}     {colored_txt("      ", (255,255,0),True)}    ||
             ||    {colored_txt("  ", (0,0,255),True)}    {colored_txt("  ", (0,0,255),True)}    {colored_txt("  ", (0,255,0),True)}        {colored_txt("  ", (0,255,0),True)}    {colored_txt("  ", (0,255,0),True)}    {colored_txt("    ", (255,0,0),True)}     {colored_txt("  ", (255,0,0),True)}    {colored_txt("  ", (255,0,0),True)}   {colored_txt("  ", (255,255,0),True)}          ||
             ||    {colored_txt("      ", (0,0,255),True)}      {colored_txt("  ", (0,255,0),True)}        {colored_txt("  ", (0,255,0),True)}    {colored_txt("  ", (0,255,0),True)}    {colored_txt("  ", (255,0,0),True)}       {colored_txt("  ", (255,0,0),True)}    {colored_txt("  ", (255,0,0),True)}     {colored_txt("    ", (255,255,0),True)}      ||
             ||    {colored_txt("  ", (0,0,255),True)}    {colored_txt("  ", (0,0,255),True)}    {colored_txt("  ", (0,255,0),True)}        {colored_txt("  ", (0,255,0),True)}    {colored_txt("  ", (0,255,0),True)}    {colored_txt("    ", (255,0,0),True)}     {colored_txt("  ", (255,0,0),True)}    {colored_txt("  ", (255,0,0),True)}         {colored_txt("  ", (255,255,0),True)}    ||
             ||    {colored_txt("      ", (0,0,255),True)}      {colored_txt("       ", (0,255,0),True)}     {colored_txt("    ", (0,255,0),True)}      {colored_txt("  ", (255,0,0),True)}  {colored_txt("  ", (255,0,0),True)}     {colored_txt("    ", (255,0,0),True)}     {colored_txt("      ", (255,255,0),True)}      ||
=====================================================================================================
"""
#     banner = f"""
# ██████╗░██╗░░░░░░█████╗░██╗░░██╗██╗░░░██╗░██████╗
# ██╔══██╗██║░░░░░██╔══██╗██║░██╔╝██║░░░██║██╔════╝
# ██████╦╝██║░░░░░██║░░██║█████═╝░██║░░░██║╚█████╗░
# ██╔══██╗██║░░░░░██║░░██║██╔═██╗░██║░░░██║░╚═══██╗
# ██████╦╝███████╗╚█████╔╝██║░╚██╗╚██████╔╝██████╔╝
# ╚═════╝░╚══════╝░╚════╝░╚═╝░░╚═╝░╚═════╝░╚═════╝░
#     """

    print(banner)
    sleep(1)
    print()

    printRules()

def printRules():
    rules = f"""{colored_txt("RULES",(255,255,0))}

{colored_txt("""PLAYING THE GAME:
The first piece a player plays must touch one of the corners
Every other piece must be touching the corner of at least another piece of their own
It must not be touching a face of their own
It must not overlap""",(255,0,0))}

{colored_txt("""WINNING THE GAME:
Once everyone has forfeited, the player with the least amount of block tiles left will win""",(255,153,0))}
"""
    print(rules)
    sleep(2)
    print()

def getPlayers():
    totalPlayers = input(colored_txt("Players: (2-4)\n", (0,255,255))+change_col((74,134,232)))
    while not (totalPlayers.isdigit() and 2 <= int(totalPlayers) <= 4):
        print()
        print(colored_txt("ERROR", (255,0,0))+colored_txt(": number of players must be in between 2 and 4", (200,0,0)))
        print()
        totalPlayers = input(colored_txt("Players: (2-4)\n", (0,255,255))+change_col((74,134,232)))

    totalPlayers = int(totalPlayers)

    print()

    return totalPlayers

def printBoard(board, colors):
    printStuff = []
    printStuff.append(f"{change_col((255,255,255))}  ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══")
    nextline = []

    alphabet = "abcdefghijklmnopqrst"
    
    for y in range(len(board)):
        nextline = []

        for x in range(len(board[y])):
            nextline.append(f"{colored_txt(f"{alphabet[x]}{alphabet[y]}", colors[board[y][x]], True)}")
        
        printStuff.append("‖ " + " | ".join(nextline) + " ‖")

        printStuff.append("‖ ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   —— ‖")
    
    for i in printStuff:
        print(i)
    
    print()

def main():
    colors = [(255,255,255), (255,0,0), (0,255,0), (0,0,255), (255,255,0)]

    board, players, totalPlayers, currentPlayer, gameOver = setup(colors)

    while not gameOver:
        sleep(1)
        clear_screen()

        players[currentPlayer].checkDead(board)

        printBoard(board, colors)

        sleep(1)
        board = players[currentPlayer].turn(board)

        currentPlayer += 1
        currentPlayer = currentPlayer % totalPlayers

main()
