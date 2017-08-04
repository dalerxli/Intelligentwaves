
class squares():

	def __init__(self, void_list, row, col):
		self.map = void_list
		self.map_xlength = len(self.map)
		self.map_ylength = len(self.map[0])
		self.is_filled = void_list[row][col]
		if row == 0:
			self.left = 0
		else:
			self.left = void_list[row-1][col]
		if row == self.map_xlength-1:
			self.right = 0
		else:
			self.right = void_list[row+1][col]
		if col == 0:
			self.down = 0
		else:
			self.down = void_list[row][col-1]
		if col == self.map_ylength-1:
			self.up = 0
		else:
			self.up = void_list[row][col+1]
		self.edges = None
		self.index = None

	def set_cell_index(self, num):
		self.index = num 

	def get_cell_index(self):
		return self.index

	def set_edge(self, cell_to_edge):
		self.edges = cell_to_edge
		self.e1 = self.edges[0]
		self.e2 = self.edges[1]
		self.e3 = self.edges[2]
		self.e4 = self.edges[3]

	def is_edge(self, edge_num):
		if self.edges != None:
			if edge_num in self.edges:
				return True 
			else:
				return False
		else:
			# print(self.edges)
			raise('Please run set_edge(cell_to_edge) fisrt')





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
	for row in range(x_sqrs):
		for col in range(y_sqrs):
			set_of_nodes = [2*col+1, 2*col+2, 2*col+3,
							y_nodes+1+2*col, y_nodes+2+2*col, y_nodes+3+2*col,
							2*y_nodes+1+2*col, 2*y_nodes+2+2*col, 2*y_nodes+3+2*col]
			# conut y_zero
			set_of_nodes = [i + y_zero for i in set_of_nodes]
			cell_to_node.append(set_of_nodes)
			print(set_of_nodes)
		y_zero += 2*y_nodes

	# create squares() to manipulate positions of mesh
	square_list = []
	for row in range(x_sqrs):
		one_row = []
		for col in range(y_sqrs):
			unit = squares(void_list, row, col)
			one_row.append(unit)
		square_list.append(one_row)
	# print(square_list)


	node_to_delete = []

	for row in range(x_sqrs):
		for col in range(y_sqrs):
			cell_num = row*y_sqrs + col
			# print(cell_num)
			if square_list[row][col].is_filled == 0:
				# void mesh, delete center node first
				node_to_delete.append(cell_to_node[cell_num][4])
				# detect edge elements
				if square_list[row][col].left == 0:
					node_to_delete.append(cell_to_node[cell_num][1])
				if square_list[row][col].right == 0:
					node_to_delete.append(cell_to_node[cell_num][7])
				if square_list[row][col].up == 0:
					node_to_delete.append(cell_to_node[cell_num][5])
				if square_list[row][col].down == 0:
					node_to_delete.append(cell_to_node[cell_num][3])
				# detect corner elements
				if square_list[row][col].left == 0 and square_list[row][col].down == 0:
					node_to_delete.append(cell_to_node[cell_num][0])
				if square_list[row][col].right == 0 and square_list[row][col].down == 0:
					node_to_delete.append(cell_to_node[cell_num][6])
				if square_list[row][col].left == 0 and square_list[row][col].up == 0:
					node_to_delete.append(cell_to_node[cell_num][2])
				if square_list[row][col].right == 0 and square_list[row][col].up == 0:
					node_to_delete.append(cell_to_node[cell_num][8])

	node_to_delete = list(set(node_to_delete)) # delete repeted elements
	node_to_delete.sort()				
	# print(node_to_delete)
	# print(cell_to_node)
	truncate_cell_to_node = []

	for row in range(x_sqrs):
		for col in range(y_sqrs):
			cell_num = row*y_sqrs + col

			if void_list[row][col] == 0:
				truncate_cell_to_node.append([0 for i in range(9)])
			else:
				unit = []
				for i in range(9):
					num_to_change = cell_to_node[cell_num][i] 
					num_less_than_n2c = len([j for j in node_to_delete if j < num_to_change])
					# print(num_to_change, num_less_than_n2c)
					unit.append(num_to_change - num_less_than_n2c)
				truncate_cell_to_node.append(unit)
	print(truncate_cell_to_node)


	return cell_to_node, truncate_cell_to_node

