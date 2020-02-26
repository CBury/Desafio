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
    debts = relationship('Debt', backref='debtor')

    def __repr__(self):
        return '<Person cpf:{}, name:{}>'.format(self.cpf, self.name)


class Debt(Base):
    __tablename__ = 'debts'
    uuid = Column(Integer, primary_key=True)
    value = Column(Float)
    company = Column(String(20), index=True)
    description = Column(String(100))
    date = Column(Date)
    status = Column(String(15), index=True)
    debtor_cpf = Column(String(11), ForeignKey('persons.cpf'))

    def __repr__(self):
        return '<Debt: value:{}, company:{}, status:{}, debtor:{}>'.format(self.value, self.company, self.status, self.debtor_cpf)

def init_db():
    url = 'mysql://{}:{}@{}'.format('root', '$hAdOw8rUn5', '127.0.0.1:3306')
    engine = create_engine(url)  # connect to server
    create_str = "CREATE DATABASE IF NOT EXISTS {}; USE db_a".format('db_a')
    engine.execute(create_str)

    # import yourapplication.models
    Base.metadata.create_all(bind=engine)

    # Create a test user
    Session = sessionmaker(bind=engine)
    session = Session()

    john = Person(cpf='12312312345', name='John Doe', address='Rua Teste 44')
    debt = Debt(value=545, company='Vivo', description='conta de telefone',
                date=datetime.datetime.strptime('2019-12-06', '%Y-%m-%d'), status='EM ABERTO')
    debt.debtor = john
    session.add(debt)
    session.add(john)
    jane = Person(cpf='89089089076', name='Jane Doe', address='Rua Teste 44')
    debt2 = Debt(value=765, company='Eletropaulo', description='conta de energia',
                 date=datetime.datetime.strptime('2019-09-04', '%Y-%m-%d'), status='EM ABERTO')
    debt3 = Debt(value=134, company='Comgas', description='conta de gás',
                 date=datetime.datetime.strptime('2018-11-17', '%Y-%m-%d'), status='EM ABERTO')
    debt2.debtor = jane
    debt3.debtor = jane
    session.add(debt2)
    session.add(debt3)
    session.add(jane)
    session.commit()
    Person.query.all()
    Debt.query.all()
    session.commit()


if __name__ == '__main__':
    init_db()
