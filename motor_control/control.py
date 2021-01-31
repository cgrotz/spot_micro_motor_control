SERVO_MAX = 575
SERVO_MIN = 80

class Joint:
    def __init__(self, pwm, pwm_id, center, rest, min, max, degree_to_pwm_width = ((SERVO_MAX-SERVO_MIN)/180)):
        self.pwm = pwm
        self.pwm_id = pwm_id
        self.center = center
        self.rest = rest
        self.min = min
        self.max = max
        self.degree_to_pwm_width = degree_to_pwm_width
    
    def set_pulse_width(self, pulse_width):
        if pulse_width > self.min and pulse_width < self.max:
            self.pwm.set_pwm( self.pwm_id, 0, int(pulse_width) )

    def rest(self):
        self.set_pulse_width( self.rest )

    def center(self):
        self.set_pulse_width( self.center )

    def set_angle_relative_from_center(self, angle):
        angle_in_pw = SERVO_MAX - ( self.center + angle * self.degree_to_pwm_width )
        self.set_pulse_width( angle_in_pw )

    def set_angle_absolute(self, angle):
        angle_in_pw = SERVO_MAX - ( angle * self.degree_to_pwm_width )
        self.set_pulse_width( angle_in_pw )
        
class Leg:
    def __init__(self, wrist, hip, shoulder):
        self.wrist = wrist
        self.hip = hip
        self.shoulder = shoulder

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
        self.shoulder.set_angle_relative_from_center(angles[0])
        self.hip.set_angle_relative_from_center(angles[1])
        self.wrist.set_angle_relative_from_center(angles[2])

class MotorControl:
    def __init__(self, left_front, left_back, right_front, right_back):
        self.left_front = left_front
        self.left_back = left_back
        self.right_front = right_front
        self.right_back = right_back

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
        self.right_back.set_angles(angles[0])
        self.right_front.set_angles(angles[1])
        self.left_front.set_angles(angles[2])
        self.left_back.set_angles(angles[3])



