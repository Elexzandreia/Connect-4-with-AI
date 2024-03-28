from sharedFunctions import PLAYER_PIECE, AI_PIECE, ROW_COUNT, COLUMN_COUNT, WINDOW_LENGTH, isValidLocation, getNextOpenRow, isWinningMove, placePiece
import random
import math
# This file contains the functions solely used by the AI opponent.

def evaluateWindow(window, piece):
	EMPTY = 0
	score = 0
	oppPiece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		oppPiece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2
	
	if window.count(oppPiece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def scorePosition(board, piece):
	score = 0

	# Score center column
	centerArray = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	centerCount = centerArray.count(piece)
	score += centerCount * 3

	# Score horizontal
	for r in range(ROW_COUNT):
		rowArray = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = rowArray[c:c+WINDOW_LENGTH]
			score += evaluateWindow(window, piece)

	# Score vertical
	for c in range(COLUMN_COUNT):
		columnArray = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = columnArray[r:r+WINDOW_LENGTH]
			score += evaluateWindow(window, piece)

	# Score positive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluateWindow(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluateWindow(window, piece)

	return score

def isTerminalNode(board):
	return isWinningMove(board, PLAYER_PIECE) or isWinningMove(board, AI_PIECE) or len(getValidLocations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	validLocations = getValidLocations(board)
	isTerminal = isTerminalNode(board)
	if depth == 0 or isTerminal:
		if isTerminal:
			if isWinningMove(board, AI_PIECE):
				return (None, 100000000000000)
			elif isWinningMove(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, scorePosition(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(validLocations)
		for col in validLocations:
			row = getNextOpenRow(board, col)
			boardCopy = board.copy()
			placePiece(boardCopy, row, col, AI_PIECE)
			newScore = minimax(boardCopy, depth-1, alpha, beta, False)[1]
			if newScore > value:
				value = newScore
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(validLocations)
		for col in validLocations:
			row = getNextOpenRow(board, col)
			boardCopy = board.copy()
			placePiece(boardCopy, row, col, PLAYER_PIECE)
			newScore = minimax(boardCopy, depth-1, alpha, beta, True)[1]
			if newScore < value:
				value = newScore
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def getValidLocations(board):
	validLocations = []
	for col in range(COLUMN_COUNT):
		if isValidLocation(board, col):
			validLocations.append(col)
	return validLocations

def pickBestMove(board, piece):
	validLocations = getValidLocations(board)
	bestScore = -10000
	bestCol = random.choice(validLocations)

	for col in validLocations:
		row = getNextOpenRow(board, col)
		tempBoard = board.copy()
		placePiece(tempBoard, row, col, piece)
		score = scorePosition(tempBoard, piece)
		if score > bestScore:
			bestScore = score
			bestCol = col
	return bestCol
