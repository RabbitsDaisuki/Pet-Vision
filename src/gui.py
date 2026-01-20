from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App

class WindowManager(ScreenManager):
    pass

class MainScreen(Screen):
    def logic_action(self):
        App.get_running_app().stop()

class ControlScreen(Screen):

    pass

class MonitorScreen(Screen):
    
    pass

class SettingScreen(Screen):

    pass
