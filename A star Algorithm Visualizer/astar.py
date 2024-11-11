import pygame
import math
from queue import PriorityQueue

WIDTH = 500
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)#already looked at it
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255) #unvisited square
BLACK = (0, 0, 0)#barrier square
PURPLE = (128, 0, 128)#end
ORANGE = (255, 165 ,0)#start node
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)#end node

class Spot:#class for spots or cubes or nodes in our grid
	def __init__(self, row, col, width, total_rows):
		self.row = row#using all of these to avoid the global variables
		self.col = col
		self.x = row * width
		self.y = col * width#to keep actal track or coordinate in the plane
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):#updating the neighbours
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Down row from 0,1,2,3....
			self.neighbors.append(grid[self.row + 1][self.col])#then append the next row to that one

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Upwards rows
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #Rightside rows
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #Leftside rows
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other): #lt-->less than
		return False

#####Now let's create a heuristic function for performing the operation of A*
def h(p1, p2):#hfunction heuristic using manhattan distance
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)#abs --> abosolute distance


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):#Grid
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))#grids on the vertical lines
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))#grids on the vertical lines by shiffting the X axis


def draw(win, grid, rows, width):
	win.fill(WHITE)#fills the entiree screen with one color, do this at he beginning of every frame

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

##Now, we have to identify what mouse position have I clicked on
#create a function to track the mouse position in the window designed; eg to create a maze or some points etc
#to figure out wj=hich one of thespots to change color when clicked on them based on mouse position
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

#lets now define the main functon
def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:#at the beginning of the run if its true and in the while loop, lets look through all the events that are happening
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False#initially if we press esc button then, stop executing that is quit the process

			if pygame.mouse.get_pressed()[0]: #leftmost button
				pos = pygame.mouse.get_pos()#gives what position the mouse is at(x or y coordinates)
				row, col = get_clicked_pos(pos, ROWS, width)#what row and column is clicked on
				spot = grid[row][col]#index the row col
                #setting the start and the end position
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:#start and end cannot be one
					end = spot
					end.make_end()

				elif spot != end and spot != start:#not clicking start and not clicked on end then make yhat spot a barrier
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: #rightmost button
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:#restting the start and end
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN: 
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_COMMA:#clear the entire screen
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)