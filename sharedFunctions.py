# This file contains functions and variables shared by both files (connect4game.py and connect4AI.py)

PLAYER_PIECE = 1
AI_PIECE = 2
ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4

def isValidLocation(board, col):
	return board[ROW_COUNT-1][col] == 0

def getNextOpenRow(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def placePiece(board, row, col, piece):
	board[row][col] = piece

def isWinningMove(board, piece):
	if isVerticalWin(board, piece) or isHorizontalWin(board, piece) or isDiagonalWin(board, piece):
		return True
	else:
		return False

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
			
