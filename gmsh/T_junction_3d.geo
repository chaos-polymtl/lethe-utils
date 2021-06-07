// 3D junction geometry
// Bruno Blais, Polytechnique Montréal
// 2020

SetFactory("OpenCASCADE");

D_sc = 0.0254;
D_c = 0.300;

L_i=0.25;
L_o=2;
L_c = L_i+L_o + D_sc;

L_sc = 0.5;

// -------------------------------------------
// Mesh
// -------------------------------------------
Mesh.CharacteristicLengthMin = 0.001;
Mesh.CharacteristicLengthMax = 0.01;
Mesh.ElementOrder = 1;
//Mesh.SecondOrderLinear = 0;
//Mesh.HighOrderOptimize = 1;
//Mesh.SubdivisionAlgorithm = 2; // quad

// -------------------------------------------
// Cylinder (pbt)
// -------------------------------------------
Cylinder(1) = {0, 0, 0, L_c, 0, 0, D_c/2, 2*Pi};

// -------------------------------------------
// Cylinder (pbt hub)
// -------------------------------------------
Cylinder(2) = {L_i+D_c/2, L_sc, 0, 0, -L_sc, 0, D_sc/2, 2*Pi};


BooleanUnion {Volume{1}; Delete;}{Volume{2}; Delete;}

Physical Surface("0") = {1,4};
Physical Surface("1") = {2};
Physical Surface("2") = {5};
Physical Volume(0) = {1};