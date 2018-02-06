import sqlalchemy
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker


print(sqlalchemy.__version__)

# 利用数据库字符串构造engine, echo为True将打印所有的sql语句
engine = create_engine('sqlite:///foo.db', echo=True)

# 首先需要生成一个BaseModel类,作为所有模型类的基类
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


# 创建所有表,如果表已经存在,则不会创建
# Base.metadata.create_all(engine)
# 删除所有表
# Base.metadata.drop_all(engine)


#创建一个 User 类实例
ed_user = User(name='ed', fullname='Ed jones', passward='edspassward')
# print(ed_user)

# 利用Session对象连接数据库
#创建会话类和会话类的对象
Session = sessionmaker(bind=engine)
session = Session()

# 向事务会话中添加实例对象，向表中插入数据需要提交事务， 调用 commit() 方法
# session.add(ed_user)
#
#查询符合条件的第一条
# our_user = session.query(User).filter_by(name='ed').first()
# 相等于下方的 sql 语句
#  select * from User where name='ed' limit 1;
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

    # 关联 User  表主键为外键，此处为 多对1
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

# 双表联合查询
for u, a in session.query(User, Address).\
        filter(User.id == Address.user_id).\
        filter(Address.email_address == 'jack@google.com').\
        all():
    print(u, a)

# 表修改
# 造数据
he_user = User(id=15, name='he', fullname='He jones', passward='edspassward')
# session.add(he_user)
# session.commit()

# 使用merge方法，如果指定的主键已存在，修改记录，不存在新增一条记录
session.merge(he_user)

session.commit()
session.close()
