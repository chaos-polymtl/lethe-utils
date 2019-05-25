// Define a variable

H=1;
L=10;
nl=50;
nh=10;

Point(1) = {0, 0, 0};
Point(2) = {L, 0, 0};
Point(3) = {L, H, 0};
Point(4) = {0, H, 0};

Line(1)={1,2};
Line(2)={2,3};
Line(3)={4,3};
Line(4)={1,4};
Transfinite Line {1,3} = Ceil(nl) Using Progression 1;
Transfinite Line {2,4} = Ceil(nh) Using Progression 1;
Line Loop(1) = {1,2,-3,-4};
Plane Surface(1) = {1} ;



Transfinite Surface {1};
Physical Surface(0) = {1};
Physical Line(0)={4};
Physical Line(1)={2};
Physical Line(2)={1,3};
Recombine Surface{1};

