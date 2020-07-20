import pygame
import random

# MAIN CUBE OBJECT--------------------------------------------

class Cube(object):
	def __init__(self, iD, x, y, color):
		self.id = iD
		self.x = x
		self.y = y
		self.color = color 

	def draw(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, 19, 19))

# BAR OBJECT--------------------------------------------

class Bar(object):
	def __init__(self, iD, x, y, color):
		self.iD = iD
		self.x = x 
		self.y = y 
		self.color = color 
		self.body = []
		self.collided = False
		self.occupied = False
		self.orientation = "H"
		self.colorMatch = False

	def check_side_obstruction(self, side):
		global occupiedPositions
		if len(occupiedPositions) > 0:
			if side == "R":
				for cube in self.body:
					for position in occupiedPositions:
						if ((cube.y == position[1]) or (cube.y+20 == position[1])) and cube.x+20 == position[0]:
							return True
				return False 
			elif side == "L":
				for cube in self.body:
					for position in occupiedPositions:
						if ((cube.y == position[1]) or (cube.y+20 == position[1])) and cube.x-20 == position[0]:
							return True
				return False 
		else:
			return False

		
	def change_orientation(self):
		global run
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN and not self.collided:
				if event.key == pygame.K_SPACE:
					if self.orientation == "H":
						self.body.clear()
						self.orientation = "V"
					elif self.orientation == "V":
						self.body.clear()
						self.orientation = "H"
				elif event.key == pygame.K_RIGHT:
					if self.check_side_obstruction("R") is False:
						if (self.orientation == "H" and self.x < 340) or (self.orientation == "V" and self.x < 360):
							self.x += 20
				elif event.key == pygame.K_LEFT:
					if self.check_side_obstruction("L") is False:
						if (self.orientation == "H" and self.x > 0) or (self.orientation == "V" and self.x+20 > 0):
							self.x -= 20
					

	def check_mount(self):
		global occupiedPositions
		if len(occupiedPositions) > 0:
			for position in occupiedPositions:
				for cube in self.body:
					if cube.x == position[0] and cube.y+20 == position[1]:
						if cube.color == position[3]:
							self.colorMatch = True 
						return True
			return False 
		else:
			return False 	



	def check_collision(self):
		for cube in self.body:
			if cube.y > 560 or self.check_mount():
				self.collided = True 
				break

	def draw(self):
		self.change_orientation()
		if self.orientation == "H":
			self.body = [Cube("b1", self.x, self.y, self.color), 
			Cube("b2", self.x+20, self.y, self.color), Cube("b3", self.x+40, self.y, self.color)]
			if self.body[2].x > 380 or self.body[0].x < 0:
				self.orientation = "V"
				self.draw()
		elif self.orientation == "V":
			self.body = [Cube("b1", self.x+20, self.y-20, self.color), 
			Cube("b2", self.x+20, self.y, self.color), Cube("b3", self.x+20, self.y+20, self.color)]
			if self.body[2].y > 580:
				self.orientation = "H"
				self.draw()
		for cube in self.body:
			cube.draw()

	def move(self):
		global occupiedPositions, brickPlaced
		self.draw()
		self.check_collision()
		if not self.collided:
			self.y += 20
		else:
			if not self.occupied:
				for cube in self.body:
					occupiedPositions.append([cube.x, cube.y, self.iD, self.color])  
				brickPlaced = True
				self.occupied = True

				# print(occupiedPositions)



# SQUARE OBJECT--------------------------------------------

class Square(object):
	def __init__(self, iD, x, y, color):
		self.iD = iD
		self.x = x 
		self.y = y
		self.color = color 
		self.occupied = False
		self.body = [Cube("s1", self.x, self.y, self.color), Cube("s2", self.x+20, self.y, self.color), 
		Cube("s3", self.x, self.y+20, self.color), Cube("s4", self.x+20, self.y+20, self.color)]
		self.collided = False 

	def check_side_obstruction(self, side):
		global occupiedPositions
		if len(occupiedPositions) > 0:
			if side == "R":
				for cube in self.body:
					for position in occupiedPositions:
						if ((cube.y == position[1]) or (cube.y+20 == position[1])) and cube.x+20 == position[0]:
							return True
				return False 
			elif side == "L":
				for cube in self.body:
					for position in occupiedPositions:
						if ((cube.y == position[1]) or (cube.y+20 == position[1])) and cube.x-20 == position[0]:
							return True
				return False 
		else:
			return False

	def change_orientation(self):
		global run
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN and not self.collided:
				if event.key == pygame.K_RIGHT and self.x < 360:
					if self.check_side_obstruction("R") is False:
						self.x += 20
				elif event.key == pygame.K_LEFT and self.x > 0:
					if self.check_side_obstruction("L") is False:
						self.x -= 20

	def check_mount(self):
		global occupiedPositions
		if len(occupiedPositions) > 0:
			for position in occupiedPositions:
				for cube in self.body:
					if cube.x == position[0] and cube.y+20 == position[1]:
						return True
			return False 
		else:
			return False 

	def check_collision(self):
		for cube in self.body:
			if cube.y > 560 or self.check_mount():
				self.collided = True 
				break

	def draw(self):
		self.change_orientation()
		self.body = [Cube("s1", self.x, self.y, self.color), Cube("s2", self.x+20, self.y, self.color), 
		Cube("s3", self.x, self.y+20, self.color), Cube("s4", self.x+20, self.y+20, self.color)]
		for cube in self.body:
			cube.draw()

	def move(self):
		global occupiedPositions, brickPlaced
		self.draw()
		self.check_collision()
		if not self.collided:
			self.y += 20
		else:
			if not self.occupied:
				for cube in self.body:
					occupiedPositions.append([cube.x, cube.y, self.iD])
				brickPlaced = True
				self.occupied = True
				# print(occupiedPositions)
				

