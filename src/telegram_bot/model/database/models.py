# from tortoise import models, fields
# from datetime import datetime
#
#
# class User(models.Model):
#     id = fields.BigIntField(pk=True, generated=True)
#     user_name = fields.CharField(max_length=250, verbose_name="Имя пользователя в телеграмме", unique=True)
#     account_id = fields.BigIntField(verbose_name="ID пользователя в телеграмме", unique=True)
#     name = fields.CharField(max_length=250, verbose_name="Имя")
#     type = fields.CharField(max_length=250, choices=["Новичок", "Продолжаю", "Профи"])
#     image = fields.BinaryField(verbose_name="Фото")
#     height = fields.FloatField(verbose_name="Рост", blank=True, null=True)
#     weight = fields.FloatField(verbose_name="Вес", blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         table = "user"
#
#
# class Target(models.Model):
#     id = fields.BigIntField(pk=True)
#     user_id = fields.ForeignKeyField(
#         "models.User",
#         on_delete=fields.CASCADE,
#         verbose_name="ID пользователя",
#         related_name="user_target"
#     )
#     name = fields.CharField(max_length=100, verbose_name="Цель")
#     begin = fields.DatetimeField(default=datetime.now(), verbose_name="Дата начала")
#     end = fields.DatetimeField(vrbose_name="Дата окончания")
#     status = fields.BooleanField(default=False, verbose_name="Статус достижения цели")
#
#     def __str__(self):
#         return self.name

from datetime import datetime
from sqlalchemy import (
    Integer,
    Float,
    String,
    Column,
    LargeBinary,
    DateTime,
    Boolean,
    ForeignKeyConstraint
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "User"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_name = Column(String(70), unique=True)
    account_id = Column(Integer(), unique=True)
    name = Column(String(70))
    type = Column(String(50))
    image = Column(String(250))
    height = Column(Float(), nullable=True)
    weight = Column(Float(), nullable=True)


class Target(Base):
    __tablename__ = "Target"
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ["User.id"], ondelete="CASCADE"),
    )
    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(Integer())
    name = Column(String(100))
    begin = Column(DateTime(timezone=True), default=datetime.now())
    end = Column(DateTime(timezone=True), default=datetime.now())
    status = Column(Boolean(), default=False)
