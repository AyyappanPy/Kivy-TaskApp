from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, SwapTransition

from mainscreen import MainScreen
from workitems import WorkItems
from kivy.network.urlrequest import UrlRequest
import urllib
from kivy.uix.popup import Popup



class TracoPopup(Popup):
    pass

class Login(Screen):
    def do_login(self, UserName, Password):
        if UserName and Password:
            app = App.get_running_app()
            app.username = UserName
            app.password = Password
            params = urllib.urlencode({'@number': 12524, '@type': 'issue','@action': 'show'})
            login_url = 'http://www.tracopedia.com/TracopediaApi/api/Login/ValidUser?UserName={username}&Password={password}'.format(username=UserName, password=Password)
            req = UrlRequest(login_url, on_success=self.got_success_login_json, on_error=self.got_error_login_json,req_body=params)
            #req = UrlRequest("http://www.tracopedia.com/TracopediaApi/api/Login/ValidUser?UserName=Rajenthiran&Password=RJthir2101", on_success=self.got_success_login_json, on_error=self.got_error_login_json,req_body=params)
            req.wait()
        else:
            pass

    def got_success_login_json(self, req, result):
        if result:
            if result.get('UserId'):
                self.manager.transition = SwapTransition() #SlideTransition(direction="left")
                self.manager.current = 'mainscreen'
        else:
            popup = TracoPopup()
            popup.open()

    def got_error_login_json(self, req, result):
        pass

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""

class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        self.manager = ScreenManager()

        self.bind(on_start=self.post_build_init)

        self.manager.add_widget(Login(name='login'))
        self.manager.add_widget(MainScreen(name='mainscreen'))
        self.manager.add_widget(WorkItems(name='workitems'))

        return self.manager

    def post_build_init(self,ev):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 4 or key == 27:
            print self.manager.current
            if(self.manager.current=='mainscreen'):
                App.get_running_app().stop()
            elif (self.manager.current=='workitems'):
                self.manager.transition = SlideTransition(direction="right")
                self.manager.current='mainscreen'
            return True

    # def get_application_config(self):
    #     if(not self.username):
    #         return super(LoginApp, self).get_application_config()
    #
    #     conf_directory = self.user_data_dir + '/' + self.username
    #
    #     if(not os.path.exists(conf_directory)):
    #         os.makedirs(conf_directory)
    #
    #     return super(LoginApp, self).get_application_config(
    #         '%s/config.cfg' % (conf_directory)
    #     )

if __name__ == '__main__':
    LoginApp().run()