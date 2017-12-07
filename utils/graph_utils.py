'''
TODO:
1. Check if you can combine on_polygon and inside_polygon
2. Check if more efficient way of doing line_intersection
'''

def distance(pt1,pt2):
	'''Returns distance between two points.'''
	return ((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)**0.5

def line_intersection(line1, line2):
	'''Returns the point of intersection of two lines.'''
	xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
	ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])  # Typo was here

	def det(a, b):
		return a[0] * b[1] - a[1] * b[0]

	div = det(xdiff, ydiff)
	if div == 0:
		return None

	d = (det(*line1), det(*line2))
	x = det(d, xdiff) / div
	y = det(d, ydiff) / div
	poi = [x, y]

	# check if point falls between two points in line
	for l in [line1, line2]:
		p1 = l[0]
		p2 = l[1]

		if (abs((distance(p1, p2) - (distance(p1, poi) + distance(poi, p2)))) > 0.1):
			return None

	return x, y

def on_polygon(x,y,polygon):
	pair_vertices = zip(polygon,polygon[1:]+polygon[:1])
	for item in pair_vertices:
		if abs(distance(item[0],item[1]) - (distance(item[0],(x,y))+distance((x,y),item[1]))) < 0.1:
			return True
	return False

def inside_polygon(x,y,polygon):
	'''Check if a point (x,y) lies inside a polygon with given vertices.
	Using ideas derived from: http://paulbourke.net/geometry/polygonmesh/'''
	num_vertices = len(polygon)

	inside = False

	p1x,p1y = polygon[0]
	for i in range(num_vertices+1):
		p2x,p2y = polygon[i % num_vertices]
		if y > min(p1y,p2y):
			if y <= max(p1y,p2y):
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or x <= xinters:
						inside = not inside
		p1x,p1y = p2x,p2y

	return inside

if __name__ == "__main__":
	print line_intersection([[1,0],[0,1]],[[2,0],[0,2]])