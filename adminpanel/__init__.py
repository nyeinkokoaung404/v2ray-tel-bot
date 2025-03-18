from .restart.restart import setup_restart_handler

def setup_adminpanel_handlers(app):
    setup_restart_handler(app)