from pymongo import MongoClient
from os import environ as env
import click
import datetime
from flask import current_app, g
from flask.cli import with_appcontext

MONGO_URL = env.get('MONGO_URL')
if not MONGO_URL or MONGO_URL is '':
    MONGO_URL = "mongodb://localhost:27017"

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db_client' not in g:
        g.db_client = MongoClient(MONGO_URL)
    if 'db' not in g:
        g.db = g.db_client.airbnb
    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db_client = g.pop('db_client', None)

    if db_client is not None:
        db_client.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    return db


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
