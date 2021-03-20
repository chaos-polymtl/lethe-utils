// Define a variable

lc = 2.0e-1;
lf = 2.0e-1;
RO=1;
RI=0.25;

Point(0) = {0, 0, 0, lc};
Point(1) = {RO, 0, 0, lc};
Point(2) = {0, -RO , 0, lc};
Point(3) = {-RO, 0, 0, lc};
Point(4) = {0, RO, 0, lc};

Point(5) = {RI, 0, 0, lf};
Point(6) = {0, -RI , 0, lf};
Point(7) = {-RI, 0, 0, lf};
Point(8) = {0, RI, 0, lf};

Circle(1)={1,0,2};
Circle(2)={2,0,3};
Circle(3)={3,0,4};
Circle(4)={4,0,1};

Circle(5)={5,0,6};
Circle(6)={6,0,7};
Circle(7)={7,0,8};
Circle(8)={8,0,5};

Line Loop(1) = {1,2,3,4};
Line Loop(2) = {5,6,7,8};

Plane Surface(1) = {1,2} ;
//Transfinite Surface{1}={1,2,3,4};
Recombine Surface{1,2};

// Creates a physical entity 1 (i.e. for a BC)
//Physical Point(1) = {1,2} ;
Physical Line(0)={1,2,3,4};
Physical Line(1)={5,6,7,8};

Physical Surface(0) = {1};
