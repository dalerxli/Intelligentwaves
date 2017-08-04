
class Square():
	''' class for mesh unit squares
		arguments may contain: cell index, edge index, edge relationship'''

	def __init__(self, void_list, row, col):
		''' parameter:
			void_list: list of shape for the mesh
			row: row number of the mesh
			col: col number of the mesh'''

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
		''' define index number of the square'''
		self.index = num 

	def set_edge(self, cell_to_edge):
		''' set the edges of this cell square'''
		self.edges = cell_to_edge
		self.e1 = self.edges[0]
		self.e2 = self.edges[1]
		self.e3 = self.edges[2]
		self.e4 = self.edges[3]

	def is_edge(self, edge_num):
		''' judge if it is the edge of the cell'''
		if self.edges != None:
			if edge_num in self.edges:
				return True 
			else:
				return False
		else:
			# print(self.edges)
			raise('Please run set_edge(cell_to_edge) fisrt')

class Mesh():

	def __init__(self, void_list, length, width):
		''' parameters:
			void_list: mesh in the representation of 2D array
			length: length of the mesh, unit: lambda
			width: width of the mesh, unit: lambda'''
		self.map = void_list
		self.length = length
		self.width = width

		self.num_cell_x = len(void_list)
		self.num_cell_y = len(void_list[0])
		self.unit_len_x = self.width / float(self.num_cell_x)
		self.unit_len_y = self.length / float(self.num_cell_y)
		self.num_node_x = 2 * self.num_cell_x + 1
		self.num_node_y = 2 * self.num_cell_y + 1

		self.__Ncel2indx, self.__Ncel2indy = self.__xyIndex()
		self.__square_list = self.__constructSquareList()

		# self.node_position_list = self.nodePosition()
		self.cell_to_node, self.num_nodes = self.cellToNodes()
		self.cell_to_edge, self.num_edges = self.cellToEdge()
		self.edge_to_cell = self.edgeToCell()


	def __constructSquareList(self):

		square_list = []
		cell_count = 1
		for row in range(self.num_cell_x):
			one_row = []
			for col in range(self.num_cell_y):
				cell_num = row*self.num_cell_y + col
				# construct a square
				unit = Square(self.map, row, col)
				# unit.set_edge(cell_to_edge[cell_num])
				# if a unit is a cell, index it
				if unit.is_filled:
					# print(cell_count)
					unit.set_cell_index(cell_count)
					cell_count += 1
				one_row.append(unit)
			square_list.append(one_row)
		# print(square_list)
		return square_list


	def cellToNodes(self):
		''' construct the cell_to_node list, i.e. pctnd'''

		# first find pctnd in whole plate
		num_squares = len(void_list) * len(void_list[0])

		cell_to_node = []
		y_base = 0
		for row in range(self.num_cell_x):
			for col in range(self.num_cell_y):
				set_of_nodes = [2*col+1, 2*col+2, 2*col+3,
								self.num_node_y+1+2*col, self.num_node_y+2+2*col, self.num_node_y+3+2*col,
								2*self.num_node_y+1+2*col, 2*self.num_node_y+2+2*col, 2*self.num_node_y+3+2*col]
				# conut y_zero
				set_of_nodes = [i + y_base for i in set_of_nodes]
				cell_to_node.append(set_of_nodes)
				print(set_of_nodes)
			y_base += 2*self.num_node_y

		# find out nodes for deleting
		node_to_delete = []

		for row in range(self.num_cell_x):
			for col in range(self.num_cell_y):
				cell_num = row*self.num_cell_y + col
				# print(cell_num)
				if self.__square_list[row][col].is_filled == 0:
					# void mesh, delete center node first
					node_to_delete.append(cell_to_node[cell_num][4])
					# detect edge elements
					if self.__square_list[row][col].left == 0:
						node_to_delete.append(cell_to_node[cell_num][1])
					if self.__square_list[row][col].right == 0:
						node_to_delete.append(cell_to_node[cell_num][7])
					if self.__square_list[row][col].up == 0:
						node_to_delete.append(cell_to_node[cell_num][5])
					if self.__square_list[row][col].down == 0:
						node_to_delete.append(cell_to_node[cell_num][3])
					# detect corner elements
					if self.__square_list[row][col].left == 0 and self.__square_list[row][col].down == 0:
						node_to_delete.append(cell_to_node[cell_num][0])
					if self.__square_list[row][col].right == 0 and self.__square_list[row][col].down == 0:
						node_to_delete.append(cell_to_node[cell_num][6])
					if self.__square_list[row][col].left == 0 and self.__square_list[row][col].up == 0:
						node_to_delete.append(cell_to_node[cell_num][2])
					if self.__square_list[row][col].right == 0 and self.__square_list[row][col].up == 0:
						node_to_delete.append(cell_to_node[cell_num][8])

		node_to_delete = list(set(node_to_delete)) # delete repeted elements
		node_to_delete.sort()	

		# calculate total node number
		num_nodes = self.num_node_x * self.num_node_y - len(node_to_delete)

		# cell_to_node list after deleting			
		truncate_cell_to_node = []

		for row in range(self.num_cell_x):
			for col in range(self.num_cell_y):
				cell_num = row*self.num_cell_y + col

				if self.map[row][col] == 0:
					truncate_cell_to_node.append([0 for i in range(9)])
				else:
					unit = []
					for i in range(9):
						num_to_change = cell_to_node[cell_num][i] 
						num_less_than_n2c = len([j for j in node_to_delete if j < num_to_change])
						# print(num_to_change, num_less_than_n2c)
						unit.append(num_to_change - num_less_than_n2c)
					truncate_cell_to_node.append(unit)
		
		cell_to_node_full = cell_to_node
		cell_to_node = truncate_cell_to_node
		# print(cell_to_node)
		return cell_to_node, num_nodes

	def __xyIndex(self):
		''' inner function: change index reference for compatible with matlab code'''
		countx = 0
		county = 0
		Ncel2indx = []
		Ncel2indy = []
		for xcell in range(self.num_cell_x):
			countx += 1
			for ycell in range(self.num_cell_y):
				county += 1
				Ncel2indx.append(countx)
				Ncel2indy.append(county)
				if county >= self.num_cell_y:
					county = 0
		return Ncel2indx, Ncel2indy


	def cellToEdge(self):
		''' construct the cell_to_edge list, i.e. pcted'''

		# initialization, find pcted in whole plane
		cell_to_edge = [[0, 0, 0, 0] for i in range(self.num_cell_x * self.num_cell_y)]
		lastmax = 0
		for ncell in range(self.num_cell_x * self.num_cell_y):
			if self.__Ncel2indx[ncell] == 1:
				if self.__Ncel2indy[ncell] == 1:
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
			elif self.__Ncel2indx[ncell] > 1:
				if self.__Ncel2indy[ncell] == 1:
					cell_to_edge[ncell][0] = lastmax+1
					cell_to_edge[ncell][1] = lastmax+2
					cell_to_edge[ncell][2] = lastmax+3
					cell_to_edge[ncell][3] = cell_to_edge[ncell-self.num_cell_y][1]
					lastmax = cell_to_edge[ncell][2]
				else:
					cell_to_edge[ncell][0] = lastmax
					cell_to_edge[ncell][1] = lastmax+1
					cell_to_edge[ncell][2] = lastmax+2
					cell_to_edge[ncell][3] = cell_to_edge[ncell-self.num_cell_y][1]
					lastmax = cell_to_edge[ncell][2]
			else:
				raise('error')

		# find deleted edges
		edge_to_delete = []

		for row in range(self.num_cell_x):
			for col in range(self.num_cell_y):
				cell_num = row*self.num_cell_y + col
				if self.__square_list[row][col].is_filled == 0:
					if self.__square_list[row][col].left == 0:
						edge_to_delete.append(cell_to_edge[cell_num][3])
					if self.__square_list[row][col].right == 0:
						edge_to_delete.append(cell_to_edge[cell_num][1])
					if self.__square_list[row][col].up == 0:
						edge_to_delete.append(cell_to_edge[cell_num][2])
					if self.__square_list[row][col].down == 0:
						edge_to_delete.append(cell_to_edge[cell_num][0])
		edge_to_delete = list(set(edge_to_delete))
		edge_to_delete.sort()

		# compute total edge
		num_edge = self.num_cell_x * (self.num_cell_y + 1) + \
				   self.num_cell_y * (self.num_cell_x + 1) - len(edge_to_delete)

		# delete edges
		truncate_cell_to_edge = []
		for row in range(self.num_cell_x):
			for col in range(self.num_cell_y):
				cell_num = row*self.num_cell_y + col

				if self.map[row][col] == 0:
					truncate_cell_to_edge.append([0 for i in range(4)])
				else:
					unit = []
					for i in range(4):
						num_to_change = cell_to_edge[cell_num][i] 
						num_less_than_n2c = len([j for j in edge_to_delete if j < num_to_change])
						# print(num_to_change, num_less_than_n2c)
						unit.append(num_to_change - num_less_than_n2c)
					truncate_cell_to_edge.append(unit)

		cell_to_edge_full = cell_to_edge
		cell_to_edge = truncate_cell_to_edge
		# print(cell_to_edge)

		return cell_to_edge, num_edge

	def edgeToCell(self):
		''' construct the edge_to_cell list, i.e. petcd'''

		# first compute the whole plane
		num_dummy_edge = self.num_cell_x * (self.num_cell_y + 1) + \
						 self.num_cell_y * (self.num_cell_x + 1) 

		edge_to_cell = []
		for ncell in range(self.num_cell_x * self.num_cell_y):
			print(ncell)
			if self.__Ncel2indx[ncell] == 1:
				if self.__Ncel2indy[ncell] == 1:
					edge_to_cell.append([ncell, -1])
				if self.__Ncel2indx[ncell]+1 <= self.num_cell_x:
					edge_to_cell.append([ncell, ncell+3])
				else:
					edge_to_cell.append([ncell, -1])
				if self.__Ncel2indy[ncell]+1 <= self.num_cell_y:
					edge_to_cell.append([ncell, ncell+1])
				else:
					edge_to_cell.append([ncell, -1])
				if self.__Ncel2indx[ncell]-1 > 0:
					edge_to_cell.append([ncell, ncell-3])
				else:
					edge_to_cell.append([ncell, -1])

			elif self.__Ncel2indx[ncell] > 1:
				if self.__Ncel2indy[ncell] == 1:
					edge_to_cell.append([ncell, -1])
				if self.__Ncel2indx[ncell]+1 <= self.num_cell_x:
					edge_to_cell.append([ncell, ncell+3])
				else:
					edge_to_cell.append([ncell, -1])
				if self.__Ncel2indy[ncell]+1 <= self.num_cell_y:
					edge_to_cell.append([ncell, ncell+1])
				else:
					edge_to_cell.append([ncell, -1])

		# start index from 1
		for pair in edge_to_cell:
			pair[0] += 1
			if pair[1] != -1:
				pair[1] += 1

		# add edge information to each square cell
		cell_count = 1
		for row in range(self.num_cell_x):
			# one_row = []
			for col in range(self.num_cell_y):
				cell_num = row*self.num_cell_y + col
				# unit = squares(void_list, row, col)
				self.__square_list[row][col].set_edge(self.cell_to_edge[cell_num])
				if self.__square_list[row][col].is_filled:
					print(cell_count)
					self.__square_list[row][col].set_cell_index(cell_count)
					cell_count += 1

		# search each edge and judge if it is the edge to some cell, add the cell to the edge_dict dictionary
		edge_dict = {}
		print(self.__square_list[0][1].edges) 
		print(self.num_edges)
		for edge in range(1, self.num_edges + 1):
			for row in range(self.num_cell_x):
				for col in range(self.num_cell_y):
					cell_num = row*self.num_cell_y + col
					# print(square)
					if self.__square_list[row][col].is_edge(edge):
						print('!!!')
						if edge not in edge_dict.keys():
							edge_dict[edge] = [self.__square_list[row][col].index]
						else:
							edge_dict[edge].append(self.__square_list[row][col].index)

		# append -1 to those with only one value, to be compatible with matlab code
		for value in edge_dict.values():
			if len(value) == 1:
				value.append(-1)

		# change to list representation
		truncate_edge_to_cell = []
		for edge in range(1, self.num_edges + 1):
			truncate_edge_to_cell.append(edge_dict[edge])
		print(truncate_edge_to_cell)

		# rename for clarity
		edge_to_cell_full = edge_to_cell
		edge_to_cell = truncate_edge_to_cell

		return edge_to_cell


	def nodePosition(self):
		# first generate nodes cords with whole square:

		node_position = []
		for row in range(2*self.num_cell_x+1):
			for col in range(2*self.num_cell_y+1):
				x_cord = -self.width/2.0 + row* self.unit_len_x/2.0
				y_cord = -self.length/2.0 + col* self.unit_len_y/2.0
				node_position.append((x_cord, y_cord, 0.0))

		# then detect and delete void squares
		print(node_position)
				
		return node_position
				
	def printMesh(self):
		''' print the mesh in the terminal'''

		for row in range(self.num_cell_x-1, -1, -1):
			print('')
			for col in range(self.num_cell_y):
				# print(row, col)
				if void_list[row][col] == 1:
					print('+'),
				else:
					print('-'),

if __name__ == "__main__":
	void_list = [[0,1,1], [1,0,0], [1,1,1]]
	mesh = Mesh(void_list, 1, 1)
	mesh.printMesh()


