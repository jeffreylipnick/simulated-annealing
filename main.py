''' 
Jeffrey Lipnick
Simulated Annealing Project

This project is designed to find a "good" solution to a political redistricting problem that has a functionally infinite solution set.  The input is a small matrix of voters (8x8 or 10x10) that each have a specific political affiliaton.  The voters are passed in as a command line argument and an example of the format can be seen in the accompanying smallState.txt or largeState.txt files.  For the purposes of this project, a "good" solution constitutes creating districts with the following properties:

1. Similar numbers of voters for each political party per district.
2. 8 districts of 8 voters for an 8x8 input or 10 districts of 10 voters for a 10x10 input.
3. All the districts must be contiguous.

'''

import sys # use for file input
import random # use for neighboring solution generation
import operator # use for neighboring solution generation
import math
import copy

# Each voter is represented by a Node
class Node():
	def __init__(self, value, row, column):
		self.value = value
		self.row = row
		self.column = column
		self.district = None
		self.adjacent = {}
		self.visited = False

	def addAdjacent(self, position, node):
		if (position not in self.adjacent):
			self.adjacent[position] = node

	def printAdjacent(self):
		print "Node " + "(" + str(self.row) + "," + str(self.column) + "): ",
		first = True
		for key, node in self.adjacent.iteritems():
			if first:
				sys.stdout.write("(" + str(node.row) + "," + str(node.column) + ")") 
				first = False
			else:
				sys.stdout.write(", (" + str(node.row) + "," + str(node.column) + ")") 
		print ""

# each solution is represtented by a Solution object.  Each solution has a list of district objects.
class Solution():
	def __init__(self):
		self.districts = []
		self.searchStates = 0

	def printDistrictData(self):
		for item in self.districts:
			print "District " + str(item.number) + ": ",
			first = True
			for key, node in item.vertices.iteritems():
				if first:
					sys.stdout.write("(" + str(node.row) + "," + str(node.column) + ")") 
					first = False
				else:
					sys.stdout.write(", (" + str(node.row) + "," + str(node.column) + ")") 
			print ""

	def printPartyMajorities(self):
		RMajor = 0
		DMajor = 0
		Tie = 0
		for district in self.districts:
			R = 0
			D = 0
			for key, node in district.vertices.iteritems():
				if (node.value == "R"):
					R += 1
				elif (node.value == "D"):
					D += 1
			if (R > D):
				RMajor += 1
			elif (D > R):
				DMajor += 1
			elif (R == D):
				Tie += 1
		print "R: " + str(RMajor)
		print "D: " + str(DMajor)
		print "Tie: " + str(Tie)

# each district has a number and the voters are stored in a vertices dictionary.
class District():
	def __init__(self, number):
		self.number = number
		self.vertices = {}

	def addVertex(self, position, node):
		#check if value already exists
		if position not in self.vertices:
			self.vertices[position] = node

# When the voter matrix is read in, this function adds the adjacent nodes to the adjacent dictionary for every node. This is needed when testing solutions for contiguity by performing a depth-first search.
def addAdjacency(matrix):
	r1 = 0
	while (r1 < len(matrix)):
		c1 = 0
		while (c1 < len(matrix)):
			node = matrix[r1][c1]
			r0 = r1 - 1 # Row Top
			r2 = r1 + 1 # Row Bottom
			c0 = c1 - 1 # Column Left
			c2 = c1 + 1 # Column Right

			if (r0 != -1):
				if (c0 != -1):
					adj = matrix[r0][c0]
					adjPos = str(adj.row) + str(adj.column)
					node.addAdjacent(adjPos, adj)

				adj = matrix[r0][c1]
				adjPos = str(adj.row) + str(adj.column)
				node.addAdjacent(adjPos, adj)

				if (c2 != len(matrix)):
					adj = matrix[r0][c2]
					adjPos = str(adj.row) + str(adj.column)
					node.addAdjacent(adjPos, adj)

			if (c0 != -1):
				adj = matrix[r1][c0]
				adjPos = str(adj.row) + str(adj.column)
				node.addAdjacent(adjPos, adj)
			if (c2 != len(matrix)):
				adj = matrix[r1][c2]
				adjPos = str(adj.row) + str(adj.column)
				node.addAdjacent(adjPos, adj)

			if (r2 != len(matrix)):
				if (c0 != -1):
					adj = matrix[r2][c0]
					adjPos = str(adj.row) + str(adj.column)
					node.addAdjacent(adjPos, adj)

				adj = matrix[r2][c1]
				adjPos = str(adj.row) + str(adj.column)
				node.addAdjacent(adjPos, adj)

				if (c2 != len(matrix)):
					adj = matrix[r2][c2]
					adjPos = str(adj.row) + str(adj.column)
					node.addAdjacent(adjPos, adj)
			c1 += 1
		r1 += 1

