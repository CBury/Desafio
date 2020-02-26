from sqlalchemy import Column, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class DocumentEvents(Base):
    cpf = Column(String(20), index=True)
    last_query = Column(Date)
    financial_transactions = Column(Float)
    last_buy = Column(Float)

    def __repr__(self):
        return '<Event for cpf:{} last_query:{}, financial_transactions:{}, last_buy:{}>'.format(self.cpf, self.last_query, self.financial_transactions, self.last_buy)


def init_db():
    url = 'mysql://{}:{}@{}'.format('root', '$hAdOw8rUn5', '127.0.0.1:3306')
    engine = create_engine(url)  # connect to server
    create_str = "CREATE DATABASE IF NOT EXISTS {}; USE db_c".format('db_c')
    engine.execute(create_str)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    john = DocumentEvents(cpf='12312312345', last_buy=datetime.datetime.strptime('2019-12-06', '%Y-%m-%d'), financial_transactions=7897)
    session.add(john)
    session.commit()


if __name__ == '__main__':
    init_db()
