from django.db import models

# Create your models here.
class context(models.Model):
    name=models.CharField(max_length=500)

    def __str__(self):
        return self.name
        
class Article(models.Model):
    title = models.CharField(max_length=500)