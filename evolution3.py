import numpy as np
import random
import pygame
import time
import math

population = []
LARGENUMBER = 10000

pygame.init()
size = WIDTH, HEIGHT = 700,700
screen = pygame.display.set_mode(size)

ACTIONRANGE = 20
MOVEMENTSPEED = 1000
MOVEMENTCOST = 0.1
EXISTENCECOST = 1
MUTATIONMAXIMUM = 0.3
TRIGGER = 1
CORRECT_MOVEMENT = 0
INCORRECT_MOVEMENT = 0
POPULATION_SIZE = 30
FOOD_MAXIUM = 75000

class Organism(object):

	# Attributes of Nearest Neighbor
	distNX = 0
	distNY = 0
	Nfood = 0
	Nindex = 0

	# CONSTRUCTOR: Each organismm has an xy position and four matrices: movement movementTrigger, action, actionTrigger that determine movement
	"""
		moveLoc is a 1 x 2 matrix
			[distNX, distNY]
		[a] [distNX, distNY]
		[b] [distNX, distNY]

		movFood is a 2 x 1 matrix
				[a    , b    ]
		[food ] [food , food ]
		[Nfood] [Nfood, Nfood]

		Then the resultant matrixes mulitply:
						[distNX, distNY]
						[distNX, distNY]
		[food , food ]  [XSfood, YSfood]
		[Nfood, Nfood]  [XNfood, YNfood]

		Acted on by movCombined:
		[a, b]          [XSfoodXNFood, YSfoodYNFood]
		Which will be the factors that govern X movement based on food.
		             
		"""
	x = None
	y = None
	food = None
	movLoc = None
	movFood = None
	movCombined = None
	action = None

	def __init__(self, food, x, y, movLoc, movFood, movCombined):
	# Physical Attributes
		self.x = x
		self.y = y
		self.food = food
		# Genetic Attributes
		self.movLoc = np.array(movLoc).reshape(2,1)
		self.movFood = np.array(movFood).reshape(1,2)
		self.movCombined = np.array(movCombined).reshape(1,2)
		
	def live(self):
		self.detect()
		self.move()
		if self.food < 20:
			population.remove(self)
		elif self.food > FOOD_MAXIUM:
			self.food = FOOD_MAXIUM
		self.eat()
		self.render()

	# CONSIDER DELETING ALL THIS AND JUST TAKING DOWN THE INDEX OF THE NEIGHBOR.
	# Update the info on the nearest neighbor.
	def detect(self):
		# Sets info of first organism in the list
		nearestOrganism= [LARGENUMBER,LARGENUMBER,LARGENUMBER,LARGENUMBER]
		for i in range (len(population)):
			if population[i] != self:
				distX = self.x - population[i].x
				distY = self.y - population[i].y
				# Update if it is the least displacement
				if (distX**2 + distY**2 < nearestOrganism[0]**2 + nearestOrganism[1]**2):
					nearestOrganism[0] = distX
					nearestOrganism[1] = distY
					nearestOrganism[2] = population[i].food
					nearestOrganism[3] = i 

		self.distNX = nearestOrganism[0]
		self.distNY = nearestOrganism[1]
		self.Nfood  = nearestOrganism[2]
		self.Nindex = nearestOrganism[3]

	# Moves based on data of nearest organism via matrix multiplication
	def move(self):
		global CORRECT_MOVEMENT
		global INCORRECT_MOVEMENT

		tempD = np.array([self.distNX/WIDTH, self.distNY/HEIGHT]).reshape(1,2)
		tempF = np.array([self.food/(self.food+self.Nfood), self.Nfood/(self.food+self.Nfood)]).reshape(2,1)

		moveResult = None
		movResult = np.matmul(self.movCombined, np.matmul(np.matmul(tempF, self.movFood), np.matmul(self.movLoc, tempD)))[0]
		movMag = abs(movResult[0]) + abs(movResult[1])

		# Super sketchy, but the movemment vector magnitutes sum to 3:
		#self.food -= MOVEMENTCOST * movMag
		if (MOVEMENTSPEED*movMag*movResult[0] > 0):
			if (self.distNX > 0 and self.Nfood < self.food):
				CORRECT_MOVEMENT += 1
			else:
				INCORRECT_MOVEMENT += 1

		if (MOVEMENTSPEED*movMag*movResult[0] < 0):
			if (self.distNX < 0 and self.Nfood < self.food):
				CORRECT_MOVEMENT += 1
			else:
				INCORRECT_MOVEMENT += 1
				
		if (MOVEMENTSPEED*movMag*movResult[1] > 0):
			if (self.distNX > 0 and self.Nfood < self.food):
				CORRECT_MOVEMENT += 1
			else:
				INCORRECT_MOVEMENT += 1

		if (MOVEMENTSPEED*movMag*movResult[1] < 0):
			if (self.distNX < 0 and self.Nfood < self.food):
				CORRECT_MOVEMENT += 1
			else:
				INCORRECT_MOVEMENT += 1

		self.x += MOVEMENTSPEED * movMag * movResult[0]
		self.y += MOVEMENTSPEED * movMag * movResult[1]
		# Doesn't exceed the threshhold, stays still
		self.food -= EXISTENCECOST

	def eat(self):
		if (self.distNX**2+self.distNY**2 < ((math.log10(self.food) + math.log10(self.Nfood))*5)**2):
		# Successful predation (just a proprotion based on food levels) Literally eat or be eaten
			if random.uniform(0,1) < self.food**2 / (self.food**2 + self.Nfood**2):
				self.food += self.Nfood
				del population[self.Nindex]
			else:
				population[self.Nindex].food += self.food
				population.remove(self)
				del self

	def reproduce(self):

		self.food = self.food/2

		childMovLoc = [self.movLoc[0],self.movLoc[1]]
		childMovFood = [self.movFood[0][0], self.movFood[0][1]]
		childMovCombined =[self.movCombined[0][0],self.movCombined[0][1]]

		# Mutations 
		mutation = np.random.uniform(0, 2)
		if mutation == 0:
			childMovLoc[np.random.uniform(0, 1)] += random.uniform(0, MUTATIONMAXIMUM)
		
		if mutation == 1:
			childMovFood[np.random.uniform(0,1)] += random.uniform(0, MUTATIONMAXIMUM)
				
		if mutation == 2:
			childMovCombined[np.random.uniform(0, 1)] += random.uniform(0, MUTATIONMAXIMUM)


		#Give the child half of the food supply and create the child.
		population.append(Organism(np.random.uniform(500,1500), np.random.uniform(0,WIDTH),np.random.uniform(0,HEIGHT), childMovLoc, childMovFood, childMovCombined))
		#self.food /= 2 

	def render(self):
		if self.x > WIDTH:
			self.x = 0
		if self.x < 0:
			self.x = WIDTH
		if self.y > HEIGHT:
			self.y = 0
		if self.y < 0:
			self.y = HEIGHT
		pygame.draw.circle(screen,(0,255,0),(int(self.x), int(self.y)),int(5*math.log10(self.food)))
		pygame.display.flip()

