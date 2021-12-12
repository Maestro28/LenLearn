from app import app, db
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    # don't work
    return {'db': db, 'User': User, 'Post': Post}