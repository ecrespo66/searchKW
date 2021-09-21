from iBott.robot_activities import RobotException, get_instances
import iRobot.robot as robot
import iRobot.settings as settings


class BusinessException(RobotException):
    """Manage Exceptions Caused by business errors"""

    def __init__(self, message=None, action=None, element=None):
        self.robotClass = get_instances(robot.Main)
        super().__init__(self.robotClass, action)
        self.action = action
        self.element = element
        self.message = message
        self.processException()

    def processException(self):
        """Write action when a Business exception occurs"""
        if self.action is "next":
            self.element.setItemAsFail()


class SystemException(RobotException):
    """Manage Exceptions Caused by system errors"""

    def __init__(self, message, action):
        super().__init__(get_instances(robot.Main), action)
        self.retry_times = settings.RETRY_TIMES
        self.action = action
        self.message = message
        self.processException()

    def processException(self):
        """Write action when a system exception occurs"""
        self.Log.systemException(self.message)
