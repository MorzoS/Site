from flask_login import UserMixin
from werkzeug import security

from wikiflix.db.db_short import *

class User(Model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)

    email = Column(String(28))
    display_name = Column(String(28))
    first_name = Column(String(28))
    last_name = Column(String(28))

    password = Column(String(64))

    @classmethod
    def user_exists(cls, email):
            return bool(cls.get(email))

    @classmethod
    def get(cls, email):
        return cls.query.filter_by(email=email).first()

    @staticmethod
    def secure_password(password: str):
        return security.generate_password_hash(password)
    def check_password(self, password: str):
        return security.check_password_hash(self.password, password)

class CarouselImage(Model):

	def __init__(self, *args, **kwargs):
		Model.__init__(self, *args, **kwargs)

	id = Column(Integer, primary_key=True, nullable=False)
	flim_id = Column(Integer, ForeignKey('film.id'))
	subtext = Column(String(255))
	image = Column(Blob)
