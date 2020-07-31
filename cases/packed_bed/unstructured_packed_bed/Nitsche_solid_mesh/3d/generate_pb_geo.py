from jinja2 import Template
import numpy as np

geo_template = "solid_mesh_template.geo"

datafilename = "datafile.txt" #To be changed for the name of the file that contains the positions and radiuses of the spheres
geofilename = "solid.geo" #To be changed for the name of the .geo file you want to create

x,y,z,r = np.loadtxt(datafilename, skiprows=1, unpack=True)
buffer = 0.99 #Prevents from sphere surfaces to touch
r = buffer * r

#Dimensions of the box
x0 = -0.004; y0 = -0.004; z0 = 0; dx = 0.008; dy = 0.008; dz = 0.014 #(x0, y0, z0) represents a corner of the box, and (dx, dy, dz) represents the vector to reach the opposite corner. See Box() in gmsh

#Length of cells
h_min = 0.0002; h_max = 0.0003 # Minimal and maximal lengths of the tetrahedral cells

i = 0
spheres = ""
for row in x:
	spheres += 'Sphere(' + str(int(i+1)) + ') = {' + str(x[i]) + ', ' + str(y[i]) + ', ' + str(z[i]) + ', ' + str(r[i]) + '};\n'
	i += 1

f_template = open(geo_template, 'r')
geo_text = f_template.read()
template = Template(geo_text)
text = template.render(x0 = x0, y0 = y0, z0 = z0, dx = dx, dy = dy, dz = dz, spheres = spheres, pb_index = i+2, last_sphere_volume = i+1, last_sphere_surface = i, h_min = h_min, h_max = h_max)

with open(geofilename, 'a') as f_geo:
	f_geo.write(text)

