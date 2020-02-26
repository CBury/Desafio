from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class Person(Base):
    __tablename__ = 'persons'
    cpf = Column(String(11), primary_key=True)
    name = Column(String(50), index=True)
    address = Column(String(50))
    source_of_income = Column(String(50))
    assets = relationship('Asset', backref='owner')

    def __repr__(self):
        return '<Person cpf:{}, name:{}>'.format(self.cpf, self.name)


class Asset(Base):
    __tablename__ = 'assets'
    uuid = Column(Integer, primary_key=True)
    value = Column(Float)
    description = Column(String(100))
    owner_cpf = Column(String(11), ForeignKey('persons.cpf'))

    def __repr__(self):
        return '<Asset: value:{}, description:{}, owner:{}>'.format(self.value, self.description, self.owner_cpf)

def init_db():
    url = 'mysql://{}:{}@{}'.format('root', '$hAdOw8rUn5', '127.0.0.1:3306')
    engine = create_engine(url)  # connect to server
    create_str = "CREATE DATABASE IF NOT EXISTS {}; USE {}".format('db_b, db_b')
    engine.execute(create_str)

    # import yourapplication.models
    Base.metadata.create_all(bind=engine)

    # Create a test user
    Session = sessionmaker(bind=engine)
    session = Session()

    john = Person(cpf='12312312345', name='John Doe', address='Rua Teste 44')
    asset = Asset(value=54500,  description='carro VW Gol azul')
    asset2 = Asset(value=250000, description='casa em Pinheiros')
    asset.owner = john
    asset2.owner = john
    session.add(asset)
    session.add(asset2)
    session.add(john)
    jane = Person(cpf='89089089076', name='Jane Doe', address='Rua Teste 44')
    asset3 = Asset(value=350000, description='Apartamento em Balneário')
    asset3.owner = jane
    session.add(asset3)
    session.add(jane)
    session.commit()
    Person.query.all()
    Asset.query.all()


if __name__ == '__main__':
    init_db()
