from django.db import models
from django.contrib.postgres.fields import ArrayField


class UserGame(models.Model):
    flag = models.BooleanField(default='True')
    game_over = models.BooleanField(default='False')
    user1_token=models.CharField(max_length=15)
    user2_token = models.CharField(max_length=15)
    user1_move = ArrayField(models.SmallIntegerField(),size=22,)
    user2_move = ArrayField(models.SmallIntegerField(),size=22,)
    matrix1 = ArrayField(
        ArrayField(
            models.SmallIntegerField(),
            size=7,
        ),
        size=8,
    )
