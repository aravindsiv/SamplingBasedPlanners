import ast
import matplotlib.pyplot as plt
from collections import defaultdict

class configuration_space:
    def __init__(self,FILE_NAME):
        self.polygons = []
        line_ctr = 0
        with open(FILE_NAME) as f:
            num_lines = sum(1 for l in f)
        with open(FILE_NAME) as f:
            for l in f:
                line_ctr += 1
                if line_ctr == 1:
                    self.boundary = list(ast.literal_eval(l))
                elif line_ctr in range(2,num_lines):
                    self.polygons.append(list(ast.literal_eval(l)))
                else:
                    temp = list(ast.literal_eval(l))
                    self.start_state = temp[0]
                    self.goal_state = temp[1]

    def plot_polygon(self,coords):
        for i in range(len(coords)):
            plt.plot(coords[i][0],coords[i][1],marker='o',color='black',markersize=0.5)
        plt.plot([elem[0] for elem in [coords[0],coords[-1]]],[elem[1] for elem in [coords[0],coords[-1]]],color='black')
        for i in range(1,len(coords)):
            plt.plot([elem[0] for elem in coords[i-1:i+1]],[elem[1] for elem in coords[i-1:i+1]],color='black')

    def plot_config_space(self,showPlot=True):
        axes = plt.gca()
        axes.set_xlim([self.boundary[0][0],self.boundary[1][0]])
        axes.set_ylim([self.boundary[0][1],self.boundary[2][1]])
        plt.plot(self.start_state[0],self.start_state[1],marker='o',color='red')
        plt.plot(self.goal_state[0],self.goal_state[1],marker='o',color='green')
        for i in range(len(self.polygons)):
            self.plot_polygon(self.polygons[i])
        if showPlot:
            plt.show()
            
class Roadmap:
    def __init__(self):
        self.vertices_dict = {}
        self.adjacency_dict = defaultdict(list)
        self.edge_weights = defaultdict(list)

if __name__ == "__main__":
	cspace = configuration_space("input.txt")
	cspace.plot_config_space()
