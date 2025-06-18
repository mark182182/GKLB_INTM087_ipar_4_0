class MotorEventDto:
    def __init__(self, id, event_time, userId, action, speed=None):
        self.id = id
        self.event_time = event_time
        self.userId = userId
        self.action = action
        self.speed = speed
