import argparse
import sys
from utils.configuration_space import configuration_space
from algorithms.PRM import PRM
from algorithms.RRT import RRT

def write_to_file(planner,path_idx,fname):
	last_key = planner.roadmap.vertices_dict.keys()[-1]
	with open(fname,'w+') as f:
		for key in planner.roadmap.vertices_dict.keys():
			if key != last_key:
				f.write(str(key)+": ("+str(planner.roadmap.vertices_dict[key][0])+","+str(planner.roadmap.vertices_dict[key][1])+"), ")
			else:
				f.write(str(key)+": ("+str(planner.roadmap.vertices_dict[key][0])+","+str(planner.roadmap.vertices_dict[key][1])+")")
		f.write("\n")
		for i in range(1,len(path_idx)):
			if i != len(path_idx)-1:
				f.write("("+str(path_idx[i-1])+","+str(path_idx[i])+"), ")
			else:
				f.write("("+str(path_idx[i-1])+","+str(path_idx[i])+")")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("-in",help="input file (default: input.txt)",default="input.txt")
	parser.add_argument("-algo",help="algorithm to implement: prm, rrt (default: prm)",default="prm")
	parser.add_argument("-out",help="output file (default: output.txt)",default="output.txt")

	# Optional arguments, only for PRM/RRT
	parser.add_argument("-n",help="number of samples for PRM/RRT (default: 1000)",default=1000)
	parser.add_argument("-k",help="number of nearest neighbors for PRM (default: 5)",default=5)
	parser.add_argument("-plot",help="plot final output? [y/n] (default: y)",default='y')

	args = vars(parser.parse_args())

	cspace = configuration_space(args['in'])

	if args['algo'] == 'prm':
		planner = PRM(cspace,args['n'])
		planner.perform_sampling(False)
		planner.get_knn(args['k'])
		path, path_idx = planner.search(args['plot']=='y')

	elif args['algo'] == 'rrt':
		planner = RRT(cspace,args['n'])
		planner.perform_sampling(False)
		path, path_idx = planner.search(args['plot']=='y')

	write_to_file(planner,path_idx,args['out'])
