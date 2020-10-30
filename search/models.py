import datetime
from django.utils.crypto import get_random_string
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords

def find_outer_parentheses_clousure(mpolynomial, i, parenth_start):
    """Finds outer parentheses clousure.
        args: 
        str mpolynomial - string in which we are searching parenthesis closure
        int i - position in mpolynomial, that will be first character in returned arg poli
        int parenth_start - position in mpolynomial, where parentheses start, char is ( 
        return:
        list including args poli, u and v:
            str poli - string created from mpolynomial starting on i-th position, ending on outher parentheses clousure position
            int u - not for reading starting position (see rewrite_mpolynomial u and v)
            int v - not for reading ending position (see rewrite_mpolynomial u and v)
    """
    # read unitll you find first parentheses closure
    reading = True
    open_par = 1
    counter = 1
    while reading:
        if mpolynomial[parenth_start + counter] == "(":
            open_par = open_par + 1
        if mpolynomial[parenth_start + counter] == ")":
            open_par = open_par - 1
        if open_par == 0:
            reading = False
            counter = counter
        elif counter < 0:
            raise Exception(
                "Higher number of closed parenthesis than opened, shouldn be happening, check do_parentheses_match")
        else:
            counter = counter + 1
    # write poly from i-th position (e.g. variable x) to outer parentheses clousure position
    poli =  mpolynomial[i:parenth_start + counter + 1]
    # set parameters to start reading again after outer parentheses clousure (we dont read twice)
    u = i + 1
    v = parenth_start + counter
    return [poli, u, v]


def read_number(mpolynomial, i):
    """Reads string as long as it is readnig digits - finds number
        args: 
        str mpolynomial - string in which we are reading the number
        int i - starting number position in mpolynomial
        return:
        list including args number, last_position:
            str number - string created from mpolynomial starting on i-th position, ending with last consecutive digit character
            int last_position - position of last consecutive digit in mpolynomial
    """
    number = ""
    while i < len(mpolynomial) and mpolynomial[i].isdigit():
        number = number + mpolynomial[i]
        i = i + 1
    last_position = i - 1
    return [number, last_position]


def rewrite_mpolynomial(mpolynomial):
    """Rewrites mpolynomial in specific structure: spaces around "main" + and - signs, around vars and vars with power and around opened and closed outer parantheses (...)
        args:
        str mpolynomial - string which we are rewriting
        return:
        str b: rewrited mpolynomial
    """
    mpolynomial = mpolynomial.replace(" ", "")
    b = ""
    u = -2
    v = -1
    # we already wrote poly between u and v, we do not read it again
    for i in range(len(mpolynomial)):
        if u <= i <= v:
            continue
        if mpolynomial[i] == "x" or mpolynomial[i] == "y":
            # vars
            if i+1 < len(mpolynomial):
                if mpolynomial[i+1] == "^":
                    # var with power
                    if i+2 < len(mpolynomial):
                        if mpolynomial[i+2] == "(":
                            #  power with multiple signs, e.g. x^(3+4b) #shouldt be happening, see definition of mpolynomial
                            results = find_outer_parentheses_clousure(mpolynomial, i, i+2)
                            poli = results[0]
                            u = results[1]
                            v = results[2]
                            b = b + " " + poli + " "
                        elif mpolynomial[i+2].isdigit():
                            # number with more than one digit
                            number = read_number(mpolynomial, i+2)[0]
                            v = read_number(mpolynomial, i+2)[1]
                            u = i + 1
                            b = b + " " + mpolynomial[i:i+2] + number + " "
                        else:
                            # power with one non-digit sign e.g. x^a #shouldt be happening, see definition of mpolynomial
                            # write x^a with spaces before and after
                            # set parameters u and v to not read "^" and "a" again
                            b = b + " " + mpolynomial[i:i+2+1] + " "
                            u = i + 1
                            v = i + 2
                    else:
                        # shouldnt be happening - see clean method in admin.py
                        raise Exception("M-polynomial variable power missing")     
                else:
                    # x or y without power
                    b = b + " " + mpolynomial[i] + " "
            else:
                    # x or y without power - last sign in mpoly
                    b = b + " " + mpolynomial[i] + " "
        elif mpolynomial[i] == "+" or mpolynomial[i] == "-":
            b = b + " " + mpolynomial[i] + " "
        elif mpolynomial[i] == "(":
            results = find_outer_parentheses_clousure(mpolynomial, i, i)
            poli = results[0]
            u = results[1]
            v = results[2]
            b = b + poli
        else:
            b = b + mpolynomial[i]
    b = b.replace("  ", " ")
    if b[0] == " ":
        b = b[1:len(b)]
    if b[len(b)-1] == " ":
        b == b[0:len(b) - 1]
    return b


def unique_rand():
    """Generates unique random string of length 8
        return:
        str string - random string of length 8
    """
    for _ in range(10):
        string = get_random_string(8)
        if not Mpolynom.objects.filter(Mid=string).exists():
            break
    else:
        raise ValueError('Too many attempts to generate the Mid.')
    return string
    

class Mpolynom(models.Model):
    history = HistoricalRecords(inherit=True)
    mpolynomial = models.CharField("M-polynomial", max_length=1000)
    structure_name = models.CharField(max_length=200, unique=True)
    keywords = models.CharField(max_length=200, blank=True) #
    comments = models.TextField(blank=True)
    references = models.TextField(blank=True)
    links = models.TextField(blank=True)
    author = models.CharField(default = User, max_length=100, editable=False)
    author_username = models.CharField("Username", default = User, max_length=100, editable=False)
    publication_date = models.DateField(auto_now=True)
    status = models.CharField(max_length = 15, default = "waiting", choices=[
        ("waiting","waiting"),
        ("approved","approved"),
        ("declined","declined"),
        ("new_comments","new comments"),
    ])
    new_keywords = models.CharField(max_length=200, blank=True) #
    new_comments = models.TextField(blank=True)
    new_references = models.TextField(blank=True)
    new_links = models.TextField(blank=True)
    new_comments_authors = models.CharField(max_length=5000, blank=True)
    Mid = models.CharField("id", max_length=10, default=unique_rand, editable=False)
    nb_tokens = models.PositiveSmallIntegerField(default=0, editable=False)

    def save(self, *args, **kwargs):
            b = rewrite_mpolynomial(self.mpolynomial)
            self.mpolynomial = b
            split = b.split()
            self.nb_tokens = len(split)
            # Call the "real" save() method.
            super(Mpolynom, self).save(*args, **kwargs)

    def replace(self, *args, **kwargs): 
        return self.mpolynomial.replace(*args, **kwargs)

    def __len__(self):
        return len(self.mpolynomial)

    # define iteration
    def __iter__(self):
       return iter(self.mpolynomial)

    # representation of mpoly objects
    def __str__(self):
        return self.mpolynomial 

    def __getitem__(self, key):
        return self.mpolynomial[key]

    def __setitem__(self, key, value):
        return self.mpolynomial[key] == value
    
    def published_recently(self): 
        """Returns true if published in last seven days
        return:
        boolean - tells if object was created or changed in last week"""
        now = timezone.now().date()
        return now - datetime.timedelta(days=7) <= self.publication_date <= now
    published_recently.admin_order_field = 'publication_date'
    published_recently.boolean = True

    def split_links(self):
        return self.links.split(",")

    def split_comments(self):
        return self.comments.split(",")

    def split_references(self):
        return self.references.split(",")

    # change name displayed on django admin site
    class Meta:
        verbose_name = "M-polynomial"



# TO DO urls about
# TO DO clean templates v search

