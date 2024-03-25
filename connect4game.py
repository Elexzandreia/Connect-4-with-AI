import numpy as np
import pygame
import sys
import math
from button import Button

GREY = (127, 127, 127)
BLACK = (0,0,0)
GREEN = (0,255,0)
MAGENTA = (255,0,255)

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
RADIUS = int(SQUARESIZE/2 - 5)
size = (width, height)
pygame.init()
myfont = pygame.font.SysFont("applechancery", 70)
playerWinsFont = pygame.font.SysFont("applechancery", 50)
screen = pygame.display.set_mode(size)

def createBoard():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def placePiece(board, row, col, piece):
	board[row][col] = piece

def isValidLocation(board, col):
	return board[ROW_COUNT-1][col] == 0

def getNextOpenRow(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r
		
def isVerticalWin(board, piece):
	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

def isHorizontalWin(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True
			
def isDiagonalWin(board, piece):			
	# Check left to right diagonals
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True
	# Check right to left diagonals
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True
			
def printBoard(board):
	print(np.flip(board, 0))

def isWinningMove(board, piece):
	if isVerticalWin(board, piece) or isHorizontalWin(board, piece) or isDiagonalWin(board, piece):
		return True
	else:
		return False

def drawBoard(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, GREY, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, GREEN, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, MAGENTA, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

def mainMenu():
	while True:
		background = pygame.image.load("imageAssets/background.png")
		screen.blit(background, (0, 0))
		MENU_MOUSE_POS = pygame.mouse.get_pos()

		label = myfont.render("Connect Four", 1, MAGENTA)
		screen.blit(label, (150,70))
	
		TWO_PLAYERS_BUTTON = Button(image=pygame.image.load("imageAssets/2players.png"), pos =(350, 350))
        
		PLAY_AI_BUTTON = Button(image=pygame.image.load("imageAssets/playAI.png"), pos=(350, 485))
        
		QUIT_BUTTON = Button(image=pygame.image.load("imageAssets/quit.png"), pos=(350, 620))

		for button in [TWO_PLAYERS_BUTTON, PLAY_AI_BUTTON, QUIT_BUTTON]:
			button.update(screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if TWO_PLAYERS_BUTTON.checkForInput(MENU_MOUSE_POS):
					twoPlayers()
				if PLAY_AI_BUTTON.checkForInput(MENU_MOUSE_POS):
					playAI()
				if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
					pygame.quit()
					sys.exit()
		pygame.display.update()

def twoPlayers():
	board = createBoard()
	printBoard(board)
	gameOver = False
	turn = 0
	drawBoard(board)
	pygame.display.update()

	while not gameOver:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			if event.type == pygame.MOUSEMOTION:
				pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
				posx = event.pos[0]
				if turn == 0:
					pygame.draw.circle(screen, GREEN, (posx, int(SQUARESIZE/2)), RADIUS)
				else: 
					pygame.draw.circle(screen, MAGENTA, (posx, int(SQUARESIZE/2)), RADIUS)
			pygame.display.update()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
				
				if turn == 0: # Get player 1 Input
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))

					if isValidLocation(board, col):
						row = getNextOpenRow(board, col)
						placePiece(board, row, col, 1)

						if isWinningMove(board, 1):
							label = playerWinsFont.render("Player 1 wins!", 1, GREEN)
							screen.blit(label, (200,10))
							gameOver = True

				else:	# Get player 2 Input
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))

					if isValidLocation(board, col):
						row = getNextOpenRow(board, col)
						placePiece(board, row, col, 2)

						if isWinningMove(board, 2):
							label = playerWinsFont.render("Player 2 wins!", 1, MAGENTA)
							screen.blit(label, (200,10))
							gameOver = True

				printBoard(board)
				drawBoard(board)

				turn += 1
				turn = turn % 2

				if gameOver:
					pygame.time.wait(4000)
					mainMenu()
					
def playAI():
	while True:
		# call function to play AI game
		return 0

mainMenu()