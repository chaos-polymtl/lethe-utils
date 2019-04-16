// Define a variable
lc = 1.25e-1;
lf = 1.25e-1;
RO=1;
RI=0.4;

Point(0) = {0, 0, 0, lc};
Point(1) = {RO, 0, 0, lc};
Point(4) = {0, RO, 0, lc};

Point(5) = {RI, 0, 0, lf};
Point(8) = {0, RI, 0, lf};

Line(1)={1,5};
Line(2)={8,4};
Circle(4)={4,0,1};
Circle(8)={8,0,5};


Line Loop(1) = {4,1,-8,2};

Plane Surface(1) = {1} ;
//Transfinite Surface{1}={1,2,3,4};

// Creates a physical entity 1 (i.e. for a BC)
//Physical Point(1) = {1,2} ;
Physical Line(0)={4};
Physical Line(1)={8};
Physical Line(2)={1,2};
//
Physical Surface(0) = {1};
Recombine Surface{1};
