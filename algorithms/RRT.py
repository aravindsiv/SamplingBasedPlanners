from utils.configuration_space import Roadmap
from utils.graph_utils import *
from collections import defaultdict
from utils.uniform_cost_search import Search
import random
import math
import sys
import matplotlib.pyplot as plt 

'''Reference: http://msl.cs.illinois.edu/~lavalle/sub/rrt.py'''

class RRT:
	def __init__(self,cspace,num_samples,epsilon=7.0):
		self.cspace = cspace
		self.num_samples = num_samples
		self.roadmap = Roadmap()
		self.epsilon = epsilon

		self.polygon_edges = []

		for polygon in cspace.polygons:
		    for i in range(len(polygon)):
		        self.polygon_edges.append([polygon[i%len(polygon)],polygon[(i+1)%len(polygon)]])

	def steer(self,pt1,pt2):
		if distance(pt1,pt2) < self.epsilon:
			return pt2
		else:
			theta = math.atan2(pt2[1]-pt1[1],pt2[0]-pt1[0])
			return round(pt1[0] + self.epsilon*math.cos(theta),2), round(pt1[1] + self.epsilon*math.sin(theta),2)

	def perform_sampling(self,showPlot=True):
		self.roadmap.vertices_dict[0] = list(self.cspace.start_state)

		i = 0

		self.cspace.plot_config_space(False)

		while i < self.num_samples:
			sample = True

			x = float(random.randint(self.cspace.boundary[0][0],self.cspace.boundary[1][0]))
			y = float(random.randint(self.cspace.boundary[0][1],self.cspace.boundary[2][1]))

			nn = self.roadmap.vertices_dict[0]
			nn_key = 0

			for key in self.roadmap.vertices_dict.keys():
				node = self.roadmap.vertices_dict[key]
				if distance(node,[x,y]) < distance(nn,[x,y]):
					nn = node
					nn_key = key

			new_node = self.steer(nn,[x,y])

			for polygon in self.cspace.polygons:
			    if inside_polygon(new_node[0],new_node[1],polygon) or on_polygon(new_node[0],new_node[1],polygon):
			        sample = False

			for edge in self.polygon_edges:
				if line_intersection(edge,[nn,new_node]) is not None:
					sample = False
					continue

			if sample is True and new_node not in self.roadmap.vertices_dict.values():
				i += 1

				self.roadmap.vertices_dict[i+1] = new_node
				self.roadmap.adjacency_dict[nn_key].append(i+1)
				self.roadmap.edge_weights[nn_key].append(distance(new_node,nn))

				plt.plot([new_node[0],nn[0]],[new_node[1],nn[1]],color='black')

		# And now...the goal node!
		nn = self.roadmap.vertices_dict[0]
		nn_key = 0
		dist = float('inf')

		for key in self.roadmap.vertices_dict.keys():
			node = self.roadmap.vertices_dict[key]
			if distance(node,self.cspace.goal_state) < distance(nn,self.cspace.goal_state):
				nn = node
				nn_key = key
				dist = distance(node,self.cspace.goal_state)

		self.roadmap.vertices_dict[1] = list(self.cspace.goal_state)
		self.roadmap.adjacency_dict[nn_key].append(1)
		self.roadmap.edge_weights[nn_key].append(dist)

		plt.plot([nn[0],self.cspace.goal_state[0]],[nn[1],self.cspace.goal_state[1]],color='black')

		if showPlot:
			plt.show()

	def search(self,showPlot=False):
		ucs = Search(self.roadmap)
		searchResult = ucs.perform_search()

		if searchResult is None:
			print "Path could not be found!"
			sys.exit()

		final_path, final_path_idx, path_cost = searchResult

		for i in range(1,len(final_path)):
		    plt.plot([elem[0] for elem in final_path[i-1:i+1]],[elem[1] for elem in final_path[i-1:i+1]],color='brown',lw=2)

		if showPlot:
			plt.show()

		return final_path, final_path_idx

if __name__ == "__main__":
	cspace = configuration_space("input.txt")
	rrt = RRT(cspace,1000)
	rrt.perform_sampling(False)
	rrt.search()