# Initialize

def makeOrganism(f, x, y, m1, m2, m3):
	Org = Organism(f, x, y, m1, m2, m3)
	return Org
	
"""
def addOrganism():
	# Reproduction is random
	reproductionChance = round(np.random.uniform(0,1),3)

	# Calculate total food.
	totalFood = 0
	for org in range(populationSize):
		totalFood += population[org].food
"""


for c in range (0,POPULATION_SIZE):
	population.append(makeOrganism(
		np.random.uniform(1000,1500),
		np.random.uniform(0,WIDTH),
		np.random.uniform(0,HEIGHT),
		[np.random.uniform(-1,1),np.random.uniform(-1,1)],
		[np.random.uniform(-1,1),np.random.uniform(-1,1)], 
		[np.random.uniform(-1,1),np.random.uniform(-1,1)]))

displayRatioEvery = 500
displayCount = 0

while len(population) > 0:
# Graphics stuff
	pygame.event.pump()
	pygame.display.flip()
	screen.fill((0,0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

	for org in population:
		org.live()

	displayCount += 1

	if (displayCount >= displayRatioEvery):
		displayCount = 0

		totalFood = 0
		for org in range(len(population)):
			totalFood += population[org].food
		print ("AVERAGE FOOD: "+str(totalFood/len(population)))

		# Print the intelligence score of the generation.
		print("EXPECTED MOTION: "+str(CORRECT_MOVEMENT/(INCORRECT_MOVEMENT+CORRECT_MOVEMENT)))
		
		# Reset the values
		CORRECT_MOVEMENT = 0
		INCORRECT_MOVEMENT = 0

	while (len(population) < POPULATION_SIZE):

		# Calculate total food.
		totalFood = 0
		for org in range(len(population)):
			totalFood += population[org].food**2


		# Reproduction is random.
		reproductionChance = round(np.random.uniform(0,totalFood),3)

		# Determine which organism reproduces.
		counter = 0

		for org in range(len(population)):
			counter += population[org].food**2
			if (counter >= reproductionChance):
				population[org].reproduce()
				break


pygame.quit()