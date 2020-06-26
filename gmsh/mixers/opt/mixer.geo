// MIXER GEOMETRY (merge)
// Valérie Bibeau, Polytechnique Montréal
// 2020

SetFactory("OpenCASCADE");

// -------------------------------------------
// Dimensionless geometry variables
// -------------------------------------------

T = 1;

ratioTD = 3;
  D = T/ratioTD;
ratioHT = 1;
  H = T*ratioHT;
ratioTC = 4;
  C = T/ratioTC;
ratioDW = 5;
  W = D/ratioDW;
ratioDW = 3;
  W_Hub = D/ratioDW;

theta = Pi/4;

d = W*Cos(theta);
r = d/2;
h = W*Sin(theta);

H_blade = D/6;
E = 0.1*W;

// -------------------------------------------
// Mesh
// -------------------------------------------
Mesh.CharacteristicLengthMin = 0.005;
Mesh.CharacteristicLengthMax = 0.04;
Mesh.ElementOrder = 1;
Mesh.SecondOrderLinear = 1;
Mesh.HighOrderOptimize = 1;
Mesh.SubdivisionAlgorithm = 2; // Hexas

// -------------------------------------------
// Cylinder (tank)
// -------------------------------------------
Cylinder(1) = {0, 0, 0, 0, 0, H, T/2, 2*Pi};

// -------------------------------------------
// Cylinder (pbt)
// -------------------------------------------
Cylinder(2) = {0, 0, C, 0, 0, H, W/2, 2*Pi};

// -------------------------------------------
// Cylinder (pbt hub)
// -------------------------------------------
Cylinder(3) = {0, 0, C, 0, 0, H_blade, W_Hub/2, 2*Pi};

// -------------------------------------------
// Blade 1
// -------------------------------------------
Box (4) = { 0, -E/2, C, D/2, E, H_blade };
Rotate {{ 1,0,0 }, {0, 0, C+H_blade/2}, -theta } {Volume{4};}

// -------------------------------------------
// Blade 2
// -------------------------------------------
Box (5) = { 0, -D/2, C, E, D/2, H_blade};
Rotate {{ 0,1,0 }, {0, 0, C+H_blade/2}, theta } {Volume{5};}

// -------------------------------------------
// Blade 3
// -------------------------------------------
Box (6) = { 0, 0, C, E, D/2, H_blade};
Rotate {{ 0,1,0 }, {0, 0, C+H_blade/2}, -theta } {Volume{6};}

// -------------------------------------------
// Blade 4
// -------------------------------------------
Box (7) = { 0, -E/2, C, -D/2, E, H_blade };
Rotate {{ 1,0,0 }, {0, 0, C+H_blade/2}, theta } {Volume{7};}

// -------------------------------------------
// Volume (fluid - shaft)
// -------------------------------------------
BooleanDifference{ Volume{1}; Delete; }{ Volume{2:7}; Delete; }

// -------------------------------------------
// Boundary conditions
// -------------------------------------------
Physical Surface(0) = {1:28,32:1000}; // Wall
Physical Surface(1) = {29}; // Wall
Physical Surface(2) = {30}; // Top
Physical Surface(3) = {31}; // Bottom

Physical Volume(0) = {1:100};

