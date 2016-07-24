from django.db import models
from django.contrib.auth.models import User


class Hand(models.Model):
    """Hand gets created at the start of every hand"""
    table = models.ForeignKey(Table)
    start = models.DateTimeField(start=start)


class DealerAction(models.Model):
    """Records every card dealt...  If no user is recorded then its a community card"""
    hand = models.ForeignKey(Hand)
    user = models.ForeignKey(User)
    card = models.CharField(max_length=3)
    time = models.DateTimeField(auto_now=True)


class PlayerAction(models.Model):
    """Records each player, their stack and their action...  (the stack size is before the bet)"""
    hand = models.ForeignKey(Hand)
    user = models.ForeignKey(User)
    stack = models.IntegerField
    bet = models.IntegerField
    time = models.DateTimeField(auto_now=True)


class ServerAction(models.Model):
    """TODO:  Track server actions like timing out players after a given length of inactivity"""
    pass
