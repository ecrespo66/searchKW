from iBott import ChromeBrowser, Excel
from iBott.robot_activities import Robot, Robotmethod, get_all_Methods
from google_search import Keywords
from iBott.system_activities import saveFileFromOrchestrator
import iRobot.settings as settings


class Main(Robot):
    def __init__(self, args):
        self.methods = get_all_Methods(self)
        if args is not None:
            self.robotId = args['RobotId']
            self.ExecutionId = args['ExecutionId']
            self.url = args['url']
            self.username = args['username']
            self.password = args['password']
            self.robotParameters = args['params']
            super().__init__(robotId=self.robotId, ExecutionId=self.ExecutionId, url=self.url,
                             username=self.username, password=self.password,
                             params=self.robotParameters)
        else:
            super().__init__()

    @Robotmethod
    def init(self):
        self.browser = ChromeBrowser(undetectable=True)
        self.browser.load_extension(settings.EXTENION_PATH)
        self.browser.headless()
        self.browser.open()
        self.browser.maximize_window()
        self.keywords =[]
        self.keyword = Keywords(self)
        try:
            if len(self.findQueuesByName("KW5")) == 0:
                self.queue = self.createQueue("KW5")
            else:
                self.queue = self.findQueuesByName("KW5")[0]
        except:
            pass


    @Robotmethod
    def cleanup(self):
        """Clean system before executing the robot"""


    @Robotmethod
    def start(self):
        """Init variables, instance objects and start the applications you are going to work with"""
        self.read_input()
        for keyword in self.keywords:
            self.queue.createItem({'Keyword': keyword})


    @Robotmethod
    def process(self):
        """Run robot process"""
        Qitem = self.queue.getNextItem()
        if Qitem:
            try:
                Qitem.setItemAsWorking()
                k = Qitem.value['Keyword']
                self.Log.info("Processing : " + k)
                self.keyword.get_search_data(Qitem)
                self.keyword.get_page_data()
                self.keyword.store_data()
                Qitem.setItemAsOk()
            except:
                Qitem.setItemAsFail()
            self.process()


    @Robotmethod
    def end(self):
        """Finish robot execution, cleanup environment, close applications and send reports"""
        self.browser.close()

    def read_input(self):
        '''Privte method reads Excel sent from Orchestrator'''
        file = saveFileFromOrchestrator(self.robotParameters['file-1632235752781'], settings.FILES_PATH)
        excel = Excel(file)
        i=1
        while True:
            data = excel.readCell(f"A{i}")
            if data is None:
                break
            else:
                self.keywords.append(data)
            i += 1




