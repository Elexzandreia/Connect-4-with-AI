import random
import numpy as np
import pygame
import sys
import math
from pygame import mixer
from button import Button
from connect4AI import minimax
from sharedFunctions import PLAYER_PIECE, AI_PIECE, ROW_COUNT, COLUMN_COUNT, isValidLocation, getNextOpenRow, isWinningMove, placePiece

GREY = (127, 127, 127) 
BLACK = (0,0,0)
GREEN = (0,255,0) 
MAGENTA = (255,0,255) 

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
RADIUS = int(SQUARESIZE/2 - 5)
size = (width, height)
pygame.init()
mixer.init()
myfont = pygame.font.SysFont("applechancery", 70)
playerWinsFont = pygame.font.SysFont("applechancery", 50)
screen = pygame.display.set_mode(size)
pygame.mixer.music.load("star-travelers.mp3")
pygame.mixer.music.set_volume(0.5)  # Adjust volume as needed (0.0 to 1.0)
pygame.mixer.music.play(-1)  # -1 indicates loop indefinitely

def createBoard():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def printBoard(board):
	print(np.flip(board, 0))

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
	turn = 0
	gameOver = False
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
		PLAYER = 0
		AI = 1
		gameOver = False

		board = createBoard()
		printBoard(board)
		drawBoard(board)
		pygame.display.update()

		turn = random.randint(PLAYER, AI)
		while not gameOver:
			for event in pygame.event.get():

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if turn == PLAYER:
						pygame.draw.circle(screen, GREEN, (posx, int(SQUARESIZE/2)), RADIUS)

				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					# Ask for Player 1 Input
					if turn == PLAYER:
						posx = event.pos[0]
						col = int(math.floor(posx/SQUARESIZE))

						if isValidLocation(board, col):
							row = getNextOpenRow(board, col)
							placePiece(board, row, col, PLAYER_PIECE)

							if isWinningMove(board, PLAYER_PIECE):
								label = playerWinsFont.render("Player 1 wins!", 1, GREEN)
								screen.blit(label, (200,10))
								gameOver = True

							turn += 1
							turn = turn % 2

							printBoard(board)
							drawBoard(board)

			# Ask for Player 2 Input
			if turn == AI and not gameOver:				
				col, minimaxScore = minimax(board, 5, -math.inf, math.inf, True)

				if isValidLocation(board, col):
					row = getNextOpenRow(board, col)
					placePiece(board, row, col, AI_PIECE)

					if isWinningMove(board, AI_PIECE):
						label = playerWinsFont.render("AI wins!", 1, MAGENTA)
						screen.blit(label, (250,10))
						gameOver = True

					printBoard(board)
					drawBoard(board)
					turn += 1
					turn = turn % 2

			if gameOver:
				pygame.time.wait(3000)
				mainMenu()

mainMenu()