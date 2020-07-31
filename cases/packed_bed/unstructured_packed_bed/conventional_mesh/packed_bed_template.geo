SetFactory("OpenCASCADE"); 
Box(1) = { {{x0}}, {{y0}}, {{z0}}, {{dx}}, {{dy}}, {{dz}} };

// Creating the spheres
{{spheres}}

// Deleting the spheres from the geometry
BooleanDifference({{pb_index}}) = { Volume{1}; Delete; }{ Volume{2 : {{last_sphere_volume}}}; Delete;};

Mesh.CharacteristicLengthMin = {{h_min}};
Mesh.CharacteristicLengthMax = {{h_max}};

Mesh.ElementOrder = 1;
Mesh.SecondOrderLinear = 1;
Mesh.HighOrderOptimize = 1;
Mesh.SubdivisionAlgorithm = 2;

Physical Volume(0) = { {{pb_index}} };
Physical Surface(0) = {5}; // z = 0 
Physical Surface(1) = {1, 2, 4, 6}; // walls
Physical Surface(3) = {3}; // z = h
Physical Surface(2) = {7 : {{last_sphere_surface}}}; //spheres

