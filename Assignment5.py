# Jeffrey Lipnick

import sys # use for file input
import random # use for neighboring solution generation
import operator # use for neighboring solution generation
import math
import copy

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
		#print "Tie: " + str(Tie)

class District():
	def __init__(self, number):
		self.number = number
		self.vertices = {}

	def addVertex(self, position, node):
		#check if value already exists
		if position not in self.vertices:
			self.vertices[position] = node

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

# def initialSolution(matrix):
# 	s = Solution()
# 	n = len(matrix)
# 	i = 0
# 	while (i < n):
# 		d = District(i)
# 		s.districts.insert(i, d)
# 		i += 1	
# 	j = 0
# 	while (j < n):
# 		for node in matrix[j]:
# 			node.district = j
# 			position = str(node.row) + str(node.column)
# 			s.districts[j].addVertex(position, node)
# 		j += 1
# 	return s

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
		#print "Connected Solution"
		return True
	else:
		#print "Not Connected Solution"
		return False

def DFS(node):
	if (node.visited == True):
		return
	else:
		node.visited = True
		for pos, adj in node.adjacent.iteritems():
			if (adj.district == node.district):
				DFS(adj)

def neighboringSolution(solution):
	complete = False
	while not complete:
		sp = copy.deepcopy(solution)
		length = len(sp.districts) - 1 # randint is inclusive
		districtNum = random.randint(0, length)
		district1 = sp.districts[districtNum]

		node = random.choice(district1.vertices.values())
		#print "Node (" + str(node.row) + "," + str(node.column) + ") randomly chosen from district " + str(district1.number)
		adj = None
		for key, value in node.adjacent.iteritems():
			if (value.district != node.district):
				adj = value
				break
		if (adj != None):
			#print "Adjacent Node (" + str(adj.row) + "," + str(adj.column) + ") selected from district " + str(adj.district)
			district2Number = adj.district
			adj.district = node.district
			adjPosition = str(adj.row) + str(adj.column)
			district2 = sp.districts[district2Number]
			district1.vertices[adjPosition] = adj
			#print "Adjacent Node (" + str(adj.row) + "," + str(adj.column) + ") added to district " + str(adj.district)
			district2.vertices.pop(adjPosition, None)
			#print "Adjacent Node (" + str(adj.row) + "," + str(adj.column) + ") removed from district " + str(district2Number)

			found = False
			grabbed = None
			j = 0
			while not found and (j < 9):
				option = random.choice(district2.vertices.values())
				#print "option chosen"
				i = 0
				for key, value in option.adjacent.iteritems():
					#print "for loop"
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
				#print "Node (" + str(grabbed.row) + "," + str(grabbed.column) + ") grabbed"
				position2 = str(grabbed.row) + str(grabbed.column)
				grabbed.district = district2Number
				#print "Grabbed's district set to: " + str(district2Number)
				district2.vertices[position2] = grabbed
				district1.vertices.pop(position2, None)

				validA = validSolution(district1)
				validB = validSolution(district2)

				if (validA and validB):
					complete = True
	return sp

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
				#print "Better solution found"
				s = sp
			else:
				p = math.exp( (-deltaE - 1) / (k*T) )
				#print "Probabilty: " + str(p)
				if (random.random() < p):
					#print "Worse solution accepted by probability"
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
	print "Algorithm applied: SA"
	print "*************************************\n"

	print "*************************************"
	print "Number of search states explored: " + str(s.searchStates)
	print "*************************************\n"

	# Print out ending districts
	# fmatrix = []
	# for district in s.districts:
	# 	for key, node in district.vertices.iteritems():
	# 		fmatrix.append(node)
	# i = 0
	# while (i < 8):
	# 	j = 0
	# 	while (j < 8):
	# 		pos = str(i) + str(j)
	# 		for item in fmatrix:
	# 			itemPos = str(item.row) + str(item.column)
	# 			if (itemPos == pos):
	# 				print str(item.district) + " ",
	# 				break
	# 		if (j == 7):
	# 			print ""
	# 		j += 1
	# 	i += 1

if __name__ == '__main__':
    main()