# This function creates an initial solution before random solutions are generated.  This function could be improved by adding some randomiation into the inital soluton generation so that every solution set doesn't start with the same initial solution. 
def initialSolution(matrix):
	s = Solution()
	n = len(matrix)
	i = 0
	while (i < n):
		d = District(i)
		s.districts.insert(i, d)
		i += 1
	half = len(matrix) / 2	
	for i in range(0,2):
		for node in matrix[i]:
			if (node.column < half):
				node.district = 0
				position = str(node.row) + str(node.column)
				s.districts[0].addVertex(position, node)
			else:
				node.district = 1
				position = str(node.row) + str(node.column)
				s.districts[1].addVertex(position, node)
	for i in range(2,4):
		for node in matrix[i]:
			if (node.column < half):
				node.district = 2
				position = str(node.row) + str(node.column)
				s.districts[2].addVertex(position, node)
			else:
				node.district = 3
				position = str(node.row) + str(node.column)
				s.districts[3].addVertex(position, node)
	for i in range(4,6):
		for node in matrix[i]:
			if (node.column < half):
				node.district = 4
				position = str(node.row) + str(node.column)
				s.districts[4].addVertex(position, node)
			else:
				node.district = 5
				position = str(node.row) + str(node.column)
				s.districts[5].addVertex(position, node)
	for i in range(6,8):
		for node in matrix[i]:
			if (node.column < half):
				node.district = 6
				position = str(node.row) + str(node.column)
				s.districts[6].addVertex(position, node)
			else:
				node.district = 7
				position = str(node.row) + str(node.column)
				s.districts[7].addVertex(position, node)
	if (len(matrix) > 8):
		for i in range(8,10):
			for node in matrix[i]:
				if (node.column < half):
					node.district = 8
					position = str(node.row) + str(node.column)
					s.districts[8].addVertex(position, node)
				else:
					node.district = 9
					position = str(node.row) + str(node.column)
					s.districts[9].addVertex(position, node)
	return s

# This function checks for contiguity of districts to ensure a valid solution.  It utilizes a depth-first search to check for contiguity.
def validSolution(district):
	for item, value in district.vertices.iteritems():
		value.visited = False
	node = random.choice(district.vertices.values())
	DFS(node)
	connected = True
	for item, value in district.vertices.iteritems():
		if (value.visited != True):
			connected = False
	if (connected == True):
		return True
	else:
		return False

def DFS(node):
	if (node.visited == True):
		return
	else:
		node.visited = True
		for pos, adj in node.adjacent.iteritems():
			if (adj.district == node.district):
				DFS(adj)

# Generates a neighboring solution for use in the simulated annealing algorithm.
def neighboringSolution(solution):
	complete = False
	while not complete:
		sp = copy.deepcopy(solution)
		length = len(sp.districts) - 1 # randint is inclusive
		districtNum = random.randint(0, length)
		district1 = sp.districts[districtNum]

		node = random.choice(district1.vertices.values())
		adj = None
		for key, value in node.adjacent.iteritems():
			if (value.district != node.district):
				adj = value
				break
		if (adj != None):
			district2Number = adj.district
			adj.district = node.district
			adjPosition = str(adj.row) + str(adj.column)
			district2 = sp.districts[district2Number]
			district1.vertices[adjPosition] = adj
			district2.vertices.pop(adjPosition, None)

			found = False
			grabbed = None
			j = 0
			while not found and (j < 9):
				option = random.choice(district2.vertices.values())
				i = 0
				for key, value in option.adjacent.iteritems():
					if (i < 9): # prevents being stuck in infinte loop with no viable adjacent nodes
						if (value.district == node.district and value != adj):
							grabbed = value
							found = True
						else:
							i += 1
					else:
						break
				j += 1
			if (found == True):
				position2 = str(grabbed.row) + str(grabbed.column)
				grabbed.district = district2Number
				district2.vertices[position2] = grabbed
				district1.vertices.pop(position2, None)

				validA = validSolution(district1)
				validB = validSolution(district2)

				if (validA and validB):
					complete = True
	return sp

