# FIX DISPLAYING BLOCKS

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

# PLAYER OBJECT

class Player():
    def __init__(self, num, colors):
        self.num = num
        self.color = colors[self.num]
        self.blocks = [[[1]], [[1,1]], [[1,1,1]], [[1,1,1,1]], [[1,1,1,1,1]], [[1,1],[0,1]], [[1,1,1],[0,0,1]], [[1,1,1],[0,1,0]], [[1,1],[1,1]], [[1,1,0],[0,1,1]], [[1,1,1,1],[1,0,0,0]], [[1,1,1,0],[0,0,1,1]], [[1,1,1],[0,1,1]], [[1,1,1],[0,0,1],[0,0,1]], [[0,1,1],[1,1,0],[1,0,0]], [[1,1,0],[0,1,0],[0,1,1]], [[1,1],[0,1],[1,1]], [[0,1,0,0],[1,1,1,1]], [[0,1,0],[1,1,1],[0,1,0]], [[1,1,0],[0,1,1],[0,1,0]], [[0,0,1],[1,1,1],[0,0,1]]]
        sleep(0.5)
        self.name = self.getName()
        print()

    def getName(self):
        return input(colored_txt(f"Player {self.num+1} name:\n", self.color)+change_col((74,134,232)))
    
    def turn(self):
        self.displayName()
        self.displayBlocks()
    
    def displayName(self):
        printStuff = " "*int(50 - len(self.name)/2) + self.name
        print(colored_txt(printStuff, self.color))
        print()
    
    def displayBlocks(self):
        printStuff = []
        for i in range(3):
            printStuff.append("")
            for block in self.blocks:
                try:
                    for b in range(len(block[i])):
                        block[i][b] = colored_txt("  ", [(0,0,0), self.color][block[i][b]], True)
                    printStuff[i] += "".join(block[i])
                    printStuff[i] += "  "
                except:
                    printStuff[i] += " "*len(block[0]) + "  "
        printStuff.append("")

        while len(printStuff[-2]) > 101:
            printStuffLen = len(printStuff)
            for i in range(printStuffLen):
                printStuff.append(printStuff[i][101:])
                printStuff[i] = printStuff[i][:101]
            printStuff.append("")

        for i in printStuff:
            print(i)

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
    colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0)]

    board, players, totalPlayers, currentPlayer = setup(colors)

    sleep(1)
    clear_screen()

    printBoard(board, colors)

    players[currentPlayer].turn()

main()