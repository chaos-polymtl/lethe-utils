// Define a variable

lc = 0.4;
L=1;

Point(0) = {-L,-L, 0, lc};
Point(1) = {L, -L, 0, lc};
Point(2) = {L, L , 0, lc};
Point(3) = {-L, L, 0, lc};

Line(0)={0,1};
Line(1)={1,2};
Line(2)={2,3};
Line(3)={3,0};

Line Loop(1) = {0,1,2,3};

Plane Surface(1) = {1} ;

Physical Surface(0) = {1};
Recombine Surface{1};

