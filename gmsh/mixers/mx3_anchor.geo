// BLADES GEOMETRY
// Valérie Bibeau, Polytechnique Montréal
// 2020

SetFactory("OpenCASCADE");

// -------------------------------------------
// Dimensionless geometry variables
// -------------------------------------------

T = 2.000;

D = 0.7;
ratioHT = 1;
  H = T*ratioHT;
ratioTC = 4;
  C = T/ratioTC;
ratioTC_anchor = 16;
C_anchor = T/ratioTC_anchor;
D_anchor = 1;
W = 0.05;
W_Hub = 0.1;

theta = Pi/6;
theta_blade = Pi/8;
theta_blade_2 = Pi/2.5;
theta_blade_3 = Pi/16;



d = W*Cos(theta);
r = d/2;
h = W*Sin(theta);

H_blade = D/4;
E = 0.25*W;

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
Cylinder(2) = {C_anchor-H/2, 0, 0, H-C, 0, 0, W/2, 2*Pi};

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

Box (15) = { C-H/2, -E/2, 0, H_blade, E, D };
Rotate {{ 0,1,0 }, {0, 0, C+H_blade/2}, theta_blade } {Volume{15};}

Translate {0.00, 0.0,-0.175} {Volume{15};}
//BooleanDifference	{ Volume{4}; Delete;}{ Volume{15}; Delete;}

Box (14) = { C-H/2, -E/2, 0, H_blade, E, D/2 };
Rotate {{ 0,1,0 }, {0, 0, C+H_blade/2}, -theta_blade_2 } {Volume{14};}
Translate {-0.65, 0.0, -0.16} {Volume{14};}

Box (16) = { C-H/2, -E/2, 0, H_blade, E, D };
Rotate {{ 0,1,0 }, {0, 0, C+H_blade/2}, -theta_blade_3 } {Volume{16};}
Translate {0.11, 0.0, 0.} {Volume{16};}


BooleanDifference	{ Volume{4}; Delete;}{ Volume{14:16}; Delete;}
Rotate {{ 0,0,1 }, {-C+H_blade/2, 0, 0}, theta } {Volume{4};}
Translate {-H_blade/4, 0.0, 0.0} {Volume{4};}

Rotate {{ 1,0,0 }, {-C+H_blade/2, 0, 0}, 2*Pi/3 } {Duplicata{Volume{4};}}
Rotate {{ 1,0,0 }, {-C+H_blade/2, 0, 0}, 4*Pi/3 } {Duplicata{Volume{4};}}


// -------------------------------------------
// Cylinder (pbt hub)
// -------------------------------------------
//Cylinder(3) = {0, 0, C, 0, 0, H_blade, W_Hub/2, 2*Pi};
Cylinder(20) = {C_anchor-H/2, 0, 0, H_blade, 0, 0, W_Hub/2, 2*Pi};
Box (21) = { C_anchor-H/2, -E/2, -D_anchor/2, H_blade, E, D_anchor };



// -------------------------------------------
// Blade 2
// -------------------------------------------
//Box (5) = { 0, -D/2, C, E, D/2, H_blade};
//Box (5) = { C-H/2, -D/2, 0, H_blade, D/2, E};
//Rotate {{ 0,1,0 }, {0, 0, C+H_blade/2}, theta } {Volume{5};}

// -------------------------------------------
// Blade 3
// -------------------------------------------
//Box (6) = { 0, 0, C, E, D/2, H_blade};
//Box (6) = { C-H/2, 0, 0,H_blade, D/2,E};
//Rotate {{ 0,1,0 }, {0, 0, C+H_blade/2}, -theta } {Volume{6};}

// -------------------------------------------
// Blade 4
// -------------------------------------------
//Box (7) = { 0, -E/2, C, -D/2, E, H_blade };
//Box (7) = { C-H/2, -E/2, 0, H_blade, E, -D/2 };
//Rotate {{ 1,0,0 }, {0, 0, C+H_blade/2}, theta } {Volume{7};}

BooleanUnion {Volume{2}; Delete;}{Volume{3:6}; Delete;}

Physical Surface("0") = {0:22};
Physical Volume(0) = {1};

