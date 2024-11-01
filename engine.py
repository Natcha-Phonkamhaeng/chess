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
		self.white_king_location = (7,4)
		self.black_king_location = (0,4)
		self.checkmate = False
		self.stalemate = False
		self.enpassant_possible = () # coordinate for the square where en passant capture is possible
		self.current_castling_right = CastleRights(True, True, True, True)
		self.castle_rights_log = [CastleRights(self.current_castling_right.wks, self.current_castling_right.bks, 
											   self.current_castling_right.wqs, self.current_castling_right.bqs)]


	def make_move(self, move):
		'''
		basic chess move does not include catling and pawn promotion etc.
		'''
		self.board[move.start_row][move.start_col] = '--'
		self.board[move.end_row][move.end_col] = move.piece_moved
		self.move_log.append(move)
		self.white_to_move = not self.white_to_move
		# update king location after moved
		if move.piece_moved == 'wK':
			self.white_king_location = (move.end_row, move.end_col)
		elif move.piece_moved == 'bK':
			self.black_king_location = (move.end_row, move.end_col)

		# pawn promotion
		if move.is_pawn_promotion:
			self.board[move.end_row][move.end_col] = move.piece_moved[0]+'Q'

		# en passant
		if move.is_enpassant_move:
			self.board[move.start_row][move.end_col] = '--' # capturing pawn

		# update enpassant_possible variable
		if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2: # update only 2 sq pawn advance
			self.enpassant_possible = ((move.start_row + move.end_row)//2, move.start_col)
		else:
			self.enpassant_possible = ()

		# castling move
		if move.is_castle_move:
			if move.end_col - move.start_col == 2: # king side move
				self.board[move.end_row][move.end_col-1] = self.board[move.end_row][move.end_col+1] # move rook
				self.board[move.end_row][move.end_col+1] = '--' # erase the old rook
			else: # queen side move
				self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-2] # move rook
				self.board[move.end_row][move.end_col-2] = '--' # erase the old rook

		# update the castle rights - whenver it is a rook or a king move
		self.update_castle_rights(move)
		self.castle_rights_log.append(CastleRights(self.current_castling_right.wks, self.current_castling_right.bks,
											   self.current_castling_right.wqs, self.current_castling_right.bqs))


	def undo_move(self):
		if len(self.move_log) != 0: # make sure that there's a move to undo
			move = self.move_log.pop() # pop the last moved
			self.board[move.start_row][move.start_col] = move.piece_moved
			self.board[move.end_row][move.end_col] = move.piece_captured
			self.white_to_move = not self.white_to_move
			if move.piece_moved == 'wK':
				self.white_king_location = (move.start_row, move.start_col)
			elif move.piece_moved == 'bK':
				self.black_king_location = (move.start_row, move.start_col)
			# undo en passant
			if move.is_enpassant_move:
				self.board[move.end_row][move.end_col] = '--' #leave landing square blank
				self.board[move.start_row][move.end_col] = move.piece_captured
				self.enpassant_possible = (move.end_row, move.end_col)
			# undo 2 sq pawn advance
			if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
				self.enpassant_possible = ()
			# undo castling rights
			self.castle_rights_log.pop()
			self.current_castling_right = self.castle_rights_log[-1] # last object
			# undo castling move
			if move.is_castle_move:
				if move.end_col - move.start_col == 2: #king side
					self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-1]
					self.board[move.end_row][move.end_col-1] = '--'
				else: #queenside
					self.board[move.end_row][move.end_col-2] = self.board[move.end_row][move.end_col+1]
					self.board[move.end_row][move.end_col+1] = '--'


	def update_castle_rights(self, move):
		if move.piece_moved == 'wK':
			self.current_castling_right.wks = False
			self.current_castling_right.wqs = False
		elif move.piece_moved == 'bK':
			self.current_castling_right.bks = False
			self.current_castling_right.bqs = False
		elif move.piece_moved == 'wR':
			if move.start_row == 7:
				if move.start_col == 0: # white left rook
					self.current_castling_right.wqs = False
				elif move.start_col == 7: # white right rook
					self.current_castling_right.wks = False
		elif move.piece_moved == 'bR':
			if move.start_row == 0:
				if move.start_col == 0: # black left rook
					self.current_castling_right.bqs = False
				elif move.start_col == 7: # black right rook
					self.current_castling_right.bks = False


	def get_valid_move(self):
		temp_enpassant_possible = self.enpassant_possible
		temp_castling_rights = CastleRights(self.current_castling_right.wks, self.current_castling_right.bks,
			                                self.current_castling_right.wqs, self.current_castling_right.bqs)
		move = self.get_all_possible_move()
		if self.white_to_move:
			self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], move)
		else:
			self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], move)

		for i in range(len(move)-1,-1,-1):
			self.make_move(move[i])
			self.white_to_move = not self.white_to_move
			if self.in_check():
				move.remove(move[i])
			self.white_to_move = not self.white_to_move
			self.undo_move()
		if len(move) == 0:
			if self.in_check():
				self.checkmate = True
			else:
				self.stalemate = True
		else:
			self.checkmate = False
			self.stalemate = False

		self.enpassant_possible = temp_enpassant_possible
		self.current_castling_right = temp_castling_rights
		return move

	def in_check(self):
		if self.white_to_move:
			return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
		else:
			return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

	def square_under_attack(self, row, col):
		self.white_to_move = not self.white_to_move
		opp_move = self.get_all_possible_move()
		self.white_to_move = not self.white_to_move
		for move in opp_move:
			if move.end_row == row and move.end_col == col:
				return True
		return False

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
				elif (row-1, col-1) == self.enpassant_possible:
					move.append(Move((row, col), (row-1, col-1), self.board, is_enpassant_move=True))
			if col+1 <= 7: #captures on the right
				if self.board[row-1][col+1][0] == 'b': # captured black piece
					move.append(Move((row, col), (row-1, col+1), self.board))
				elif (row-1, col+1) == self.enpassant_possible:
					move.append(Move((row, col), (row-1, col+1), self.board, is_enpassant_move=True))
			
		else: # black pawn move
			if self.board[row+1][col] == "--": # 1 sq black pawn advance
				move.append(Move((row, col), (row+1, col), self.board))
				if row == 1 and self.board[row+2][col] == "--": # 2 sq pawn advance
					move.append(Move((row, col), (row+2, col), self.board))
			
			if col-1 >= 0: # capture on the left
				if self.board[row+1][col-1][0] == "w": # capture white on the left
					move.append(Move((row, col), (row+1, col-1), self.board))
				elif (row+1, col-1) == self.enpassant_possible:
					move.append(Move((row, col), (row+1, col-1), self.board, is_enpassant_move=True))
			if col+1 <= 7: # capture on the right
				if self.board[row+1][col+1][0] == "w": # capture white on the right
					move.append(Move((row, col), (row+1, col+1), self.board))
				elif (row+1, col+1) == self.enpassant_possible:
					move.append(Move((row, col), (row+1, col+1), self.board, is_enpassant_move=True))
		# add pawn promotion later


	def get_rook_move(self, row, col, move):
		directions = ((-1,0), (0,-1), (1,0), (0,1)) # up, left, down, right
		enemy_color = 'b' if self.white_to_move else 'w'
		'''
		this is equal to
		if self.white_to_move:
			enemy_color = 'b'
		else:	
			enemy_color = 'w'
		'''
		for d in directions:
			for i in range(1,8): # counting 1-7
				end_row = row + d[0] * i # d[0] is -1 0 1 0, when it multiply by 0 it will not move so it will move only row
				end_col = col + d[1] * i # d[1] is 0 -1 0 1, when it multiply by 0 it will not move so it will move only col
				if 0 <= end_row < 8 and 0<= end_col < 8: # check that move will still valid on board
					end_piece = self.board[end_row][end_col]
					if end_piece == '--': # rook landing on empty space
						move.append(Move((row, col), (end_row, end_col), self.board))
					elif end_piece[0] == enemy_color: # found enemy piece
						move.append(Move((row, col), (end_row, end_col), self.board))
						break # break the for loop, we will not jump the enemy piece
					else:
						break # break the loop, if we found our friend color, we will not jump and will not landing on our friend
				else:
					break # break if our rook move is off the board


	def get_bishop_move(self, row, col, move): # similar move like rook
		directions = ((-1,-1), (-1,1), (1,-1), (1,1))
		enemy_color = 'b' if self.white_to_move else 'w'
		for d in directions:
			for i in range(1,8):
				end_row = row + d[0] * i
				end_col = col + d[1] * i
				if 0<= end_row < 8 and 0<= end_col < 8:
					end_piece = self.board[end_row][end_col]
					if end_piece == '--':
						move.append(Move((row, col), (end_row, end_col), self.board))
					elif end_piece[0] == enemy_color:
						move.append(Move((row, col), (end_row, end_col), self.board))
						break
					else:
						break
				else:
					break


	def get_knight_move(self, row, col, move):
		directions = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
		ally_color = 'w' if self.white_to_move else 'b'
		for d in directions:
			end_row = row + d[0]
			end_col = col + d[1]
			if 0 <= end_row < 8 and 0 <= end_col < 8:
				end_piece = self.board[end_row][end_col]
				if end_piece[0] != ally_color:
					move.append(Move((row, col), (end_row, end_col), self.board))


	def get_queen_move(self, row, col, move): # queen can move like rook and bishop
		self.get_rook_move(row, col, move)
		self.get_bishop_move(row, col, move)


	def get_king_move(self, row, col, move):
		directions = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
		ally_color = 'w' if self.white_to_move else 'b'
		for i in range(8):
			end_row = row + directions[i][0]
			end_col = col + directions[i][1]
			if 0 <= end_row < 8 and 0 <= end_col < 8:
				end_piece = self.board[end_row][end_col]
				if end_piece[0] != ally_color:
					move.append(Move((row, col), (end_row, end_col), self.board))
		

	'''
	generate all valid castle moves for king (row, col) and add them to the list of moves
	'''
	def get_castle_moves(self, row, col, moves):
		if self.square_under_attack(row, col):
			return # can't castling while king in check
		if (self.white_to_move and self.current_castling_right.wks) or (not self.white_to_move and self.current_castling_right.bks):
			self.get_king_side_castle_moves(row, col, moves)
		if (self.white_to_move and self.current_castling_right.wqs) or (not self.white_to_move and self.current_castling_right.bqs):
			self.get_queen_side_castle_moves(row, col, moves)
			

	def get_king_side_castle_moves(self, row, col, moves):
		if self.board[row][col+1] == '--' and self.board[row][col+2] == '--':
			if not self.square_under_attack(row, col+1) and not self.square_under_attack(row, col+2):
				moves.append(Move((row, col), (row, col+2), self.board, is_castle_move=True))

	def get_queen_side_castle_moves(self, row, col, moves):
		if self.board[row][col-1] == '--' and self.board[row][col-2] == '--' and self.board[row][col-3]:
			if not self.square_under_attack(row, col-1) and not self.square_under_attack(row, col-2):
				moves.append(Move((row, col), (row, col-2), self.board, is_castle_move=True))


