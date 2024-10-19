from gameplay.enums import State
from gameplay.enums import Times

class Humanoid(object):
    """
    Are they a human or a zombie???
    """
    def __init__(self, fp, state, value, time='d', job='h'):

        self.fp = fp
        self.state = state
        self.value = value
        self.time = time
        self.job = job

    def is_zombie(self):
        return self.state == State.ZOMBIE.value

    def is_injured(self):
        return self.state == State.INJURED.value

    def is_healthy(self):
        return self.state == State.HEALTHY.value

    def is_corpse(self):
        return self.state == State.CORPSE.value

    def is_day(self):
        return self.time == Times.DAY.value

    def is_night(self):
        return self.time == Times.NIGHT.value