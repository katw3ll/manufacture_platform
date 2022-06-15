from django.apps import AppConfig
#from . import signal

class RolgroupConfig(AppConfig):
    name = 'rolgroup'

    def ready(self):
        from . import signal
