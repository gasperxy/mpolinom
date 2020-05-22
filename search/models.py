import datetime
from django.db import models
from django.utils import timezone


# Create your models here. # preimenuj polynom
class Mpolynom(models.Model):
    mpolynomyal = models.CharField("M-polynomial", max_length=1000) ### popravi, zaradi presledkov ne dela
    structure_name = models.CharField(max_length=200, unique=True) # keywords - glede na to da unique?? dopuscamo vec ali ne
    #structure_picture = models.ImageField()
    keywords = models.CharField(max_length=200) #
    comments = models.TextField(blank=True)
    references = models.TextField(blank=True)
    links = models.TextField(blank=True)
    author = models.CharField(max_length=100)
    publication_date = models.DateField(auto_now=True) #spremeni primere
    # omogoci iteracijo
    def __iter__(self):
       ''' Returns the Iterator object '''
       return iter(self.mpolynomyal)
    def __str__(self):
        return self.mpolynomyal #tukaj poves reprezentacijo objektov
        #dodamo metodo, ki deluje na teh objektih
    def published_recently(self): 
        """true if published in last seven days"""
        return self.publication_date >= timezone.now().date() - datetime.timedelta(days=7)
    # change name displayed on django admin site
    class Meta:
        verbose_name = "M-polynomial"