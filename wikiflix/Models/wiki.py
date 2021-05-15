from flask import url_for

from wikiflix.db.db_short import *

class wiki(Model):
    __tablename__ = "wiki"

    #ID die uniek moet zijn
    id = Column(Integer, primary_key=True, autoincrement=True)
    #titel van de serie/film
    title = Column(String(100), nullable=False)
    #hoeveel afleveringen
    episodes = Column(Integer) 
    #hoe lang de tetale kijktijd
    watch_time = Column(Integer, nullable=False) 
    #kleine uitleg
    summary = Column(String(500))
    #sterren uit de show
    stars = Column(String(200))
    #id van regisseur  
    regisseur = Column(Integer, nullable=False)
    #de foto voor de cover
    foto= Column(Blob())

@classmethod
def get(cls, *_, **kwargs):
    return cls.query.filter_by(**kwargs).first()

@classmethod
def get_all(cls, *_, **kwargs):
    return cls.query.filter_by(**kwargs).all()

def cover_art_src(self):
		if self.cover_art:
			return self.foto
		else:
			return url_for('wiki.static', filename='img/default_cover_art.jpg')