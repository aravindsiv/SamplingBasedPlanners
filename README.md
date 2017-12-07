# SamplingBasedPlanners
The following algorithms have been implemented for a simple 2D navigation task with polygonal obstacles

* Probabilistic Roadmap (PRM)
* Rapidly-exploring Random Trees (RRT)

Usage:
```
python main.py [-h] [-in IN] [-algo ALGO] [-out OUT] [-n N] [-k K]
               [-plot PLOT]

arguments:
  -h, --help  show this help message and exit
  -in IN      input file (default: input.txt)
  -algo ALGO  algorithm to implement: prm, rrt (default: prm)
  -out OUT    output file (default: output.txt)
  -n N        number of samples for PRM/RRT (default: 1000)
  -k K        number of nearest neighbors for PRM (default: 5)
  -plot PLOT  plot final output? y/n (default: y)
```

A sample input file has been provided in ```input.txt```. The first lines of the input file are the dimensions of the map. The following lines are the co-ordinates of the vertices of the different polygonal obstacles present in the map.

A sample output is present in ```output.txt```. The first line is a dictionary of the various vertices in the final roadmap. The second line is the shortest path found, with the notation _(i,j)_ representing an edge from vertex _i_ to vertex _j_.