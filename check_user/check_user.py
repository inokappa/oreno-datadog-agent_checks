import time
import subprocess
from checks import AgentCheck

class CheckUser(AgentCheck):
    def check(self, instance):
        threshold_user = self.init_config.get('threshold_user', 3)
        current_login_count = self.login_check()
        self.gauge('login.user.check', current_login_count)
        if int(current_login_count) >= int(threshold_user):
        	self.send_event(current_login_count, threshold_user, 'error')

    def login_check(self):
        count = subprocess.check_output('w -sh | wc -l', shell=True)  
        return count.strip()

    def send_event(self, current_login_count, threshold_user, alert_type):
        self.event({
            'timestamp': int(time.time()),
            'event_type': 'login_user_check',
            'msg_title': 'Still Login user count check',
            'msg_text': '%s users still login.(Threshhold : %s users)' % (current_login_count, threshold_user),
            'aggregation_key': 'login.user.check',
            'alert_type': alert_type
        })
