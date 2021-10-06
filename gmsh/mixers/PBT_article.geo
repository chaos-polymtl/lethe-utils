//
SetFactory("OpenCASCADE");

// -------------------------------------------
// Dimensionless geometry variables
// -------------------------------------------

//tank geometry
T = 0.365;
ratioHT = 1;
H = T*ratioHT;
//NB: origin = center of liquid cylinder
//-> liquid between -H/2:+H/2 and -T/2:T/2

//impeller geometry
ratioTD = 3;
ratioTC = 4;
D = T/ratioTD;
C = T/ratioTC;
Himp = -H/2+C; 

//blade geometry
theta = Pi/4;
ratioDW = 5;
ratioWE = 10;
W = D/ratioDW;
E = W/ratioWE;
H_blade = W*Sin(theta);

//shaft and hub geometry
W_shaft = W*Cos(theta);
W_hub = W_shaft*1.4;
H_hub = H_blade*1;

//minimum number of elements on the blade width
Nelem = 2;//2;
//NB : number of particles = 2-3 * number of nodes

// -------------------------------------------
// Mesh
// -------------------------------------------
// In GMSH : Tools > Options... > Mesh > General, Tick Recombine all triangular meshes and select Subdivision algorithm "All Quad"

Mesh.CharacteristicLengthMin = E/Nelem;
Mesh.CharacteristicLengthMax = E/Nelem;
Mesh.ElementOrder = 1;
Mesh.SecondOrderLinear = 0;
Mesh.HighOrderOptimize = 1;

// -------------------------------------------
// Cylinder (pbt shaft) 
// -------------------------------------------
Cylinder(2) = {Himp, 0, 0, 			H-C, 0, 0, 		W_shaft/2, 	2*Pi}; 
// 		xcenter, ycenter, ycenter, 	xaxis, yaxis, zaxis,	radius, 	angular opening

// -------------------------------------------
// Cylinder (pbt hub)
// -------------------------------------------
Cylinder(3) = {Himp, 0, 0, H_hub, 0, 0, W_hub/2, 2*Pi};

// -------------------------------------------
// Blades
// -------------------------------------------
// Blade 1
Box (4) = {Himp, -E/2, 0, H_blade, E, D/2 };
Rotate {{ 0,0,1 }, {Himp+H_blade/2, 0, 0}, theta } {Volume{4};}

// Other blades
Rotate {{ 1,0,0 }, {Himp+H_blade/2, 0, 0}, Pi/2 } {Duplicata{Volume{4};}}
Rotate {{ 1,0,0 }, {Himp+H_blade/2, 0, 0}, 2*Pi/2 } {Duplicata{Volume{4};}}
Rotate {{ 1,0,0 }, {Himp+H_blade/2, 0, 0}, 3*Pi/2 } {Duplicata{Volume{4};}}

// -------------------------------------------
// Global object
// -------------------------------------------
BooleanUnion {Volume{2}; Delete;} {Volume{3:7}; Delete;}
//Recombine Surface{1:100}; //uncomment for quad mesh
Physical Surface("0") = {0:22};
Physical Volume(0) = {1};


