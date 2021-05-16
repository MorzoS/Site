from flask import url_for

from wikiflix.db.db_short import *

class wiki(Model):
    __tablename__ = "wiki"

    #ID die uniek moet zijn
    id = Column(Integer, primary_key=True, autoincrement=True)
    #titel van de serie/film
    titel = Column(String(100), nullable=False)
    #hoeveel afleveringen
    afleveringen = Column(Integer) 
    #hoe lang de tetale kijktijd
    kijktijd = Column(Integer, nullable=False) 
    #kleine uitleg
    samenvatting = Column(String(500))
    #sterren uit de show
    stars = Column(String(200))
    #Releasejaar van de serie of film
    releasejaar = Column(Integer)
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

def foto_src(self):
		if self.foto:
			return self.foto
		else:
			return url_for('wiki.static', filename='img/default_foto.jpg')