from app import app, db
from app.models import User, Home, Item

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Home': Home, 'Item': Item}