// Define a variable

y0=-0.5;
y1=0;
y2=1.;
x0 =0.;
x1 = 5.;
x2 = 40.;

lc = 2.0e-1;
//lc = 1.0e-1;

Point(0) = {x0, y1, 0, lc};
Point(1) = {x0, y2, 0, lc};
Point(2) = {x1, y0, 0, lc};
Point(3) = {x1, y1, 0, lc};
Point(4) = {x2, y0, 0, lc};
Point(5) = {x2, y2, 0, lc};

Line(1) = {0,1};
Line(2) = {1,5};
Line(3) = {5,4};
Line(4) = {4,2};
Line(5) = {2,3};
Line(6) = {3,0};

Line Loop(1) = {1,2,3,4,5,6};

// Creates a physical entity 1 (i.e. for a BC)
//Physical Point(1) = {1,2} ;
Physical Line(0)={2,4,5,6};
Physical Line(1)={1};
Physical Line(2)={3};

Plane Surface(1) = {1};
Physical Surface(2) = {1};
Recombine Surface{1};

