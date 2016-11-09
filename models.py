from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, DateTime
import os
from datetime import datetime
from config import DB_URI

db_path = os.path.join(os.path.dirname(__file__), DB_URI)
db_uri = 'sqlite:///{}'.format(db_path)
print db_uri
engine = create_engine(db_uri, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Image(Base):

    __tablename__ = 'images'

    id          =   Column(Integer, primary_key=True)
    name        =   Column(String, unique=True, nullable=False)
    size        =   Column(Integer, nullable=False)
    exif_info   =   Column(Integer, default=0)
    created_at  =   Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        str_created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return "<Image (name='%s', size='%d', exif_info=%s, created_at=%s)>" % (self.name, self.size, exif_info, str_created_at)

Base.metadata.create_all(engine)

