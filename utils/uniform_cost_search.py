from collections import defaultdict
from priority_queue import priority_queue

class Search:
    def __init__(self,roadmap):
        self.roadmap = roadmap
        self.g = {}
        self.parents = {}
        for key in self.roadmap.vertices_dict.keys():
            self.g[key] = float("inf")
            self.parents[key] = -1

    def perform_search(self):
        self.g[0] = 0 # Since 0 is the start state
        closed_list = []
        pq = priority_queue()
        pq.insert(self.roadmap.vertices_dict[0][0],self.roadmap.vertices_dict[0][1],self.g[0],0)

        while not pq.isEmpty():
            temp = pq.pop()

            if [temp.x,temp.y] == self.roadmap.vertices_dict[1]:
                final_path, final_path_idx = [list(reversed(item)) for item in self.get_final_path()]
                return final_path, final_path_idx, self.g[1]

            closed_list.append([temp.x,temp.y])

            successors = self.roadmap.adjacency_dict[temp.idx]
        
            for node_idx in successors:
                if self.roadmap.vertices_dict[node_idx] not in closed_list:
                    xTemp = self.roadmap.vertices_dict[node_idx][0]
                    yTemp = self.roadmap.vertices_dict[node_idx][1]

                    heapIndex = pq.elementInHeap(xTemp,yTemp)

                    distance_index = self.roadmap.adjacency_dict[temp.idx].index(node_idx)

                    gTemp = self.g[temp.idx] + self.roadmap.edge_weights[temp.idx][distance_index] 
                    if gTemp < self.g[node_idx]:
                        self.parents[node_idx] = temp.idx
                        self.g[node_idx] = gTemp

                    if heapIndex != -1:
                        pq.remove(heapIndex)

                    pq.insert(xTemp, yTemp,self.g[node_idx],node_idx)

        return None

    def get_final_path(self):
        final_path = [self.roadmap.vertices_dict[1]]
        final_path_idx = [1]
        while True:
            idx = final_path_idx[-1]
            previous_node = self.parents[idx]
            if previous_node == 0:
                final_path.append(self.roadmap.vertices_dict[previous_node])
                final_path_idx.append(previous_node)
                break
            final_path.append(self.roadmap.vertices_dict[previous_node])
            final_path_idx.append(previous_node)
        return final_path, final_path_idx