from sqlalchemy import Column, String, Float, Date, Integer
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mysql.connector
from sqlalchemy.exc import IntegrityError


Base = declarative_base()

class DocumentEvents(Base):
    __tablename__ = 'document_events'
    uuid = Column(Integer, primary_key=True)
    cpf = Column(String(11), index=True)
    last_query = Column(Date)
    financial_transactions = Column(Float)
    last_buy = Column(Float)

    def __repr__(self):
        return '<Event for cpf:{} last_query:{}, financial_transactions:{}, last_buy:{}>'.format(self.cpf, self.last_query, self.financial_transactions, self.last_buy)


def init_db():
    cnx = mysql.connector.connect(user='root', password='root', host='mysql_c', database='db_c')
    cursor = cnx.cursor()
    create_str = "ALTER USER my_user IDENTIFIED WITH mysql_native_password BY 'my_pass';"
    cursor.execute(create_str)
    create_str = "CREATE DATABASE IF NOT EXISTS {}; USE {}".format('db_c', 'db_c')
    cursor.execute(create_str)
    cnx.close()

    url = 'mysql://{}:{}@{}/{}'.format('my_user', 'my_pass', 'mysql_c', 'db_c')
    engine = create_engine(url)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        event1 = DocumentEvents(cpf='12312312345', last_query=datetime.datetime.strptime('2019-12-06', '%Y-%m-%d'),
                              financial_transactions=7897, last_buy=134)
        event2 = DocumentEvents(cpf='89089089076', last_query=datetime.datetime.strptime('2020-02-15', '%Y-%m-%d'),
                                financial_transactions=152, last_buy=15)
        session.add(event2)
        session.add(event1)
        session.commit()
    except IntegrityError as e:
        session.rollback()


if __name__ == '__main__':
    init_db()
