// BLADES GEOMETRY
// Valérie Bibeau, Polytechnique Montréal
// 2020

SetFactory("OpenCASCADE");

// -------------------------------------------
// Dimensionless geometry variables
// -------------------------------------------

T = 2.000;

ratioTD = 3;
  D = T/ratioTD;
ratioHT = 1;
  H = T*ratioHT;
ratioTC = 4;
  C = T/ratioTC;
ratioDW = 5;
  W = D/ratioDW;
ratioDW = 10;
  W_Hub = D/ratioDW;

theta = Pi/4;

d = W*Cos(theta);
r = d/2;
h = W*Sin(theta);

H_blade = D/4;
E = 0.1*W;

// -------------------------------------------
// Mesh
// -------------------------------------------
Mesh.CharacteristicLengthMin = 0.020;
Mesh.CharacteristicLengthMax = 0.020;
Mesh.ElementOrder = 1;
Mesh.SecondOrderLinear = 1;
Mesh.HighOrderOptimize = 1;
Mesh.SubdivisionAlgorithm = 2; // quad

// -------------------------------------------
// Cylinder (pbt)
// -------------------------------------------
//Cylinder(2) = {0, 0, C, 0, 0, H-C, W/2, 2*Pi};
Cylinder(2) = {C-H/2, 0, 0, H-C, 0, 0, W/2, 2*Pi};

// -------------------------------------------
// Cylinder (pbt hub)
// -------------------------------------------
//Cylinder(3) = {0, 0, C, 0, 0, H_blade, W_Hub/2, 2*Pi};
Cylinder(3) = {C-H/2, 0, 0, H_blade, 0, 0, W_Hub/2, 2*Pi};

// -------------------------------------------
// Blade 1
// -------------------------------------------
//Box (4) = { 0, -E/2, C, D/2, E, H_blade };
Box (4) = { C-H/2, -E/2, 0, H_blade, E, D/2 };
//Rotate {{ 1,0,0 }, {0, 0, C+H_blade/2}, -theta } {Volume{4};}

// -------------------------------------------
// Blade 2
// -------------------------------------------
//Box (5) = { 0, -D/2, C, E, D/2, H_blade};
Box (5) = { C-H/2, -D/2, 0, H_blade, D/2, E};
//Rotate {{ 0,1,0 }, {0, 0, C+H_blade/2}, theta } {Volume{5};}

// -------------------------------------------
// Blade 3
// -------------------------------------------
//Box (6) = { 0, 0, C, E, D/2, H_blade};
Box (6) = { C-H/2, 0, 0,H_blade, D/2,E};
//Rotate {{ 0,1,0 }, {0, 0, C+H_blade/2}, -theta } {Volume{6};}

// -------------------------------------------
// Blade 4
// -------------------------------------------
//Box (7) = { 0, -E/2, C, -D/2, E, H_blade };
Box (7) = { C-H/2, -E/2, 0, H_blade, E, -D/2 };
//Rotate {{ 1,0,0 }, {0, 0, C+H_blade/2}, theta } {Volume{7};}

BooleanUnion {Volume{2}; Delete;}{Volume{3:7}; Delete;}

Physical Surface("0") = {0:22};
Physical Volume(0) = {1};

