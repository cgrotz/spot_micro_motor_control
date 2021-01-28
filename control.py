class Joint:
    def __init__(self, pwm, pwm_id, center, rest, min, max, degree_to_pwm_width = (575-80/180)):
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
        if angle_in_pw > min and angle_in_pw < max:
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


