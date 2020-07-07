from app import App
from gunicorn.app.base import BaseApplication
import multiprocessing
import sys
import os

application = App()
app = application.get_app()


class StartServer(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    if('--prod' in sys.argv):
        options = {
            'bind': '%s:%s' % ('0.0.0.0', '5000'),
            'workers': (multiprocessing.cpu_count() * 2) + 1,
            'reload': True,
        }
        StartServer(app, options).run()
    else:
        os.environ['FLASK_ENV'] = "development"
        app.run()