#################################################################################
class CastleRights:
	def __init__(self, wks, bks, wqs, bqs):
		self.wks = wks
		self.bks = bks
		self.wqs = wqs
		self.bqs = bqs


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

	def __init__(self, start_sq, end_sq, board, is_enpassant_move=False, is_castle_move=False):
		self.start_row = start_sq[0]
		self.start_col = start_sq[1]
		self.end_row = end_sq[0]
		self.end_col = end_sq[1]
		self.piece_moved = board[self.start_row][self.start_col]
		self.piece_captured = board[self.end_row][self.end_col]

		# pawn promotion
		self.is_pawn_promotion = (self.piece_moved == 'wp' and self.end_row == 0) or (self.piece_moved == 'bp' and self.end_row == 7)
		#### same as written below ####
		# self.is_pawn_promotion = False
		# if (self.piece_moved == 'wp' and self.end_row == 0) or (self.piece_moved == 'bp' and self.end_row == 7):
			# self.is_pawn_promotion = True
		
		# en passant
		self.is_enpassant_move = is_enpassant_move
		if self.is_enpassant_move:
			self.piece_captured = 'wp' if self.piece_moved =='bp' else 'bp'
		#castle move
		self.is_castle_move = is_castle_move
		

		self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

	def __eq__(self, other):
		if isinstance(other, Move):
			return self.move_id == other.move_id
		return False

	def get_rank_file(self, row, col):
		return self.cols_to_files[col] + self.rows_to_ranks[row]

	def get_chess_notation(self):
		return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

















