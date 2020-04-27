from django.db import models

# Create your models here.
class Mpolynom(models.Model):
    mpolynomyal = models.CharField("M-polynomial", max_length=1000) ### popravi
    structure_name = models.CharField(max_length=200)
    #structure_picture = models.ImageField()
    keywords = models.CharField(max_length=200) #
    comments = models.TextField()
    references = models.TextField()
    links = models.TextField()
    author = models.CharField(max_length=100)
    publication_date = models.DateField()