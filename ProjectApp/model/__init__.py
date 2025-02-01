from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("mysql+pymysql://root:Lozinka123@mysql:3306/stvaridb")
#engine = create_engine("mysql+pymysql://root:Lozinka123@localhost:3306/stvaridb")
Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()
