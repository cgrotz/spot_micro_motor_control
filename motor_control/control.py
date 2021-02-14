SERVO_MAX = 570
SERVO_MIN = 90

import time
import random
import RPi.GPIO as GPIO

class Joint:
    def __init__(self, pwm, pwm_id, min, max, disabled = False, degree_to_pwm_width = 2.5, correction = 0, debug = False ):
        self.pwm = pwm
        self.pwm_id = pwm_id
        self.min = min
        self.max = max
        self.correction = correction
        self.disabled = disabled
        self.degree_to_pwm_width = degree_to_pwm_width
        self.debug = debug

    def set_pulse_width(self, pulse_width):
        if self.disabled == False:
            pulse_width = abs(int(pulse_width))
            if self.debug:
                print("Trying to set pw", self.pwm_id, pulse_width, self.min, self.max)
            if pulse_width >= self.min and pulse_width <= self.max:
                self.pwm.set_pwm( self.pwm_id, 0, pulse_width )

    def center(self):
        self.set_pulse_width( self.min + (90 + self.correction) * self.degree_to_pwm_width )

    def set_angle_relative_from_center(self, angle):
        if self.debug:
            print("Trying to set angle", angle)
        angle = (angle + self.correction)
        if self.debug:
            print("Trying to set corrected angle", angle)
        if angle >= 0:
            angle_in_pw = self.max - (angle * self.degree_to_pwm_width)
        elif angle < 0:
            angle_in_pw = angle * self.degree_to_pwm_width
            angle_in_pw = self.min + abs(angle_in_pw)

        self.set_pulse_width( angle_in_pw )

    def set_angle_absolute(self, angle):
        angle = (angle + self.correction)
        angle_in_pw = abs( angle * self.degree_to_pwm_width )
        self.set_pulse_width( angle_in_pw )
    
    def set_disabled(self, disabled):
        self.disabled = disabled

class Leg:
    def __init__(self, wrist, hip, shoulder, shoulder_inverted = False):
        self.wrist = wrist
        self.hip = hip
        self.shoulder = shoulder
        self.shoulder_inverted = shoulder_inverted

    # collisions
    def rest(self):
        self.shoulder.rest()
        self.wrist.rest()
        self.hip.rest()

    ''' Sets the angles for this legs.

        Used for interoperability with Spot Micro Python
        Args:
            angles: Angles in the order q1,q2,q3. (hip, leg, knee)
                      An example output:
                         (lb_q1,lb_q2,lb_q3)
        Returns:
            None
    '''
    def set_angles(self, angles):
        if self.shoulder_inverted:
            self.shoulder.set_angle_relative_from_center(90 - angles[0])
        else:
            self.shoulder.set_angle_relative_from_center(angles[0] - 90)
        #time.sleep(0.005)
        self.hip.set_angle_relative_from_center(angles[1])
        #time.sleep(0.005)
        self.wrist.set_angle_relative_from_center(angles[2])
        #time.sleep(0.005)
    
    def set_disabled(self, disabled):
        self.shoulder.set_disabled(disabled[0])
        self.hip.set_disabled(disabled[1])
        self.wrist.set_disabled(disabled[2])

class MotorControl:
    def __init__(self, left_front, left_back, right_front, right_back, relay_pin = 13):
        self.left_front = left_front
        self.left_back = left_back
        self.right_front = right_front
        self.right_back = right_back
        self.relay_pin = relay_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(relay_pin, GPIO.OUT)

    def __del__(self):
        GPIO.output(self.relay_pin, GPIO.LOW)
        GPIO.cleanup()

    def rest(self):
        self.left_front.rest()
        self.left_back.rest()
        self.right_front.rest()
        self.right_back.rest()
    
    ''' Sets the leg angles for all four legs.

        Used for interoperability with Spot Micro Python
        Args:
            angles: Tuple of 4 of the leg angles. Legs in the order rightback
                      rightfront, leftfront, leftback. Angles in the order q1,q2,q3. (hip, leg, knee)
                      An example output:
                        ((rb_q1,rb_q2,rb_q3),
                         (rf_q1,rf_q2,rf_q3),
                         (lf_q1,lf_q2,lf_q3),
                         (lb_q1,lb_q2,lb_q3))
        Returns:
            None
    '''
    def setAngles(self, angles):
        sequence = [0,1,2,3]
        random.shuffle(sequence)
        for leg in sequence:
            if leg == 0:
                self.right_back.set_angles(angles[0])
            elif leg == 1:
                self.right_front.set_angles(angles[1])
            elif leg == 2:
                self.left_front.set_angles(angles[2])
            else:
                self.left_back.set_angles(angles[3])

    def set_disabled(self, disabled):
        self.right_back.set_disabled(disabled[0])
        self.right_front.set_disabled(disabled[1])
        self.left_front.set_disabled(disabled[2])
        self.left_back.set_disabled(disabled[3])

    def set_motor_relay(self, state):
        if state:
            GPIO.output(self.relay_pin, GPIO.HIGH)
        else:
            GPIO.output(self.relay_pin, GPIO.LOW)


