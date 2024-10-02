class GameState:
	def __init__(self):
		self.board = [
			['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
			['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
			['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
		] # 8x8 dimention
		self.move_function = {
							'p': self.get_pawn_move, 
							'R': self.get_rook_move, 
							'B': self.get_bishop_move,
							'Q': self.get_queen_move,
							'K': self.get_king_move,
							'N': self.get_knight_move
							}
		self.white_to_move = True
		self.move_log = []


	def make_move(self, move):
		'''
		basic chess move does not include catling and pown promotion etc.
		'''
		self.board[move.start_row][move.start_col] = '--'
		self.board[move.end_row][move.end_col] = move.piece_moved
		self.move_log.append(move)
		self.white_to_move = not self.white_to_move

	def undo_move(self):
		if len(self.move_log) != 0: # make sure that there's a move to undo
			move = self.move_log.pop() # pop the last moved
			self.board[move.start_row][move.start_col] = move.piece_moved
			self.board[move.end_row][move.end_col] = move.piece_captured
			self.white_to_move = not self.white_to_move

	def get_valid_move(self):
		return self.get_all_possible_move()

	def get_all_possible_move(self):
		move = []
		for row in range(len(self.board)):
			for col in range(len(self.board)):
				turn = self.board[row][col][0] # get b or w move
				if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
					piece = self.board[row][col][1] # return pieces
					self.move_function[piece](row, col, move)
		return move

	def get_pawn_move(self, row, col, move):
		if self.white_to_move:
			if self.board[row-1][col] == "--": # 1 sq pawn advance
				move.append(Move((row, col), (row-1, col), self.board))
				if row == 6 and self.board[row-2][col] == "--": # 2 sq pawn advance
					move.append(Move((row, col), (row-2, col), self.board))
			if col-1 >= 0: # avoid moving to -1 and captures on the left
				if self.board[row-1][col-1][0] == "b": # captured black piece
					move.append(Move((row, col), (row-1, col-1), self.board))
			if col+1 <= 7: #captures on the right
				if self.board[row-1][col+1][0] == 'b': # captured black piece
					move.append(Move((row, col), (row-1, col+1), self.board))
			
		else: # black pawn move
			if self.board[row+1][col] == "--": # 1 sq black pawn advance
				move.append(Move((row, col), (row+1, col), self.board))
				if row == 1 and self.board[row+2][col] == "--": # 2 sq pawn advance
					move.append(Move((row, col), (row+2, col), self.board))
			if col-1 >= 0: # capture on the left
				if self.board[row+1][col-1][0] == "w": # capture white on the left
					move.append(Move((row, col), (row+1, col-1), self.board))
			if col+1 <= 7: # capture on the right
				if self.board[row+1][col+1][0] == "w": # capture white on the right
					move.append(Move((row, col), (row+1, col+1), self.board))
		# add pawn promotion later


	def get_rook_move(self, row, col, move):
		pass

	def get_bishop_move(self, row, col, move):
		pass

	def get_knight_move(self, row, col, move):
		pass

	def get_queen_move(self, row, col, move):
		pass

	def get_king_move(self, row, col, move):
		pass

#################################################################################
class Move:
	# maps keys to values with dictionary
	ranks_to_rows = {
	'1': 7,
	'2': 6,
	'3': 5,
	'4': 4,
	'5': 3,
	'6': 2,
	'7': 1,
	'8': 0
	}

	rows_to_ranks = {v:k for k,v in ranks_to_rows.items()}

	files_to_cols = {
	'a': 0,
	'b': 1,
	'c': 2,
	'd': 3,
	'e': 4,
	'f': 5,
	'g': 6,
	'h': 7
	}

	cols_to_files = {v:k for k,v in files_to_cols.items()}

	def __init__(self, start_sq, end_sq, board):
		self.start_row = start_sq[0]
		self.start_col = start_sq[1]
		self.end_row = end_sq[0]
		self.end_col = end_sq[1]
		self.piece_moved = board[self.start_row][self.start_col]
		self.piece_captured = board[self.end_row][self.end_col]
		self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

	def __eq__(self, other):
		if isinstance(other, Move):
			return self.move_id == other.move_id
		return False

	def get_rank_file(self, row, col):
		return self.cols_to_files[col] + self.rows_to_ranks[row]

	def get_chess_notation(self):
		return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

















