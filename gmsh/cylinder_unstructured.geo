// Define a variable

y0=0;
y1=1;

x0 =0.;
x1 =10;

xc=1;
yc=0.5;
r=0.025;

lo = 5.0e-2;
lc = 1.0e-2;

Point(0) = {x0, y0, 0, lo};
Point(1) = {x0, y1, 0, lo};
Point(2) = {x1, y0, 0, lo};
Point(3) = {x1, y1, 0, lo};

Point(4) = {xc, yc, 0, lc};
Point(5) = {xc-r, yc, 0, lc};
Point(6) = {xc, yc+r, 0, lc};
Point(7) = {xc+r, yc, 0, lc};
Point(8) = {xc, yc-r, 0, lc};



Line(1) = {0,1};
Line(2) = {1,3};
Line(3) = {3,2};
Line(4) = {2,0};

Circle(5)={5,4,6};
Circle(6)={6,4,7};
Circle(7)={7,4,8};
Circle(8)={8,4,5};

Line Loop(1) = {1,2,3,4};
Line Loop(2) = {5,6,7,8};

// Creates a physical entity 1 (i.e. for a BC)
//Physical Point(1) = {1,2} ;
Physical Line(0)={5,6,7,8};
Physical Line(1)={1};
Physical Line(2)={2,4};
Physical Line(3)={3};

Plane Surface(1) = {1,2};
Physical Surface(2) = {1};
Recombine Surface{1};

