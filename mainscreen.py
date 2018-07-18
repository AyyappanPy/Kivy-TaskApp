from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty, OptionProperty, NumericProperty
from kivy.clock import Clock
import datetime

class MainScreen(Screen):

    mode = OptionProperty('normal', options=('normal', 'down'))
    total_seconds = NumericProperty()
    total = NumericProperty()
    workitem_started_dt = StringProperty()

    def __init__(self, **kwargs):
        self.mode = 'normal'
        super(MainScreen, self).__init__(**kwargs)

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'workitems'
        self.manager.get_screen('workitems').resetForm()

    def start_timer(self):
        if self.mode == 'normal':
            self.workitem_started_dt = str(datetime.datetime.now())
            Clock.schedule_interval(self.timer, 60)
            self.ids.btn_start_workitem.background_normal = 'atlas://textures/images/traco-atlas/pause_small'
            self.ids.btn_start_workitem.background_down = 'atlas://textures/images/traco-atlas/pause_small'
            self.mode = 'down'
        else:
            workitem_started = datetime.datetime.strptime(self.workitem_started_dt, '%Y-%m-%d %H:%M:%S.%f')

            self.total_seconds = (datetime.datetime.now()-workitem_started).total_seconds()
            self.total += self.total_seconds

            m, s = divmod(self.total, 60)
            h, m = divmod(m, 60)
            self.update_timer.text = u'[color=e9003a]%02d:%02d[/color]' % (h, m)
            Clock.unschedule(self.timer)
            self.ids.btn_start_workitem.background_normal = 'atlas://textures/images/traco-atlas/play_small'
            self.ids.btn_start_workitem.background_down = 'atlas://textures/images/traco-atlas/play_small'
            self.mode = 'normal'

    def timer(self, dt):
        now = datetime.datetime.now()
        # self.update_timer.text = u'[color=e9003a]{0} [/color]'.format(now.strftime('%S:') or '00.00') #now.strftime('%S:')
        # self.update_timer.text += u'[color=e9003a]{0} [/color]'.format(str(now.microsecond)[:3] or '00.00') #str(now.microsecond)[:3]

        workitem_started = datetime.datetime.strptime(self.workitem_started_dt, '%Y-%m-%d %H:%M:%S.%f')

        self.total_seconds = (now-workitem_started).total_seconds()
        m, s = divmod(self.total_seconds, 60)
        h, m = divmod(m, 60)
        self.update_timer.text = u'[color=e9003a]%02d:%02d[/color]' % (h, m)

    def open_workitems(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'workitems'