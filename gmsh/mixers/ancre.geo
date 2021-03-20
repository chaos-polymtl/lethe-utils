//SetFactory("OpenCASCADE");
Mesh.CharacteristicLengthMin = 0.0001;
Mesh.CharacteristicLengthMax = 0.025;
//Geometry.NumSubEdges = 100; // nicer display of curve

//Cuve
rTank=0.1825;
hTank=0.365;

//Tige
rtige=0.0127;
htige=0.333;  //pas le choix pour le maillage detre dans le domaine

//Ancre
S=0.333;
Ti=0.0254;
Wb=0.0356;
L=0.22;
C=0.0456;
e=0.004;
//x=Tan(45)*(Wb);
x=0.023;

//Raffinement
l=0.0125; //pour le raffinement
l1=0.0125;

//l=0.05; //pour le raffinement
//l1=0.05;


//===========================================================================
//Ancre
//===========================================================================
Point (0) = {S/2-Wb,e/2,S,l1};
Point (1) = {S/2,e/2,S,l1};
Point (2) = {S/2-Wb,e/2,S-L,l1};
Point (3) = {S/2,e/2,S-L-x,l1};
//Point (4) = {0,e/2,C+Wb,l1};
Point (5) = {0,e/2,C,l1};
Point (6) = {-(S/2-Wb),e/2,S-L,l1};
Point (7) = {-S/2,e/2,S-L-x,l1};
Point (8) = {-(S/2-Wb),e/2,S,l1};
Point (9) = {-S/2,e/2,S,l1};
Point (10) = {0,e/2,S-L,l1};
Point (11) = {0,e/2,S-L-x,l1};

//Calcul ellipse
z=(S-L-C-Wb)*Sqrt(1-((Ti/2)/((S-2*Wb)/2))^2);//depuis le centre de l' ellipse
z2=S-L-z;

Point (12) = {-Ti/2,e/2,z2,l1};
Point (13) = {Ti/2,e/2,z2,l1};
Point (32) = {-Ti/2,-e/2,z2,l1};
Point (33) = {Ti/2,-e/2,z2,l1};

Point (20) = {S/2-Wb,-e/2,S,l1};
Point (21) = {S/2,-e/2,S,l1};
Point (22) = {S/2-Wb,-e/2,S-L,l1};
Point (23) = {S/2,-e/2,S-L-x,l1};
//Point (24) = {0,-e/2,C+Wb,l1};
Point (25) = {0,-e/2,C,l1};
Point (26) = {-(S/2-Wb),-e/2,S-L,l1};
Point (27) = {-S/2,-e/2,S-L-x,l1};
Point (28) = {-(S/2-Wb),-e/2,S,l1};
Point (29) = {-S/2,-e/2,S,l1};
Point (30) = {0,-e/2,S-L,l1};
Point (31) = {0,-e/2,S-L-x,l1};

Line(30)={0,1};
Line(40)={20,21};
Line(31)={0,2};
Line(41)={20,22};
Line(32)={1,3};
Line(42)={21,23};
Ellipse(33) = {2,10,6,13};
Ellipse(43) = {22,30,26,33};
Ellipse(39) = {6,10,2,12};
Ellipse(49) = {26,30,22,32};
Line(34)={6,8};
Line(44)={26,28};
Line(35)={7,9};
Line(45)={27,29};
Line(36)={8,9};
Line(46)={28,29};
Ellipse(37) = {3,11,7,5};
Ellipse(47) = {23,31,27,25};
Ellipse(38) = {7,11,3,5};
Ellipse(48) = {27,31,23,25};

Line(50) = {0,20};
Line(51) = {1,21};
Line(52) = {2,22};
Line(53) = {3,23};
Line(54) = {2,22};
Line(55) = {3,23};
//Line(56) = {4,24};
Line(57) = {5,25};
Line(58) = {6,26};
Line(59) = {7,27};
Line(60) = {8,28};
Line(61) = {9,29};
Line(62) = {13,33};
Line(63) = {12,32};


//===========================================================================
//Tige interieur
//===========================================================================

