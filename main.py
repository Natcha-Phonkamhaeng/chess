import pygame
from engine import GameState


WIDTH =  HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION # 64
MAX_FPS = 15
IMAGES = {}

def load_images():
	pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']
	for piece in pieces:
		IMAGES[piece] = pygame.transform.scale(pygame.image.load(f'images/{piece}.png'), (SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, gs):
	draw_board(screen)
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
	load_images()
	draw_game_state(screen, gs)
	running = True
	while running:
		for e in pygame.event.get():
			if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
				running = False
		clock.tick(MAX_FPS)
		pygame.display.flip()




if __name__ == '__main__':
	main()


