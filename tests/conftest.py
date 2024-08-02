import pytest
from app import create_app, mongo

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.from_mapping({
        'TESTING': True,
        'MONGO_URI': 'mongodb://localhost:27017/testdb'
    })

    with app.app_context():
        # Initialize the database
        mongo.db.rules.drop()
        mongo.db.assets.drop()

    yield app

    with app.app_context():
        # Cleanup after tests
        mongo.db.rules.drop()
        mongo.db.assets.drop()

@pytest.fixture
def client(app):
    return app.test_client()
