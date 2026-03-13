# NOTE:
# input question color: (0,255,255)
# input answer color: (74,134,232)
# error word color: (255,0,0)
# error message color: (200,0,0)

"""
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

rotated_clockwise = [list(row) for row in zip(*matrix[::-1])]

print(rotated_clockwise)
# Output: [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
"""

from time import sleep
import sys

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
        self.num = num
        self.color = colors[self.num+1]
        self.blocks = [[[[1]], [[1,1]], [[1,1,1]], [[1,1,1,1]], [[1,1,1,1,1]]], [[[1,1],[0,1]], [[1,1,1],[0,0,1]], [[1,1,1],[0,1,0]], [[1,1],[1,1]], [[1,1,0],[0,1,1]], [[1,1,1,1],[1,0,0,0]], [[1,1,1,0],[0,0,1,1]], [[1,1,1],[0,1,1]], [[0,1,0,0],[1,1,1,1],[0,0,0,0]]], [[[1,1,1],[0,0,1],[0,0,1]], [[0,1,1],[1,1,0],[1,0,0]], [[1,1,0],[0,1,0],[0,1,1]], [[1,1],[0,1],[1,1]], [[0,1,0],[1,1,1],[0,1,0]], [[1,1,0],[0,1,1],[0,1,0]], [[0,0,1],[1,1,1],[0,0,1]]]]
        sleep(0.5)
        self.name = self.getName()
        print()

    def getName(self):
        return input(colored_txt(f"Player {self.num+1} name:\n", self.color)+change_col((74,134,232)))
    
    def turn(self):
        self.displayName()
        self.displayBlocks()

        sleep(1)
        row, block = self.chooseBlock()

        pos = self.getBlockPos()

        possible = self.checkBlock(row, block, pos)
    
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

                for block in self.blocks[section]: # for each block in the section
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
        row = input(colored_txt(f"Chosen block row:\n", (0,255,255))+change_col((74,134,232)))

        while not row in ["1","2","3"]:
            print()
            print(colored_txt("ERROR", (255,0,0))+colored_txt(": block row must be in the range 1-3", (200,0,0)))
            print()
            row = input(colored_txt(f"Chosen block row:\n", (0,255,255))+change_col((74,134,232)))
        
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
        pos = input(colored_txt(f"Enter x,y coordinates of the top right pixel of the block (top right - bottom left)\nFormat: x,y (e.g. 53,29):\n", (0,255,255))+change_col((74,134,232)))

        pos = pos.split(",")

        while not (len(pos) == 2 and pos[0].isdigit() and pos[1].isdigit() and int(1 <= pos[0] <= 20) and int(1 <= pos[1] <= 20)):
            print()
            print(colored_txt("ERROR", (255,0,0))+colored_txt(": coordinates must be 2 numbers in the range 1-20 representing x and y seperated by commas", (200,0,0)))
            print()
            pos = input(colored_txt(f"Enter x,y coordinates of the top right pixel of the block (top right - bottom left)\nFormat: x,y (e.g. 53,29):\n", (0,255,255))+change_col((74,134,232)))
        
        pos = (int(pos[0])-1, int(pos[1])-1)

        print()

        return pos

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

    return board, players, totalPlayers, currentPlayer

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
    
    rules = f"""{colored_txt("RULES",(255,255,0))}

{colored_txt("""PLAYING THE GAME:
The first piece a player plays must touch one of the corners
Every other piece must be touching the corner of at least another piece of their own
It must not be touching a face of their own
It must not overlap""",(255,0,0))}

{colored_txt("""WINNING THE GAME:
Once everyone has forfeited, the player with the least amount of block tiles left will win""",(255,153,0))}
"""

    print(banner)
    sleep(1)
    print()
    print(rules)
    sleep(2)
    print()

def getPlayers():
    totalPlayers = int(input(colored_txt("Players: (2-4)\n", (0,255,255))+change_col((74,134,232))))
    while not 2 <= totalPlayers <= 4:
        print()
        print(colored_txt("ERROR", (255,0,0))+colored_txt(": number of players must be in between 2 and 4", (200,0,0)))
        print()
        totalPlayers = int(input(colored_txt("Players: (2-4)\n", (0,255,255))+change_col((74,134,232))))
    print()

    return totalPlayers

def printBoard(board, colors):
    printStuff = []
    printStuff.append(f"{change_col((255,255,255))}  ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══   ══")
    nextline = []
    
    for y in range(len(board)):
        nextline = []

        for x in range(len(board[y])):
            nextline.append(f"{colored_txt("██", colors[board[y][x]])}")
        
        printStuff.append("‖ " + " | ".join(nextline) + " ‖")

        printStuff.append("‖ ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   ——   —— ‖")
    
    for i in printStuff:
        print(i)
    
    print()

def main():
    colors = [(255,255,255), (255,0,0), (0,255,0), (0,0,255), (255,255,0)]

    board, players, totalPlayers, currentPlayer = setup(colors)

    sleep(1)
    clear_screen()

    printBoard(board, colors)

    sleep(1)
    players[currentPlayer].turn()

main()