# Initialize Game
pygame.init()
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("TETRIS")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (252, 173, 3)
PURPLE = (113, 50, 168)
colors = [WHITE, RED, BLUE, GREEN, ORANGE, PURPLE]

# Game Variables
barCount = 1
squareCount = 1
occupiedPositions = []
played_bricks = []
eliminateBodies = []
rows = [num for num in range(0, 600, 20)]
brickPlaced = False
initialPlay = True
rowEliminate = False
bricks = ["bar","square"]
run = True

def grid(surf):
	global WHITE
	y = 19
	x = 19
	for _ in range(29):
		pygame.draw.line(surf, WHITE, (0, y), (400, y))
		y += 20
	for _ in range(19):
		pygame.draw.line(surf, WHITE, (x, 0), (x, 600))
		x += 20

def layout(surf):
	global WHITE
	pygame.draw.line(surf, WHITE, (400, 0), (400, 600), 5)
	grid(surf)

def feed_bricks():
	global brickPlaced, barCount, squareCount, initialPlay, played_bricks, bricks, colors
	if initialPlay:
		played_bricks[-1].move()
	if brickPlaced:
		initialPlay = False
		brick = random.choice(bricks)
		if brick == "bar":
			played_bricks.append(Bar("B"+str(barCount), 180, 0, random.choice(colors)))
			barCount += 1
			brickPlaced = False
		elif brick == "square":
			played_bricks.append(Square("S"+str(squareCount), 180, 0, random.choice(colors)))
			squareCount += 1
			brickPlaced = False
	if not initialPlay:
		played_bricks[-1].move()

def draw_bricks():
	global rowEliminate
	if rowEliminate:
		eliminate_rows()
		rowEliminate = False
	for brick in played_bricks:
		if brick.occupied:
			brick.draw()

def eliminate_rows():
	global eliminateBodies, played_bricks, occupiedPositions, rowEliminate
	if rowEliminate:
		for position in eliminateBodies:
			for brick in played_bricks:
				if brick.iD == position[2]:
					for cube in brick.body:
						if cube.x == position[0] and cube.y == position[1]: 
							brick.body.pop(brick.body.index(cube))
							for position in occupiedPositions:
								for cube in brick.body:
									if cube.x == position[0] and cube.y == position[1]:
										occupiedPositions.pop(occupiedPositions.index(position))
										# brick.occupied = False
							# occupiedPositions.pop(occupiedPositions.index(position))
							if len(brick.body) == 0:
								del brick

							brick.check_collision()
							brick.move()				
		eliminateBodies.clear()


def check_row_elimination():
	global occupiedPositions, rows, eliminateBodies, rowEliminate
	if len(occupiedPositions) > 0:
		for row in rows:
			rowCount = 0
			if len(eliminateBodies) == 20:
				break
			for position in occupiedPositions:
				if position[1] == row:
					rowCount += 1
					if len(eliminateBodies) == 20:
						break
					if rowCount == 20:
						for position in occupiedPositions:
							if position[1] == row:
								eliminateBodies.append(position)
								if len(eliminateBodies) == 20:
									break
						rowEliminate = True
						print("A ROW HAS BEEN ELIMINATED")
						# print(eliminateBodies)   # FOR DEBUGGING PURPOSES
						break


def window_update(surf):
	global BLACK, initialPlay, brickPlaced
	surf.fill(BLACK)
	layout(win)
	feed_bricks()
	draw_bricks()
	check_row_elimination()
	pygame.display.update()

def main():
	global run, bricks, played_bricks, barCount, squareCount, colors
	first_brick = random.choice(bricks)
	if first_brick == "bar":
		played_bricks.append(Bar("B"+str(barCount), 180, 0, random.choice(colors)))
		barCount += 1
	elif first_brick == "square":
		played_bricks.append(Square("S"+str(squareCount), 180, 0, random.choice(colors)))
		squareCount += 1
	while run:
		clock.tick(5)
		window_update(win)

if __name__ == '__main__':
	main()