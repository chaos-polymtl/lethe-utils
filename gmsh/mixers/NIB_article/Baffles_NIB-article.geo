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

//baffle geometry
Cb = Ci/3; //off-bottom clearance (along z)
Wb = Dt/10; //width (along y)
Tb = Wb/3; //thickness (along z)
Sb = 19*Dt/20; //spacing to tank

//mesh refinement parameter
p_solid = 1;
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
// Baffles
// -------------------------------------------
Box (1) = {-H/2+Cb, -Sb/2, -Tb/2, H-Cb, Wb, Tb };
//tank (TMP)
//Cylinder(16) = {-H/2, 0, 0, H, 0, 0, T/2, 2*Pi};

// Other baffles
Rotate {{ 1,0,0 }, {0, 0, 0}, Pi/2 } {Duplicata{Volume{1};}}
//Rotate {{ 1,0,0 }, {0, 0, 0}, Pi/2 } {Volume{1};}
Rotate {{ 1,0,0 }, {0, 0, 0}, Pi } {Duplicata{Volume{1};}}
//Rotate {{ 1,0,0 }, {0, 0, 0}, Pi } {Volume{1};}
Rotate {{ 1,0,0 }, {0, 0, 0}, 3*Pi/2 } {Duplicata{Volume{1};}}
//Rotate {{ 1,0,0 }, {0, 0, 0}, 3*Pi/2 } {Volume{1};}

// -------------------------------------------
// Global object
// -------------------------------------------
//Recombine Surface{1:100}; //uncomment for quad mesh
Physical Surface("0") = {0:100};
Physical Volume(0) = {0:10};


