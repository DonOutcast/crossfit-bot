from tortoise import models, fields
from datetime import datetime


class User(models.Model):
    id = fields.BigIntField(pk=True, generated=True)
    user_name = fields.BigIntField(verbose_name="Имя пользователя в телеграмме", unique=True)
    account_id = fields.BigIntField(verbose_name="ID пользователя в телеграмме", unique=True)
    name = fields.CharField(max_length=50, verbose_name="Имя")
    type = fields.CharField(max_length=10, choices=["Новичок", "Продолжаю", "Профи"])
    image = fields.BinaryField(verbose_name="Фото")
    height = fields.FloatField(verbose_name="Рост", blank=True, null=True)
    weight = fields.FloatField(verbose_name="Вес", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        table = "user"


class Target(models.Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.ForeignKeyField(
        "models.User",
        on_delete=fields.CASCADE,
        verbose_name="ID пользователя",
        related_name="user_target"
    )
    name = fields.CharField(max_length=100, verbose_name="Цель")
    begin = fields.DatetimeField(default=datetime.now().strftime("%d/%m/%Y"), verbose_name="Дата начала")
    end = fields.DatetimeField(vrbose_name="Дата окончания")
    status = fields.BooleanField(default=False, verbose_name="Статус достижения цели")

    def __str__(self):
        return self.name

