SetFactory("OpenCASCADE"); 

// Creating the spheres
{{spheres}}

Mesh.CharacteristicLengthMin = {{h_min}};
Mesh.CharacteristicLengthMax = {{h_max}};

Mesh.ElementOrder = 1;
Mesh.SecondOrderLinear = 1;
Mesh.HighOrderOptimize = 1;
Mesh.SubdivisionAlgorithm = 2;

Physical Volume(0) = {1 : {{ last_sphere_surface }} };

