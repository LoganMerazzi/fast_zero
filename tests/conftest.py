import pytest
from fastapi.testclient import TestClient
from fast_zero.app import app
from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker

from fast_zero.models import User, Base


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def teste_create_user(session):
    new_user = User(
        username='sophia', password='secret', email='teste@teste.com'
    )
    session.add(new_user)
    session.commit

    user = session.scalar(select(User).where(User.username == 'sophia'))

    assert user.username == 'sophia'


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)
