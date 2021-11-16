import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Report(Base):  # inheritance

    __tablename__ = "reports"  # variable = tablename

    id = Column(Integer, primary_key=True)
    title = Column(String,)
    desc = Column(String)  # description
    img_name = Column(String)


if __name__ == "__main__":
    engine = create_engine('sqlite:///db.sqlite3')
    Base.metadata.create_all(engine)
