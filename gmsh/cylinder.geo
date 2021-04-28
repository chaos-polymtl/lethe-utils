// Define a variable

lc = 5.0e-2;
RI=0.25;
mH=1;

Point(0) = {-mH, 0, 0, lc};
Point(1) = {-mH, RI, 0, lc};
Point(2) = {-mH, 0, -RI, lc};
Point(3) = {-mH,-RI, 0, lc};
Point(4) = {-mH,0, RI, lc};

Point(5) = {mH, RI, 0  , lc};
Point(6) = {mH, 0, -RI , lc};
Point(7) = {mH, -RI, 0 , lc};
Point(8) = {mH, 0, RI  , lc};
Point(9) = {mH, 0, 0   , lc};


Circle(1)={1,0,2};
Circle(2)={2,0,3};
Circle(3)={3,0,4};
Circle(4)={4,0,1};

Circle(5)={5,9,6};
Circle(6)={6,9,7};
Circle(7)={7,9,8};
Circle(8)={8,9,5};
//
Line(10)= {1,5};
Line(11)= {2,6};
Line(12)= {3,7};
Line(13)= {4,8};
//
//
//
Line Loop(1) = {1,11,-5,-10};
Line Loop(2) = {2,12,-6,-11};
Line Loop(3) = {3,13,-7,-12};
Line Loop(4) = {4,10,-8,-13};
//
Surface(1) = {1};//,3,4} ;
Surface(2) = {2};//,3,4} ;
Surface(3) = {3};//,3,4} ;
Surface(4) = {4};//,3,4} ;
////Plane Surface(2) = {2} ;
////Transfinite Surface{1}={1,2,3,4};
Recombine Surface{1:4};

// Creates a physical entity 1 (i.e. for a BC)
//Physical Point(1) = {1,2} ;
//Physical Line(0)={1,2,3,4};
//Physical Line(1)={5,6,7,8};

Physical Surface(0) = {1:4};
