//Define Variables
tubeDiameter = 10.3;
scaler = 1;
module Base(){
    rotate([180,0,0]) scale([scaler,scaler,scaler]) import("BottleCap.stl");
    translate([0,0,0]) cylinder(h = 10, d = 32, $fn=150);
}
module TubeMounts(){
    difference(){
        Base();
        translate([-8,0,-5]) cylinder(h = 40, d = tubeDiameter, $fn=60);
        translate([8,0,-5]) cylinder(h = 40, d = tubeDiameter, $fn=60);
    }
}

TubeMounts();