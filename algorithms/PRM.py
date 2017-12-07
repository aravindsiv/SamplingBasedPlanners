from utils.configuration_space import Roadmap
from utils.graph_utils import *
from collections import defaultdict
from utils.uniform_cost_search import Search
import random
import sys
import matplotlib.pyplot as plt 

class PRM:
    def __init__(self,cspace,num_samples):
        self.cspace = cspace
        self.num_samples = num_samples
        self.roadmap = Roadmap()

        self.polygon_edges = []
        for polygon in cspace.polygons:
            for i in range(len(polygon)):
                self.polygon_edges.append([polygon[i%len(polygon)],polygon[(i+1)%len(polygon)]])

    def perform_sampling(self,showPlot=True):
        self.roadmap.vertices_dict[0] = list(self.cspace.start_state)
        self.roadmap.vertices_dict[1] = list(self.cspace.goal_state)
        
        i = 0
        
        self.cspace.plot_config_space(False)
        
        while i < self.num_samples:
            sample = True
            x = float(random.randint(self.cspace.boundary[0][0],self.cspace.boundary[1][0]))
            y = float(random.randint(self.cspace.boundary[0][1],self.cspace.boundary[2][1]))
            for polygon in self.cspace.polygons:
                if inside_polygon(x,y,polygon) or on_polygon(x,y,polygon):
                    sample = False
            if sample:
                if [x,y] not in self.roadmap.vertices_dict.values():
                    i += 1
                    plt.plot(x,y,marker='o',color='black',markersize=1)
                    self.roadmap.vertices_dict[i+1] = [x,y]  
                    
        if showPlot:
            plt.show()

    def get_knn(self,k=5):
        distances = defaultdict(list)
        for i in self.roadmap.vertices_dict.keys():
            for j in self.roadmap.vertices_dict.keys():
                distances[i].append(distance(self.roadmap.vertices_dict[i],self.roadmap.vertices_dict[j]))
        
        for i in range(len(self.roadmap.vertices_dict.keys())):
            sorted_distances = sorted(distances[i])[1:k+1]
            dist_indices = [distances[i].index(item) for item in sorted_distances]
            for j,idx in enumerate(dist_indices):
                add_edge = True
                for edge in self.polygon_edges:
                    if line_intersection(edge,[self.roadmap.vertices_dict[i],self.roadmap.vertices_dict[idx]]) is not None:
                        add_edge = False
                        break
                if add_edge:
                    self.roadmap.adjacency_dict[i].append(idx)
                    # self.roadmap.adjacency_dict[].append(i)
                    self.roadmap.edge_weights[i].append(sorted_distances[j])
            
    def search(self,showPlot=False):
        ucs = Search(self.roadmap)
        searchResult = ucs.perform_search()

        if searchResult is None:
        	print "Path could not be found!"
        	sys.exit()

        final_path, final_path_idx, path_cost = searchResult

        for i in range(1,len(final_path)):
            plt.plot([elem[0] for elem in final_path[i-1:i+1]],[elem[1] for elem in final_path[i-1:i+1]],color='brown')

        if showPlot:
            plt.show()

        return final_path, final_path_idx