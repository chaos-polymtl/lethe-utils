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

theta = Pi/4;

d = W*Cos(theta);
r = d/2;
h = W*Sin(theta);

E = 0.1*W;
td = E*Cos(Pi/2-theta);
th = E*Sin(Pi/2-theta);

// -------------------------------------------
// Mesh
// -------------------------------------------
Mesh.CharacteristicLengthMin = 0.01;
Mesh.CharacteristicLengthMax = 0.1;
Mesh.ElementOrder = 1;
Mesh.SecondOrderLinear = 1;
Mesh.HighOrderOptimize = 1;
Mesh.SubdivisionAlgorithm = 2; // Hexas

// -------------------------------------------
// Cylinder (pbt)
// -------------------------------------------
Cylinder(1) = {0, 0, C, 0, 0, h+th, W/2, 2*Pi};

// -------------------------------------------
// Blade 1 and 3
// -------------------------------------------
Point(3) = {0, r, C};		Point(4) = {0, -r, C+h};
Point(5) = {D/2, r, C+h};	Point(6) = {-D/2, -r, C+h};
Point(7) = {0, -r, C};		Point(8) = {0, r, C+h};
Point(9) = {D/2, -r, C};	Point(10) = {-D/2, r, C};

Line(4) = {4, 6};
Line(5) = {6, 10};
Line(6) = {10, 3};
Line(7) = {3, 4};
Line(8) = {5, 8};
Line(9) = {8, 7};
Line(10) = {7, 9};
Line(11) = {9, 5};

Extrude {0, -td, th} {
  Curve{8}; Curve{11}; Curve{10}; Curve{9}; 
}
Extrude {0, td, th} {
  Curve{4}; Curve{5}; Curve{6}; Curve{7}; 
}

// -------------------------------------------
// Blade 2 and 4
// -------------------------------------------
Point(19) = {r, 0, C};		Point(20) = {-r, 0, C+h};
Point(21) = {r, D/2, C};	Point(22) = {-r, -D/2, C};
Point(23) = {-r, 0, C};	Point(24) = {r, 0, C+h};
Point(25) = {-r, D/2, C+h};	Point(26) = {r, -D/2, C+h};

Line(28) = {24, 26};
Line(29) = {26, 22};
Line(30) = {22, 23};
Line(31) = {23, 24};
Line(32) = {25, 20};
Line(33) = {20, 19};
Line(34) = {19, 21};
Line(35) = {21, 25};

Extrude {td, 0, th} {
  Curve{32}; Curve{35}; Curve{34}; Curve{33}; 
}
Extrude {-td, 0, th} {
  Curve{30}; Curve{29}; Curve{28}; Curve{31}; 
}

// -------------------------------------------
// Surfaces
// -------------------------------------------
Curve Loop(20) = {22, 24, 26, 27};
Plane Surface(20) = {20};
Curve Loop(21) = {6, 7, 4, 5};
Plane Surface(21) = {21};
Curve Loop(22) = {38, 43, 42, 40};
Plane Surface(22) = {22};
Curve Loop(23) = {34, 35, 32, 33};
Plane Surface(23) = {23};
Curve Loop(24) = {18, 16, 14, 19};
Plane Surface(24) = {24};
Curve Loop(25) = {10, 11, 8, 9};
Plane Surface(25) = {25};
Curve Loop(26) = {28, 29, 30, 31};
Plane Surface(26) = {26};
Curve Loop(27) = {46, 51, 50, 48};
Plane Surface(27) = {27};

// -------------------------------------------
// Volumes
// -------------------------------------------
Surface Loop(2) = {27, 16, 17, 18, 19, 26};
Volume(2) = {2};
Surface Loop(3) = {24, 6, 7, 4, 5, 25};
Volume(3) = {3};
Surface Loop(4) = {12, 13, 14, 15, 22, 23};
Volume(4) = {4};
Surface Loop(5) = {21, 10, 9, 8, 11, 20};
Volume(5) = {5};

BooleanUnion{ Volume{1}; Delete; }{ Volume{4}; Volume{5}; Volume{2}; Volume{3}; Delete; }

// -------------------------------------------
// Cylinder (shaft)
// -------------------------------------------
bottom = -H+C+h+th;
Cylinder(2) = {0, 0, H, 0, 0, bottom, W/2, 2*Pi};

// -------------------------------------------
// Cylinder (tank)
// -------------------------------------------
Cylinder(3) = {0, 0, 0, 0, 0, H, T/2, 2*Pi};

// -------------------------------------------
// Volume (fluid)
// -------------------------------------------
BooleanDifference{ Volume{3}; Delete; }{ Volume{2}; Volume{1}; Delete; }

// -------------------------------------------
// Boundary conditions
// -------------------------------------------
// Tank :
Physical Surface(1) = {46}; // Wall
Physical Surface(2) = {47}; // Top
Physical Surface(3) = {48}; // Bottom

// Shaft :
Physical Surface(4) = {49};

// PBT :
Physical Surface(5) = {32, 23, 35, 24, 34, 25, 33, 42, 38, 43, 45, 39, 37, 50, 40, 36, 41, 44, 30, 29, 21, 27, 22, 28, 20};

Physical Volume(6) = {3};
