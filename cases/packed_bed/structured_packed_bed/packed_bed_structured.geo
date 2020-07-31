SetFactory("OpenCASCADE"); 
Box(1) = {-0.1,-0.1,-0.1, 1.1,1.1,1.1};

// Creating the spheres
x0 = -0.05; y0 = -0.05; z0 = -0.05; r = 0.18; dx = 0.1666; n = 3;
x = x0; y = y0; z = z0;
For t In {1:n}
  x += dx ;
  For u In {1:n}
    y += dx ;
    For v In {1:n}
      z += dx ;

      Sphere(1 + (t-1)*n*n + (u-1)*n + v) = {x,y,z,r};
      Physical Volume((t-1)*n*n + (u-1)*n + v) = {1 + (t-1)*n*n + (u-1)*n + v};     
 
      z += dx;
    EndFor
    y += dx;
    z = z0;
  EndFor
  x += dx;
  y = y0;
EndFor

// Deleting the spheres from the geometry
BooleanDifference(n*n*n+2) = { Volume{1}; Delete; }{ Volume{2 : n*n*n+1}; Delete;};

Mesh.CharacteristicLengthMin = 0.0200;
Mesh.CharacteristicLengthMax = 0.100;

Mesh.ElementOrder = 1;
Mesh.SecondOrderLinear =1;
Mesh.HighOrderOptimize = 1;
Mesh.SubdivisionAlgorithm = 2;


Physical Volume(0) = {n*n*n+2};
Physical Surface(0) = {5}; // z = 0 
Physical Surface(1) = {1, 2, 4, 6}; // walls
Physical Surface(2) = {7:n*n*n+6}; //spheres
Physical Surface(3) = {3}; // z = h

