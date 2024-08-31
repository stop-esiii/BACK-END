import click
from flask.cli import with_appcontext


@click.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from STOP_APP.extensions import db
    from STOP_APP.models import User

    click.echo("create user")
    user = User(username="henrique", email="pincellihenrique9@gmail.com", password="fatec@2024", active=True)
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")
