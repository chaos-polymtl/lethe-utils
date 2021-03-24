// Define a variable

H_1=1;
H_2=H_1+0.5;
L_1=1;
L_2=L_1+0.5;
L_3=L_1+3;
nl_1=5;
nl_2=10;
nl_3=20;
nh_1=10;
nh_2=5;


Point(1) = {0, 0, 0};
Point(2) = {L_1, 0, 0};
Point(3) = {L_1, H_1, 0};
Point(4) = {0, H_1, 0};
Point(5) = {L_1, H_2, 0};
Point(6) = {L_2, 0, 0};
Point(7) = {L_2, H_1, 0};
Point(8) = {L_2, H_2, 0};
Point(9) = {L_3, 0, 0};
Point(10) = {L_3, H_1, 0};



Line(1)={1,2};
Line(2)={2,3};
Line(3)={4,3};
Line(4)={1,4};

Line Loop(1) = {1,2,-3,-4};
Plane Surface(1) = {1} ;

Line(5)={2,6};
Line(6)={6,7};
Line(7)={3,7};
Line(8)={7,8};
Line(9)={8,5};
Line(10)={5,3};
Line(11)={6,9};
Line(12)={9,10};
Line(13)={10,7};

Transfinite Line {1,3} = Ceil(nl_1) Using Progression 1;
Transfinite Line {2,4,6,12} = Ceil(nh_1) Using Progression 1;
Transfinite Line {5,7,9} = Ceil(nl_2) Using Progression 1;
Transfinite Line {11,13} = Ceil(nl_3) Using Progression 1;
Transfinite Line {8,10} = Ceil(nh_2) Using Progression 1;


Line Loop(2) = {5,6,-7,-2};
Plane Surface(2) = {2} ;

Line Loop(3) = {7,8,9,10};
Plane Surface(3) = {3} ;

Line Loop(4) = {11,12,13,-6};
Plane Surface(4) = {4} ;


Transfinite Surface {1:4};







Recombine Surface{1:4};
Physical Surface(0) = {1:4};
Physical Line(0)={1,5,11,3,10,8,13};
Physical Line(1)={4};
Physical Line(2)={9};
Physical Line(3)={12};