# Evaluates the fitness of a solution. The fitness here is defined as evenness between the number of voters in each political party for a district.
def fitness(s):
	f = 0.0
	counter = 0.0
	for district in s.districts:
		R = 0
		D = 0
		for key, node in district.vertices.iteritems():
			if (node.value == "R"):
				R += 1.0
			elif (node.value == "D"):
				D += 1.0
		f += math.fabs(R - D)
		counter += 1.0
	f = f / counter
	return f

def simulatedAnnealing(solution):
	# The number of search states can be adjusted by tweaking these initial parameters
	s = solution
	T = 1.0
	k = 50
	Tmin = 0.001
	alpha = 0.9
	while (T > Tmin):
		i = 0
		while (i < 10):
			sp = neighboringSolution(s)
			deltaE = fitness(sp) - fitness(s)
			if (deltaE < 0):
				s = sp
			else:
				p = math.exp( (-deltaE - 1) / (k*T) )
				if (random.random() < p):
					s = sp		
			s.searchStates += 1	
			i+=1
		T = T * alpha
	return s

def main():
	try:
		file = open(sys.argv[1], 'r')
	except:
		print('There was an error opening the file.')
		return

	rowNumber = 0
	matrix = []
	rCount = 0.0 # counter for number of "Rabbit" voters, use float so pecentage displays
	dCount = 0.0 # counter for number of "Dragon" voters, use float so percentage displays
	for line in file:
		columnNumber = 0
		line = line.rstrip() # remove newline character
		rowData = line.split(" ") # split row items into a list
		row = []
		for item in rowData:
			node = Node(rowData[columnNumber], rowNumber, columnNumber) # create a node for each item
			if (node.value == "R"):
				rCount += 1
			elif (node.value == "D"):
				dCount += 1
			row.insert(columnNumber, node) # insert the node into the row
			columnNumber += 1
		matrix.insert(rowNumber, row) # insert the row into the matrix
		rowNumber += 1

	addAdjacency(matrix)
	si = initialSolution(matrix)
	s = simulatedAnnealing(si)


	totalVoters = rCount + dCount
	percentR = rCount / totalVoters
	percentD = dCount / totalVoters
	print "Party division in population:"
	print "*************************************"
	print "R: %.2f" % percentR
	print "D: %.2f" % percentD
	print "*************************************\n"

	print "Number of districts with a majority for each party:"
	print "*************************************"
	s.printPartyMajorities()
	print "*************************************\n"

	print "Locations assigned to each district:"
	print "*************************************"
	s.printDistrictData()
	print "*************************************\n"

	print "*************************************"
	print "Number of search states explored: " + str(s.searchStates)
	print "*************************************\n"

	print "*************************************"
	print "Visualization of final districts:"
	print "*************************************\n"
	fmatrix = []
	for district in s.districts:
		for key, node in district.vertices.iteritems():
			fmatrix.append(node)
	if (len(fmatrix) == 64): # Print 8x8
		i = 0
		while (i < 8):
			j = 0
			while (j < 8):
				pos = str(i) + str(j)
				for item in fmatrix:
					itemPos = str(item.row) + str(item.column)
					if (itemPos == pos):
						print str(item.district) + " ",
						break
				if (j == 7):
					print ""
				j += 1
			i += 1
		print ""
	elif (len(fmatrix) == 100): # Print 10x10
		i = 0
		while (i < 10):
			j = 0
			while (j < 10):
				pos = str(i) + str(j)
				for item in fmatrix:
					itemPos = str(item.row) + str(item.column)
					if (itemPos == pos):
						print str(item.district) + " ",
						break
				if (j == 9):
					print ""
				j += 1
			i += 1
		print ""

if __name__ == '__main__':
    main()