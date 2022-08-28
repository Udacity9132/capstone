from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from models import db, Movie, Actor

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# Seed the Database with movies and actors

def seed():
    Movie(title='Example movie', release_date='2022-05-05').insert()
    Movie(title='Berlin movie', release_date='2022-01-03').insert()
    Movie(title='London movie', release_date='2022-02-03').insert()
    Movie(title='SF movie', release_date='2022-03-03').insert()
    Movie(title='NYC movie', release_date='2022-04-03').insert()

    Actor(name='London actor', age='25', gender='male').insert()
    Actor(name='Berlin actor', age='23', gender='male').insert()
    Actor(name='SF actor', age='24', gender='female').insert()
    Actor(name='NYC actor', age='28', gender='female').insert()

if __name__ == '__main__':
    manager.run()