lc = 0.05; // Mesh characteristic length
lc2 = lc;
lc3 = 0;
front3d = 0; // Set to 1 if Frontal 3D mesh algorithm is used
nn = (1./lc)/4.; // Mesh subdivisions per turn, used with Frontal 3D

If(front3d == 1)
  Mesh.Algorithm3D = 4; // Frontal 3D
EndIf
Mesh.Optimize = 1;


turns =10;   //{5, Name "Geometry/Number of coil turns"},
r =0.625;    //{0.11, Name "Geometry/Coil radius"},
rc =0.03;   //{0.01, Name "Geometry/Coil wire radius"},
hc =1.294;    //{0.2, Name "Geometry/Coil height"},
lb =1;      //{1, Name "Geometry/Infinite box width"}
left =1;    // {1, Choices{0,1}, Name "Geometry/Terminals on the left?"}


// inductor
p = newp;
//Point(p)={0, -r, -hc/2, lc};
//Point(p+1)={0, -r+rc, -hc/2, lc};
//Point(p+2)={0, -r, -hc/2+rc, lc};
//Point(p+3)={0, -r-rc, -hc/2, lc};
//Point(p+4)={0, -r, -hc/2-rc,lc};

Point(p)={-hc/2, -r, 0, lc};
Point(p+1)={-hc/2, -r+rc, 0, lc};
Point(p+2)={-hc/2+rc, -r, 0, lc};
Point(p+3)={-hc/2, -r-rc, 0, lc};
Point(p+4)={-hc/2-rc, -r, 0,lc};
c = newl;
Circle(c) = {p+1,p,p+2};
Circle(c+1) = {p+2,p,p+3};
Circle(c+2) = {p+3,p,p+4};
Circle(c+3) = {p+4,p,p+1};
ll = newll;
Line Loop(ll) = {c,c+1,c+2,c+3};
s = news;
Plane Surface(s) = {ll};
tmp[] = {s};
vol_coil[] = {};

For j In {1:4*turns+(left?2:0)}
If(front3d == 1)
  tmp[] = Extrude { {hc/turns/4,0,0}, {1,0,0} , {0,0,0} , Pi/2}
                  { Surface {tmp[0]}; Layers {nn / 4}; };
EndIf
If(front3d == 0)
  tmp[] = Extrude { {hc/turns/4,0,0}, {1,0,0} , {0,0,0} , Pi/2}
                  { Surface {tmp[0]}; };
EndIf
  vol_coil[] += tmp[1];
EndFor

Mesh.ElementOrder = 1;
Mesh.SecondOrderLinear = 1;
Mesh.HighOrderOptimize = 1;
Mesh.SubdivisionAlgorithm = 2; // quad

Physical Volume(0) = {1:1000};





