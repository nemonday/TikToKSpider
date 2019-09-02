from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BIGINT, Integer
Base = declarative_base()


class Work(Base):
    # 表名称
    __tablename__ = 'work'

    id = Column(BIGINT(), primary_key=True)
    url = Column(String(length=1024), nullable=False)
    Host = Column(String(length=255), nullable=False)
    Connection = Column(String(length=255), nullable=False)
    x_Tt_Token = Column(String(length=255), nullable=False)
    x_tt_trace_id = Column(String(length=255), nullable=False)
    Accept_Encoding = Column(String(length=255), nullable=False)
    Cookie = Column(String(length=1024), nullable=False)
    X_Khronos = Column(String(length=255), nullable=False)
    X_Gorgon = Column(String(length=255), nullable=False)
    user_name = Column(String(length=255), nullable=False)
    status = Column(String(length=255), nullable=False)


class Video(Base):
    # 表名称
    __tablename__ = 'video'
    id = Column(BIGINT(), primary_key=True)
    aweme_id = Column(BIGINT(), nullable=False)
    title = Column(String(length=500), nullable=False)
    nickname = Column(String(length=255), nullable=False)

