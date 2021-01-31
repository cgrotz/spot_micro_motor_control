class Joint:
    def __init__(self, pwm, pwm_id, center, rest, min, max, degree_to_pwm_width = ((575-80)/180)):
        self.pwm = pwm
        self.pwm_id = pwm_id
        self.center = center
        self.rest = rest
        self.min = min
        self.max = max
        self.degree_to_pwm_width = degree_to_pwm_width

    def rest(self):
        self.pwm.set_pwm( self.pwm_id, 0, self.rest )

    def center(self):
        self.pwm.set_pwm( self.pwm_id, 0, self.center )

    def angle_relative_from_center(self, angle):
        angle_in_pw = self.center + angle * self.degree_to_pwm_width
        if angle_in_pw > self.min and angle_in_pw < self.max:
            self.pwm.set_pwm( self.pwm_id, 0, angle_in_pw )

    def setAngle(self, angle):
        angle_in_pw = self.center + (angle * self.degree_to_pwm_width)
        if angle_in_pw > self.min and angle_in_pw < self.max:
            print("Setting joint to %f", angle_in_pw)
            self.pwm.set_pwm( self.pwm_id, 0, angle_in_pw )
        
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
    def setAngles(self, angles):
        self.shoulder.setAngle(angles[0])
        self.hip.setAngle(angles[1])
        self.wrist.setAngle(angles[2])

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
        self.right_back.setAngles(angles[0])
        self.right_front.setAngles(angles[1])
        self.left_front.setAngles(angles[2])
        self.left_back.setAngles(angles[3])



