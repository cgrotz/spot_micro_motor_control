Motor Control Abstraction for Spot Micro
=============
```
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685(address=0x40)
pwm.set_pwm_freq(SERVO_FREQ)

control = MotorControl(
    left_front = Leg(
        wrist = Joint(pwm, 0, 300, 80, 80, 575),
        hip = Joint(pwm, 1, 300, 340, 80, 575),
        shoulder = Joint(pwm, 2, 310, 310, 80, 575),
    ),
    left_back = Leg(
        wrist = Joint(pwm, 12, 300, 80, 80, 575),
        hip = Joint(pwm, 13, 300, 300, 80, 575),
        shoulder = Joint(pwm, 14, 315, 315,80, 575),
    ),
    right_front = Leg(
        wrist = Joint(pwm, 4, 300, 510, 80, 575),
        hip = Joint(pwm, 5, 300, 300, 80, 575),
        shoulder = Joint(pwm, 6, 295, 295, 80, 575),
    ),
    right_back = Leg(
        wrist = Joint(pwm, 8, 300, 525, 80, 575),
        hip = Joint(pwm, 9, 300, 80, 100, 575),
        shoulder = Joint(pwm, 10, 300, 300,80, 575),
    )
) 
```