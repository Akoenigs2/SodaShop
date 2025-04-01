#include <Servo.h>

Servo myServo;  // Create a servo object

void setup() {
    myServo.attach(3); // Attach servo to Digital Pin 3
}

void loop() {
    // Move servo from 0 to 180 degrees
    for (int pos = 0; pos <= 180; pos += 5) {
        myServo.write(pos);
        delay(20); // Small delay for smooth movement
    }

    // Move servo back from 180 to 0 degrees
    for (int pos = 180; pos >= 0; pos -= 5) {
        myServo.write(pos);
        delay(20);
    }
}
