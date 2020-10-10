import datetime
from django.utils.crypto import get_random_string
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

# extending user model
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # count number of waiting comments
#     nb_comments = models.PositiveSmallIntegerField(default=0, editable=False)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# def rewrite_mpolynomial(mpolynomial):
#     mpolynomial = mpolynomial.replace(" ", "")
#     sign_list = ["x^", "y^"]
#     b = ""
#     for i in range(len(mpolynomial)):
#         if mpolynomial[i] == "-" or mpolynomial[i] == "+":
#             # če je kak člen pred znakom
#             # if possible there is x^n and y^n before this sign (n number >= 1)
#             if i > 0:
#                 if i > 1:
#                     # if plus is two spaces after x^ or y^ (case x^a+) 
#                     if mpolynomial[i-3]+ mpolynomial[i-2] in sign_list:
#                         b = b + " " + mpolynomial[i] + " "
#                     # or if plus is one space after ) (case x^(2n+3))
#                     elif mpolynomial[i-1] == ")":
#                         b = b + " " + mpolynomial[i] + " "
#                     # sign is in m_ij
#                     else:
#                         b= b + mpolynomial[i]
#                 # sign is in m_ij
#                 else:
#                     b = b + mpolynomial[i]
#             else:
#                 raise Exception("Check form of M-polynomial; - or + on second position")
#         elif mpolynomial[i] == "x" or mpolynomial[i] == "y":
#             b = b + " " + mpolynomial[i]
#         # elif wq[i] == " ":  # naceloma to ni mozno ker smo nardil replace (wq)
#         #     b = b
#         else:
#             b = b + mpolynomial[i]
#     if b[0] == " ":
#         b = b[1:len(b)]
#     if b[len(b)-1] == " ":
#         b == b[0:len(b) - 1]
#     return b



# Driver code
string = "())(()"
#print(do_parentheses_match(string))

def find_outer_parentheses_clousure(mpolynomial, i, parenth_start):
    # print("v funkciji")
    # print("i", i)
    # print("parenth_start", parenth_start )
    # beremo dokler se zunanji odprti oklepaj ne zapre
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

    # zapišemo polinom do zunanjega zaprtega oklepaja
    poli =  mpolynomial[i:parenth_start + counter + 1]
   # print("poli", poli)
    # nastavimo parametre, da nadaljujemo z branjem v glavni for zanki na koncu zunanjega zaprtega oklepaja (t.j., da ne beremo 2x)
    u = i + 1
    v = parenth_start + counter
   # print("u", u)
    #print("v", v)
    return [poli, u, v]
def read_number(mpolynomial, i):
  #  print("read_number")
    number = ""
    while i < len(mpolynomial) and mpolynomial[i].isdigit():
        number = number + mpolynomial[i]
        i = i + 1
    last_position = i - 1
    # print(mpolynomial[i-1].isdigit())
    # print("last",last_position)
    # print("len", len(mpolynomial))
    return [number, last_position]


def rewrite_mpolynomial(mpolynomial):
    mpolynomial = mpolynomial.replace(" ", "")
    print(mpolynomial)
    b = ""
    u = -2
    v = -1
    for i in range(len(mpolynomial)):
        if u <= i <= v:
            continue
        #print("mpoli", mpolynomial[i])
        #print(i)

        if mpolynomial[i] == "x" or mpolynomial[i] == "y":
           # print("x ali y")
            if mpolynomial[i+1] == "^":
              #  print("stresica")
                if mpolynomial[i+2] == "(":
                    #  potenca z več členi npr. x^(3+4b) #to naceloma ni mozno? (def mpolinom)
                    results = find_outer_parentheses_clousure(mpolynomial, i, i+2)
                    poli = results[0]
                    u = results[1]
                    v = results[2]
                    b = b + " " + poli + " "
                elif mpolynomial[i+2].isdigit():
                    #print(i+2)
                    number = read_number(mpolynomial, i+2)[0]
                    v = read_number(mpolynomial, i+2)[1]
                    u = i + 1
                    b = b + " " + mpolynomial[i:i+2] + number + " "

                else:
                    #primer potence z enim členom npr. x^a #to tudi ni mozno (def mpolinom)
                    # zapišemo x^a s presledkom prej in kasneje in
                    # nastavimo parametre da ne beremo še enkrat členov "^" in "a"
                    b = b + " " + mpolynomial[i:i+2+1] + " "
                    u = i + 1
                    v = i + 2

            else:
                # x ali y brez potence
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
    for _ in range(10):
        string = get_random_string(8)
        if not Mpolynom.objects.filter(Mid=string).exists():
            break
    else:
        raise ValueError('Too many attempts to generate the Mid.')
    return string

# @classmethod
# def get_name(user):
#     if user.first_name and user.last_name:
#         return user.first_name + " " + user.last_name
#     else:
#         return user.username


    
# Create your models here. # preimenuj polynom
class Mpolynom(models.Model):
    mpolynomyal = models.CharField("M-polynomial", max_length=1000) ### popravi, zaradi presledkov ne dela
    structure_name = models.CharField(max_length=200, unique=True) # keywords - glede na to da unique?? dopuscamo vec ali ne
    #structure_picture = models.ImageField()
    keywords = models.CharField(max_length=200, blank=True) #
    comments = models.TextField(blank=True)
    references = models.TextField(blank=True)
    links = models.TextField(blank=True)
    author = models.CharField(default = User, max_length=100, editable=False)
    publication_date = models.DateField(auto_now=True) #spremeni primere
    status = models.CharField(max_length = 15, default = "waiting", choices=[
        ("waiting","waiting"),
        ("approved","approved"),
        ("disapproved","disapproved"),
        ("new_comments","new_comments"),
    ])
    new_keywords = models.CharField(max_length=200, blank=True) #
    new_comments = models.TextField(blank=True)
    new_references = models.TextField(blank=True)
    new_links = models.TextField(blank=True)
    new_comments_authors = models.CharField(max_length=5000, blank=True)
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
        #return '%s %s' % (self.mpolynomyal , self.keywords)
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