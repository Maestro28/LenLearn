from app import app, db
from app.models import User, Post
from flask.cli import FlaskGroup

@app.shell_context_processor
def make_shell_context():
    # don't work
    return {'db': db, 'User': User, 'Post': Post}


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    cli()