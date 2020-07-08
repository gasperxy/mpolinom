import datetime
from django.utils.crypto import get_random_string
from django.db import models
from django.utils import timezone

def rewrite_mpolynomial(mpolynomial):
    mpolynomial = mpolynomial.replace(" ", "")
    sign_list = ["x^", "y^"]
    b = ""
    for i in range(len(mpolynomial)):
        if mpolynomial[i] == "-" or mpolynomial[i] == "+":
            # if possible there is x^n or y^n before this sign (n number)
            if i > 2:
                # if plus is two spaces after x^or y^ (case x^a+) 
                if mpolynomial[i-3]+ mpolynomial[i-2] in sign_list:
                    b = b + " " + mpolynomial[i] + " "
                # or if plus is one space after ) (case x^(2n+3))
                elif mpolynomial[i-1] == ")":
                    b = b + " " + mpolynomial[i] + " "
                # sign is in m_ij
                else:
                    b= b + mpolynomial[i]
            # sign is in m_ij
            else:
                b = b + mpolynomial[i]
        elif mpolynomial[i] == "x" or mpolynomial[i] == "y":
            b = b + " " + mpolynomial[i]
        # elif wq[i] == " ":  # naceloma to ni mozno ker smo nardil replace (wq)
        #     b = b
        else:
            b = b + mpolynomial[i]
    if b[0] == " ":
        b = b[1:len(b)]
    if b[len(b)-1] == " ":
        b == b[0:len(b) - 1]
    return b


def unique_rand():
    for _ in range(10):
        string = get_random_string(8)
        if not Mpolynom.objects.filter(Mid=string).exists():
            break
    else:
        raise ValueError('Too many attempts to generate the Mid.')
    return string
    
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
   # class Foo(models.Model):
    Mid = models.CharField("id", max_length=10, default=unique_rand, editable=False)
    nb_tokens = models.PositiveSmallIntegerField(default=0, editable=False)
    def save(self, *args, **kwargs):
        b = rewrite_mpolynomial(self.mpolynomyal)
        self.mpolynomyal = b
        split = b.split()
        self.nb_tokens = len(split)
        super(Mpolynom, self).save(*args, **kwargs) # Call the "real" save() method.

    def replace(self, *args, **kwargs): # a je to ok
        return self.mpolynomyal.replace(*args, **kwargs)
    def __len__(self):
        return len(self.mpolynomyal)
    # omogoci iteracijo
    def __iter__(self):
       ''' Returns the Iterator object '''
       return iter(self.mpolynomyal)
    def __str__(self):
        return self.mpolynomyal #tukaj poves reprezentacijo objektov
        #dodamo metodo, ki deluje na teh objektih
    def __getitem__(self, key):
        return self.mpolynomyal[key]

    def __setitem__(self, key, value):
        return self.mpolynomyal[key] == value
    def published_recently(self): 
        """true if published in last seven days"""
        now = timezone.now().date()
        return now - datetime.timedelta(days=7) <= self.publication_date <= now
    published_recently.admin_order_field = 'publication_date'
    published_recently.boolean = True
        #return self.publication_date >= timezone.now().date() - datetime.timedelta(days=7)
    def split_links(self):
        return self.links.split(",")
    def split_comments(self):
        return self.comments.split(",")
    def split_references(self):
        return self.references.split(",")
    # change name displayed on django admin site
    class Meta:
        verbose_name = "M-polynomial"