//Define Variables
tubeDiameter = 10.3;
scaler = 1;
tubeGap = .7;
module Base(){
    difference(){
        rotate([90,0,0]) translate([-19,-22.0,-17]) scale([scaler,scaler,scaler]) import("AdapterCap.stl");
        translate([-100,-100,0]) cube([200,200,200]);
    }
    translate([0,0,0]) cylinder(h = 10, d = 32, $fn=150);
}
module TubeMounts(){
    difference(){
        Base();
        translate([-(5.15+tubeGap/2),0,-0.1]) cylinder(h = 40, d = tubeDiameter, $fn=60);
        translate([5.15+tubeGap/2,0,-0.1]) cylinder(h = 40, d = tubeDiameter, $fn=60);
    }
}
TubeMounts();