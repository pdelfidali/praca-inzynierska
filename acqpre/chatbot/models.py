from django.db import models


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Response(models.Model):
    text = models.CharField(max_length=250, unique=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, unique=True)
    legal_basis = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.text} [{self.tag}]'


class Pattern(models.Model):
    text = models.CharField(max_length=1000)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text} [{self.tag}]'