Point (100) = {-Ti/2,e/2,S,l1};
Point (101) = {Ti/2,e/2,S,l1};


Point (200) = {-Ti/2,-e/2,S,l1};
Point (201) = {Ti/2,-e/2,S,l1};

Line(300) = {100,101};
Line(301) = {101,13};
//Line(302) = {13,12};
Line(303) = {12,100};
Line(304) = {200,201};
Line(305) = {201,33};
//Line(306) = {33,32};
Line(307) = {32,200};

Line(308) = {100,200};
Line(309) = {101,201};


//Loop

Line Loop(500) = {30,32,37,-38,35,-36,-34,39,303,300,301,-33,-31};
Line Loop(501) = {40,42,47,-48,45,-46,-44,49,307,304,305,-43,-41};

//Interieur
Line Loop(502) = {30,51,-40,-50};
Line Loop(503) = {31,54,-41,-50};
Line Loop(504) = {33,62,-43,-54};
Line Loop(505) = {-39,58,49,-63};
Line Loop(506) = {34,60,-44,-58};
Line Loop(507) = {36,61,-46,-60};


//Exterieur
Line Loop(508) = {35,61,-45,-59};
Curve Loop(509) = {38,57,-48,-59};
Curve Loop(510) = {-37,53,47,-57};
Line Loop(511) = {-32,51,42,-53};

//Tige
Line Loop(512) = {303,308,-307,-63};
Line Loop(513) = {300,309,-304,-308};
Line Loop(514) = {301,62,-305,-309};




Plane Surface(600) = {500};
Plane Surface(601) = {501};
Surface(602) = {502};
Surface(603) = {503};
Surface(604) = {504};
Surface(605) = {505};
Surface(606) = {506};
Surface(607) = {507};
Surface(608) = {508};
Surface(609) = {509};
Surface(610) = {510};
Surface(611) = {511};
Surface(612) = {512};
Surface(613) = {513};
Surface(614) = {514};



//===========================================================================
//Cylindre 
//===========================================================================


Point (2000) = { 0, 0 ,0,l1};
Point (2001) = {rTank, 0 , 0,l1};
Point (2002) = {0, rTank , 0,l1};
Point (2003) = {-rTank, 0 , 0,l1};
Point (2004) = {0, -rTank , 0,l1};
Point (20010) = { 0, 0 ,hTank,l1};
Point (20011) = {rTank, 0 ,  hTank,l1};
Point (20012) = {0, rTank ,  hTank,l1};
Point (20013) = {-rTank, 0 , hTank,l1};
Point (20014) = {0, -rTank , hTank,l1};

Circle(1000) = {2001,2000,2002};
Circle(1001) = {2002,2000,2003};
Circle(1002) = {2003,2000,2004};
Circle(1003) = {2004,2000,2001};
Circle(1004) = {20011,20010,20012};
Circle(1005) = {20012,20010,20013};
Circle(1006) = {20013,20010,20014};
Circle(1007) = {20014,20010,20011};
Line(1011) = {2001,20011};
Line(1012) = {2002,20012};
Line(1013) = {2003,20013};
Line(1014) = {2004,20014};

Line Loop(1) ={1000:1003};
Line Loop(2) ={1004:1007};

Line Loop(3) = {1003,1011,-1007,-1014};
Line Loop(4) = {1000,1012,-1004,-1011};
Line Loop(5) = {1001,1013,-1005,-1012};
Line Loop(6) = {1002,1014,-1006,-1013};

Plane Surface (101) = {1};
Plane Surface (102) = {2};
Surface (103) = {3};
Surface (104) = {4};
Surface (105) = {5};
Surface (106) = {6};

//===========================================================================
//Volume final
//===========================================================================

Surface Loop (2) = {101:106,-600,-601,-602,-603,-604,-605,-606,-607,-608,-609,-610,-611,-612,-613,-614};
Volume (2) = {2};

Physical Surface ("Cote") = {101,103:106};
Physical Surface ("Haut") = {102};

Physical Surface ("melangeur") = {600:614};


Physical Volume ("volfinal") = {2};