def edgeToCell(void_list):
	x_sqrs = len(void_list)
	y_sqrs = len(void_list[0])
	num_dummy_edge = x_sqrs*(y_sqrs+1) + y_sqrs*(x_sqrs+1)

	countx = 0
	county = 0
	# Ncel2indx = [i+1 for i in range(x_sqrs)]
	# Ncel2indy = [i+1 for i in range(y_sqrs)]
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
	# print(Ncel2indx)

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
	_, cell_to_edge, tol_edge = cellToEdge(void_list)
	print(cell_to_edge)
	# create squares() to manipulate positions of mesh
	square_list = []
	cell_count = 1
	for row in range(x_sqrs):
		one_row = []
		for col in range(y_sqrs):
			cell_num = row*y_sqrs + col
			unit = squares(void_list, row, col)
			unit.set_edge(cell_to_edge[cell_num])
			if unit.is_filled:
				print(cell_count)
				unit.set_cell_index(cell_count)
				cell_count += 1
			one_row.append(unit)
		square_list.append(one_row)

	# edge_to_delete = []

	# for row in range(x_sqrs):
	# 	for col in range(y_sqrs):
	# 		cell_num = row*y_sqrs + col
	# 		if square_list[row][col].left == 0:
	# 			edge_to_delete.append()	

	# search for edge to
	edge_dict = {}
	print(square_list[0][1].edges) 
	print(tol_edge)
	for edge in range(1,tol_edge):
		for row in range(x_sqrs):
			for col in range(y_sqrs):
				cell_num = row*y_sqrs + col
				# print(square)
				if square_list[row][col].is_edge(edge):
					print('!!!')
					if edge not in edge_dict.keys():
						edge_dict[edge] = [square_list[row][col].index]
					else:
						edge_dict[edge].append(square_list[row][col].index)
	print(edge_dict)
	# append -1 to those with only one value
	for value in edge_dict.values():
		if len(value) == 1:
			value.append(-1)
	print(edge_dict)
	# change to list representation
	truncate_edge_to_cell = []
	for edge in range(1, tol_edge):
		truncate_edge_to_cell.append(edge_dict[edge])
	print(truncate_edge_to_cell)



	return edge_to_cell, truncate_edge_to_cell


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

	square_list = []
	for row in range(x_sqrs):
		one_row = []
		for col in range(y_sqrs):
			unit = squares(void_list, row, col)
			one_row.append(unit)
		square_list.append(one_row)

	edge_to_delete = []

	for row in range(x_sqrs):
		for col in range(y_sqrs):
			cell_num = row*y_sqrs + col
			if square_list[row][col].is_filled == 0:
				if square_list[row][col].left == 0:
					edge_to_delete.append(cell_to_edge[cell_num][3])
				if square_list[row][col].right == 0:
					edge_to_delete.append(cell_to_edge[cell_num][1])
				if square_list[row][col].up == 0:
					edge_to_delete.append(cell_to_edge[cell_num][2])
				if square_list[row][col].down == 0:
					edge_to_delete.append(cell_to_edge[cell_num][0])
				# print(cell_num)
	edge_to_delete = list(set(edge_to_delete))
	edge_to_delete.sort()

	truncate_cell_to_edge = []
	tol_edge = x_sqrs * (y_sqrs + 1) + y_sqrs * (x_sqrs + 1) - len(edge_to_delete)
	for row in range(x_sqrs):
		for col in range(y_sqrs):
			cell_num = row*y_sqrs + col

			if void_list[row][col] == 0:
				truncate_cell_to_edge.append([0 for i in range(4)])
			else:
				unit = []
				for i in range(4):
					num_to_change = cell_to_edge[cell_num][i] 
					num_less_than_n2c = len([j for j in edge_to_delete if j < num_to_change])
					# print(num_to_change, num_less_than_n2c)
					unit.append(num_to_change - num_less_than_n2c)
				truncate_cell_to_edge.append(unit)

	print(edge_to_delete)
	print(truncate_cell_to_edge)

	return cell_to_edge, truncate_cell_to_edge, tol_edge
	
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
	print(cellToNodes(void_list))
	edgeToCell(void_list)
	cellToEdge(void_list)
	sq = squares(void_list, 2, 2)
	print(sq.left, sq.right, sq.up, sq.down)