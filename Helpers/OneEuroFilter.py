import math

class OneEuroFilter:
    def __init__(self, fcm = 1.0, b= 0.007, fcd = 1.0):
        self.fcm = fcm
        self.b = b
        self.fcd = fcd
        self.cfc = self.fcm
        self.alpha_vel = 0

        self.p_pos = 0
        self.p_time = 0.0
        self.p_filtered_vel = 0

        self.c_pos = 0
        self.c_time = 0.0
        self.c_filtered_vel = 0

    def apply(self,pos,time):
        if self.p_pos != 0:
            self.c_time = time
            self.c_pos = pos
            raw_vel = self.calc_velocity()
            self.calc_filtered_vel(raw_vel)
            self.calc_new_cfc()
            new_pos = self.calc_filtered_pose()
            self.p_pos = new_pos
            self.p_time = time
            self.p_filtered_vel = self.c_filtered_vel

            self.c_pos = 0
            self.c_time = 0.0
            self.c_filtered_vel = 0

            return new_pos
        else:
            self.p_pos = pos
            self.p_time = time

            return pos

    def calc_pos_tao(self):
        return 1/(2 * math.pi * self.cfc)

    def calc_vel_tao(self):
        return 1/(2 * math.pi * self.fcd)

    def calc_alpha_pos(self):
        tao = self.calc_pos_tao()
        delta_time = self.c_time - self.p_time
        below = 1 + (delta_time / tao)
        return 1/below

    def calc_velocity(self):
        delta_time = self.c_time - self.p_time
        delta_pos = self.c_pos - self.p_pos
        return delta_pos / delta_time

    def calc_alpha_vel(self):
        tao = self.calc_vel_tao()
        delta_time = self.c_time - self.p_time
        below = 1 + (delta_time / tao)
        self.alpha_vel = 1/below

    def calc_filtered_vel(self, raw_vel):
        current_trust = self.alpha_vel * raw_vel
        past_trust = (1 - self.alpha_vel) * self.p_filtered_vel
        self.c_filtered_vel = current_trust + past_trust

    def calc_new_cfc(self):
        self.cfc = self.fcm + (self.b * abs(self.p_filtered_vel))

    def calc_filtered_pose(self):
        alpha_pos = self.calc_alpha_pos()
        current_trust = alpha_pos * self.c_pos
        past_trust = (1 - alpha_pos) * self.p_pos
        return current_trust + past_trust





