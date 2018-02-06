import sqlalchemy
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker


print(sqlalchemy.__version__)

# 打印执行的命令的 SQL格式命令
engine = create_engine('sqlite:///foo.db', echo=True)


Base = declarative_base()


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    passward = Column(String)

    def __repr__(self):
        return '<User(name="%s", fullname="%s", passward="%s")>' % (
            self.name, self.fullname, self.passward)

#创建数据库
# Base.metadata.create_all(engine)
ed_user = User(name='ed', fullname='Ed jones', passward='edspassward')
# print(ed_user)

Session = sessionmaker(bind=engine)
session = Session()
# session.add(ed_user)
#
#查询符合条件的第一条
# our_user = session.query(User).filter_by(name='ed').first()
# # select * from User where name='ed' limit 1;
#
# session.add_all([
#     User(name='wendy', fullname='Wendy Williams', passward='foobar'),
#     User(name='wendy2', fullname='Wendy Williams', passward='foobar'),
#     User(name='wendy3', fullname='Wendy Williams', passward='foobar')
#     ])
# session.commit()

#查询全部
# print(session.query(User).all())

#查询符合条件的第一条
# our_user = session.query(User).filter_by(name='ed').first()

#排序
# for row in session.query(User).order_by(User.id):
#     print(row)

# 查询 in 操作
# for row in session.query(User).filter(User.name.in_(['ed', 'wendy'])):
#     print(row)

# 查询 not in 操作
# for row in session.query(User).filter(~User.name.in_(['ed', 'wendy'])):
#     print(row)

# count 操作
# print(session.query(User).filter(User.name =='ed').count())

# and 和 or 操作, 需要导入模块
# from sqlalchemy import and_, or_
# for row in session.query(User).filter(and_(User.name == 'ed', User.fullname == 'Ed jones')):
#     print(row)
# for row in session.query(User).filter(or_(User.name == 'ed', User.name =='wendy')):
#     print(row)

# 创建外键
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    user_i = relationship("User", backref=backref('addresses', order_by=id))

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

# Base.metadata.create_all(engine)

# jack = User(name='jack', fullname='Jack Bean', passward='giffs')
# jack.addresses = [
#     Address(email_address='jack@google.com'),
#     Address(email_address='j25@yahoo.com')]
#
# session.add(jack)
# session.commit()
x = 1
for u, a in session.query(User, Address).\
        filter(User.id == Address.user_id).\
        filter(Address.email_address == 'jack@google.com').\
        all():
    print(u, a)

