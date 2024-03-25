import numpy as np
import pygame
import sys
import math

GREY = (127, 127, 127)
BLACK = (0,0,0)
GREEN = (0,255,0)
MAGENTA = (255,0,255)

ROW_COUNT = 6
COLUMN_COUNT = 7

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
	#Connect 4 header
	#2 buttons, one "1 player", second "2 player"
	#one small quit button
	#if chosen 1-player button:
		#begin ai game
	#if chosen 2-player button:
		#begin 2-player game
	#if chosen quit button
		#pygame.time.wait(3000)
	return 0


board = createBoard()
printBoard(board)
gameOver = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()

print(pygame.font.get_fonts())
myfont = pygame.font.SysFont("applechancery", 50)

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
			
			# Get player 1 Input
			if turn == 0:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if isValidLocation(board, col):
					row = getNextOpenRow(board, col)
					placePiece(board, row, col, 1)

					if isWinningMove(board, 1):
						label = myfont.render("Player 1 wins!", 1, GREEN)
						screen.blit(label, (200,10))
						gameOver = True

			# Get player 2 Input
			else:				
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if isValidLocation(board, col):
					row = getNextOpenRow(board, col)
					placePiece(board, row, col, 2)

					if isWinningMove(board, 2):
						label = myfont.render("Player 2 wins!", 1, MAGENTA)
						screen.blit(label, (40,10))
						gameOver = True

			printBoard(board)
			drawBoard(board)

			turn += 1
			turn = turn % 2

			if gameOver:
				#mainMenu
				pygame.time.wait(3000)