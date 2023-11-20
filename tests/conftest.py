import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app
from fast_zero.database import get_session

from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fast_zero.models import Base, User


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


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
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = User(username='Teste', email='teste@test.com', password='testtest')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
