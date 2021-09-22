from iBott import ChromeBrowser
from iRobot import settings

browser = ChromeBrowser(undetectable=True)
browser.load_extension(settings.EXTENION_PATH)
browser.open()
browser.maximize_window()


