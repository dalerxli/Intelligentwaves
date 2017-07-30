
class square():

	def __init__(self, num_ind, pos, neighbor):
		self.num_ind = num_ind
		self.pos = pos
		self.left = neighbor[0]
		self.right = neighbor[1]
		self.down = neighbor[2]
		self.up = neighbor[3]


def createMesh(void_list):
	pass

# def numOfNodes(void_list):
# 	for row in len(void_list):
# 		for col in len(void_list[0]):
# 			if 

def nodePosition(void_list, length, width):
	x_sqrs = len(void_list)
	y_sqrs = len(void_list[0])
	x_square = width / float(x_sqrs)
	y_square = length / float(y_sqrs)
	# first generate nodes cords with whole square:

	node_position = []
	for row in range(2*x_sqrs+1):
		for col in range(2*y_sqrs+1):
			x_cord = -length/2.0 + row*x_square/2.0
			y_cord = -length/2.0 + col*y_square/2.0
			node_position.append((x_cord, y_cord, 0.0))

	# then detect and delete void squares

			
	return node_position
			
	pass

def cellToNodes(void_list):
	# first find pctnd in whole plate
	num_squares = len(void_list) * len(void_list[0])
	x_sqrs = len(void_list)
	y_sqrs = len(void_list[0])	
	x_nodes = 2*x_sqrs+1
	y_nodes = 2*y_sqrs+1
	cell_to_node = []
	y_zero = 0
	for row in range(len(void_list)):
		for col in range(len(void_list[0])):
			print(row, col)
			set_of_nodes = [2*col+1, 2*col+2, 2*col+3,
							y_nodes+1+2*col, y_nodes+2+2*col, y_nodes+3+2*col,
							y_nodes+1+2*col, 2*y_nodes+2+2*col, 2*y_nodes+3+2*col]
			# conut y_zero
			set_of_nodes = [i + y_zero for i in set_of_nodes]
			cell_to_node.append(set_of_nodes)
			print(set_of_nodes)
		y_zero += 2*y_nodes


	return cell_to_node

def edgeToCell(void_list):
	x_sqrs = len(void_list)
	y_sqrs = len(void_list[0])
	num_dummy_edge = x_sqrs*(y_sqrs+1) + y_sqrs*(x_sqrs+1)

	countx = 0
	county = 0
	Ncel2indx = []
	Ncel2indy = []
	for xcell in range(x_sqrs):
		countx += 1
		for ycell in range(y_sqrs):
			county += 1
			Ncel2indx.append(countx)
			Ncel2indy.append(county)
			if county >= y_sqrs:
				county = 0
	print(Ncel2indx[0])

	edge_to_cell = []
	for ncell in range(x_sqrs*y_sqrs):
		print(ncell)
		if Ncel2indx[ncell] == 1:
			if Ncel2indy[ncell] == 1:
				edge_to_cell.append([ncell, -1])
			if Ncel2indx[ncell]+1 <= x_sqrs:
				edge_to_cell.append([ncell, ncell+3])
			else:
				edge_to_cell.append([ncell, -1])
			if Ncel2indy[ncell]+1 <= y_sqrs:
				edge_to_cell.append([ncell, ncell+1])
			else:
				edge_to_cell.append([ncell, -1])
			if Ncel2indx[ncell]-1 > 0:
				edge_to_cell.append([ncell, ncell-3])
			else:
				edge_to_cell.append([ncell, -1])

		elif Ncel2indx[ncell] > 1:
			if Ncel2indy[ncell] == 1:
				edge_to_cell.append([ncell, -1])
			if Ncel2indx[ncell]+1 <= x_sqrs:
				edge_to_cell.append([ncell, ncell+3])
			else:
				edge_to_cell.append([ncell, -1])
			if Ncel2indy[ncell]+1 <= y_sqrs:
				edge_to_cell.append([ncell, ncell+1])
			else:
				edge_to_cell.append([ncell, -1])

	# start index from 1
	for pair in edge_to_cell:
		pair[0] += 1
		if pair[1] != -1:
			pair[1] += 1

	print(edge_to_cell)
	return edge_to_cell

def cellToEdge(void_list):
	x_sqrs = len(void_list)
	y_sqrs = len(void_list[0])

	countx = 0
	county = 0
	Ncel2indx = []
	Ncel2indy = []
	for xcell in range(x_sqrs):
		countx += 1
		for ycell in range(y_sqrs):
			county += 1
			Ncel2indx.append(countx)
			Ncel2indy.append(county)
			if county >= y_sqrs:
				county = 0

	cell_to_edge = [[0, 0, 0, 0] for i in range(x_sqrs*y_sqrs)]
	lastmax = 0
	for ncell in range(x_sqrs*y_sqrs):
		if Ncel2indx[ncell] == 1:
			if Ncel2indy[ncell] == 1:
				cell_to_edge[ncell][0] = 1
				cell_to_edge[ncell][1] = 2
				cell_to_edge[ncell][2] = 3
				cell_to_edge[ncell][3] = 4
				lastmax = cell_to_edge[ncell][3]
			else:
				cell_to_edge[ncell][0] = cell_to_edge[ncell-1][2]
				cell_to_edge[ncell][1] = lastmax+1
				cell_to_edge[ncell][2] = lastmax+2
				cell_to_edge[ncell][3] = lastmax+3
				lastmax = cell_to_edge[ncell][3]
		elif Ncel2indx[ncell] > 1:
			if Ncel2indy[ncell] == 1:
				cell_to_edge[ncell][0] = lastmax+1
				cell_to_edge[ncell][1] = lastmax+2
				cell_to_edge[ncell][2] = lastmax+3
				cell_to_edge[ncell][3] = cell_to_edge[ncell-y_sqrs][1]
				lastmax = cell_to_edge[ncell][2]
			else:
				cell_to_edge[ncell][0] = lastmax
				cell_to_edge[ncell][1] = lastmax+1
				cell_to_edge[ncell][2] = lastmax+2
				cell_to_edge[ncell][3] = cell_to_edge[ncell-y_sqrs][1]
				lastmax = cell_to_edge[ncell][2]
		else:
			raise('error')
	print(cell_to_edge)
	pass

def printMesh(void_list):
	rows = len(void_list)
	print(rows)
	cols = len(void_list[0])
	for row in range(rows-1, -1, -1):
		print('')
		for col in range(cols):
			# print(row, col)
			if void_list[row][col] == 1:
				print('+'),
			else:
				print('-'),

if __name__ == '__main__':
	# void_list = [[0,1,1,1], [1,0,0,1], [1,1,1,1]]
	void_list = [[0,1,1], [1,0,0], [1,1,1]]

	printMesh(void_list)
	a = nodePosition(void_list, 3,3)
	print((a))
	cellToNodes(void_list)
	# edgeToCell(void_list)
	cellToEdge(void_list)