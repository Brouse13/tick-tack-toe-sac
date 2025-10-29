import pygame

from broker import Client
from constants import *

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 60)

WIDTH = 3 * table_size
HEIGHT = 3 * table_size

window_size = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption(F"Tic Tac Toe ")

class TicTacToe:
	def __init__(self, player: str, client: Client):
		self.player = player
		self.winner = None
		self.table = ['-'] * 9
		self.FPS = pygame.time.Clock()
		self.running = True
		self.my_turn = self.player == 'X'
		self.client = client

		self.client.subscribe(f'tick-tack-toe-{self.player}')

	def __draw_table(self):
		row, col = 0, 0

		for element in self.table:
			x = col * table_size
			y = row * table_size

			# Fill the cell white
			pygame.draw.rect(screen, (255, 255, 255), [x, y, table_size, table_size])

			# Draw black border
			pygame.draw.rect(screen, (0, 0, 0), [x, y, table_size, table_size], 2)

			# Draw symbols
			if element == 'X': self.__draw_cross(col, row)
			elif element == 'O': self.__draw_circle(col, row)

			col += 1
			if col == 3: col = 0;row += 1

	def __draw_cross(self, row, col):
		pygame.draw.line(screen, cross_color,
						 [row * table_size, col * table_size],
						 [(row + 1) * table_size, (col + 1) * table_size], 5)
		pygame.draw.line(screen, cross_color,
						 [row * table_size, (col + 1) * table_size],
						 [(row + 1) * table_size, col * table_size], 5)

	def __draw_circle(self, row, col):
		radius = table_size / 2
		pygame.draw.circle(screen, circle_color,
						   [row * table_size + radius, col * table_size + radius], radius)

	def __has_line(self, symbol):
		wins = [
			(0, 1, 2), (3, 4, 5), (6, 7, 8),
			(0, 3, 6), (1, 4, 7), (2, 5, 8),
			(0, 4, 8), (2, 4, 6),
		]

		# Check if any of these triples are all the same symbol
		return any(self.table[a] == self.table[b] == self.table[c] == symbol for a, b, c in wins)

	def __process_mouse_click(self, event):
		if event.type != pygame.MOUSEBUTTONDOWN or not self.my_turn: return

		x, y = pygame.mouse.get_pos()

		print(f"Mouse click {x, y}")

		row = y // table_size
		col = x // table_size
		pos = row * 3 + col

		# Skip already filled cells
		if self.table[pos] != '-': return

		# Register move locally
		self.table[pos] = self.player
		self.my_turn = False

		# Send move to opponent
		self.client.publish(f'tick-tack-toe-{'O' if self.player == 'X' else 'X'}' , str(pos))

	def main(self):
		screen.fill(background_color)

		while self.running:
			self.__draw_table()

			status = self.__check_game_status()

			if status:
				text_surface = font.render(status, True, (0, 0, 0))
				text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
				screen.blit(text_surface, text_rect)

			for event in pygame.event.get():
				if event.type == pygame.QUIT: self.running = False

				if self.my_turn: self.__process_mouse_click(event)

			pygame.display.flip()
			self.FPS.tick(60)

	def on_receive(self, data: str):
		pos = int(data.split(' ', 2)[1])
		print(f"Received pos {pos}")

		if self.table[pos] != '-': return

		self.table[pos] = 'X' if self.player == 'O' else 'O'
		self.my_turn = True

	def __check_game_status(self):
		winner = None
		if self.__has_line('X'): winner = 'X'
		elif self.__has_line('O'): winner = 'O'

		if winner:
			if winner == self.player: return 'win'
			else: return 'loose'
		elif '-' not in self.table: return 'draw'
		return None
