from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(username='sophia', password='secret', email='test@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'sophia'))

    assert user.username == 'sophia'
