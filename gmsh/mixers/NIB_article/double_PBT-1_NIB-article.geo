//
SetFactory("OpenCASCADE");

// -------------------------------------------
// Dimensionless geometry variables
// -------------------------------------------
// All notations are defined accordingly to the article:
// "A parallel and adaptative Nitsche immersed boundary method to simulate viscous mixing" (Joachim, Daunais, Bibeau, Heltai, Blais)

//tank geometry
Dt = 0.365;
H = Dt*1;
//NB: origin = center of liquid cylinder
//-> the liquid is between -H/2:+H/2 and -T/2:T/2

//impeller geometry
Di = Dt/3;
Ci = Dt/4;
Hi = -H/2+Ci;

//blade geometry
theta = Pi/4;
Wi = Di/5;
Ti = Wi/10;
H_blade = Wi*Sin(theta);

//shaft and hub geometry
Ds = Wi*Cos(theta);
Dh = Ds*1.4;
Hh = H_blade*1;

//impeller's offset with tank center of revolution
//hard coded to avoid rounding errors in the center of rotation location
//corresponds to 3*Di/8
imp_offset = 0.045625; 

//minimum number of elements on the blade thickness
p_solid = 0.5;
//NB : number of particles = 2-3 * number of nodes

// -------------------------------------------
// Mesh
// -------------------------------------------
// In GMSH : Tools > Options... > Mesh > General, Tick Recombine all triangular meshes and select Subdivision algorithm "All Quad"

Mesh.CharacteristicLengthMin = Ti/p_solid;
Mesh.CharacteristicLengthMax = Ti/p_solid;
Mesh.ElementOrder = 1;
Mesh.SecondOrderLinear = 0;
Mesh.HighOrderOptimize = 1;

// -------------------------------------------
// Cylinder (pbt shaft) 
// -------------------------------------------
Cylinder(2) = {Hi, 0, 0, 			H-Ci, 0, 0, 		Ds/2,	2*Pi}; 
// 		xcenter, ycenter, ycenter, 	xaxis, yaxis, zaxis,	radius,	angular opening

// -------------------------------------------
// Cylinder (pbt hub)
// -------------------------------------------
Cylinder(3) = {Hi, 0, 0, Hh, 0, 0, Dh/2, 2*Pi};

// -------------------------------------------
// Blades
// -------------------------------------------
// Blade 1
Box (4) = {Hi, -Ti/2, 0, H_blade, Ti, Di/2 };
Rotate {{ 0,0,1 }, {Hi+H_blade/2, 0, 0}, theta } {Volume{4};}

// Other blades
Rotate {{ 1,0,0 }, {Hi+H_blade/2, 0, 0}, Pi/2 } {Duplicata{Volume{4};}}
Rotate {{ 1,0,0 }, {Hi+H_blade/2, 0, 0}, 2*Pi/2 } {Duplicata{Volume{4};}}
Rotate {{ 1,0,0 }, {Hi+H_blade/2, 0, 0}, 3*Pi/2 } {Duplicata{Volume{4};}}

// -------------------------------------------
// Global object
// -------------------------------------------
BooleanUnion {Volume{2}; Delete;} {Volume{3:7}; Delete;}

//Transformations
Translate {0, 0, imp_offset} {Volume{1};}
//Rotate {{1, 0, 0}, {0, 0, 0}, Pi/4} {Volume{1};}
//Translate {0, 0, -imp_offset} {Volume{1};}

//tank (for verification)
//Cylinder(20) = {-H/2, 0, 0, H, 0, 0, T/2, 2*Pi};

//Recombine Surface{1:100}; //uncomment for quad mesh
Physical Surface("0") = {0:100};
Physical Volume(0) = {1};

