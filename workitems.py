from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty, OptionProperty, NumericProperty
from kivy.clock import Clock
import datetime

class WorkItems(Screen):

    # def disconnect(self):
    #     self.manager.transition = SlideTransition(direction="right")
    #     self.manager.current = 'login'
    #     self.manager.get_screen('login').resetForm()

    def open_workitem(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'mainscreen'
        #self.manager.get_screen('mainscreen').resetForm()

