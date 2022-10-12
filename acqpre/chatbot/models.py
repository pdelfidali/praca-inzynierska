from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Response(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, unique=True)
    text = models.TextField(max_length=2500, unique=True)
    legal_basis = models.CharField(max_length=250)
    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.text} [{self.tag}]'


class Pattern(models.Model):
    text = models.CharField(max_length=1000)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text} [{self.tag}]'


class Rating(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    rating = models.IntegerField()
    ip = models.GenericIPAddressField()

    class Meta:
        unique_together = ('response', 'ip')
