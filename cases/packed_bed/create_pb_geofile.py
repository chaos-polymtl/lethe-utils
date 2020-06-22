import pygmsh
import meshio
import csv

datafilename = 'data.txt'
geofilename = 'output.geo'

#Creation of the geometry
geom = pygmsh.built_in.Geometry()
with open (datafilename, 'r') as f:
	reader = csv.reader(f,delimiter=" ")
	next(reader)
	for row in reader:
		x = float(row[0])
		y = float(row[1])
		z = float(row[2])
		r = float(row[3])
		#Creation of spheres
		ballHole = geom.add_ball(x0=[x,y,z], radius=r, lcar=0.10, )

#Creation of the box - deleting the spheres from this box
x0 = -0.004
x1 = 0.004
y0 = -0.004
y1 = 0.004
z0 = 0
z1 = 0.01
geom.add_box(x0, x1, y0, y1, z0, z1, holes=[ballHole.surface_loop])

#Creation of the .geo file
mesh = pygmsh.generate_mesh(geom, geo_filename = geofilename)

#hmin, hmax, forcing hexs
h_min = 0.00008
h_max = 0.0008
with open(geofilename , 'a') as geo_file:
	geo_file.write("\n\nMesh.CharacteristicLengthMin = " + str(h_min) + ";\nMesh.CharacteristicLengthMax = " + str(h_max) + ";\nMesh.ElementOrder = 1;\nMesh.SecondOrderLinear = 1;\nMesh.HighOrderOptimize = 1;\nMesh.SubdivisionAlgorithm = 2;")

