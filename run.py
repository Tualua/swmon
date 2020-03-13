from swmon import create_app
from swmon.models import db, Switch, Router, Settings

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Switch': Switch, 'Settings': Settings, 'Router': Router}
