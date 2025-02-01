from sqlalchemy import *
from . import Base

class Stvari(Base):
    __tablename__ = "stvari"
    ID_stvar = Column(Integer, primary_key=True)
    ime = Column(String(255), unique=True)
    opis = Column(String(255))