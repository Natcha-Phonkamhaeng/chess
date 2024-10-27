import pygame
from engine import GameState, Move


WIDTH =  HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION # 64
MAX_FPS = 15
IMAGES = {}

def load_images():
	pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']
	for piece in pieces:
		IMAGES[piece] = pygame.transform.scale(pygame.image.load(f'images/{piece}.png'), (SQ_SIZE, SQ_SIZE))


def hightlight_square(screen, gs, valid_move, sq_selected):
	'''
	highlight square selected and moves for piece selected
	'''
	if sq_selected != ():
		row, col = sq_selected
		if gs.board[row][col][0] == ('w' if gs.white_to_move else 'b'):
			s = pygame.Surface((SQ_SIZE, SQ_SIZE)) # create hightlight with pygame surface
			s.set_alpha(100) # transparency value -> 0 is pure transparency
			s.fill(pygame.Color('blue'))
			screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
			# hight moves from that square
			s.fill(pygame.Color('yellow'))
			for move in valid_move:
				if move.start_row == row and move.start_col == col:
					screen.blit(s, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))


def draw_game_state(screen, gs, valid_move, sq_selected):
	draw_board(screen)
	hightlight_square(screen, gs, valid_move, sq_selected)
	draw_pieces(screen, gs.board)


def draw_board(screen):
	colors = [pygame.Color('white'), pygame.Color('grey')] # return aka => [(255, 255, 255, 255), (190, 190, 190, 255)]
	for row in range(DIMENSION):
		for col in range(DIMENSION):
			color = colors[(row + col)%2] # return 0 and 1 => 0 for white, 1 for black
			pygame.draw.rect(screen, color, pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
	for row in range(DIMENSION):
		for col in range(DIMENSION):
			piece = board[row][col] # return gs.board[0][0] which is 'bR' in GameState
			if piece != '--':
				screen.blit(IMAGES[piece], pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def main():
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()
	screen.fill(pygame.Color('white'))
	gs = GameState()
	valid_move = gs.get_valid_move()
	move_made = False

	load_images()
	running = True
	sq_selected = () # return (row, col) to keep track of last click of the users
	player_click = [] # return [(6,4), (4,4)] to keep track of users click

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				location = pygame.mouse.get_pos() # return (x,y)
				col = location[0]//SQ_SIZE
				row = location[1]//SQ_SIZE
				# print(f'location: {location}, col: {col}, row: {row}')
				if sq_selected == (row, col): # if users click the same square twice
					sq_selected = ()
					player_click = []
					# print(f'selected square: {sq_selected}')
				else:
					sq_selected = (row, col)
					player_click.append(sq_selected) # append for both 1st and 2nd click
					# print(f'selected square: {sq_selected}')
				if len(player_click) == 2: # logic we want to move the pieces for the users
					move = Move(player_click[0], player_click[1], gs.board)
					print(move.get_chess_notation())
					for i in range(len(valid_move)):
						if move == valid_move[i]:
							gs.make_move(valid_move[i])
							move_made = True
							sq_selected = ()
							player_click = []
					if not move_made:
						player_click = [sq_selected]
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_z: # undo the last move
					gs.undo_move()
					move_made = True

		if move_made:
			valid_move = gs.get_valid_move()
			move_made = False

		draw_game_state(screen, gs, valid_move, sq_selected)
		clock.tick(MAX_FPS)
		pygame.display.flip()
		




if __name__ == '__main__':
	main()


