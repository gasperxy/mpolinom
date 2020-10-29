from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Mpolynom, rewrite_mpolynomial

from django.core.files import File
import datetime

from elasticsearch_dsl import connections

connections.create_connection(hosts=['localhost'], timeout=20)
# create elasticsearch index
@registry.register_document
class MpolynomDocument(Document):
    mpolynomyal = fields.TextField(analyzer='whitespace')
    Mid = fields.KeywordField()
    status = fields.KeywordField()

    def prepare_mpolynomyal(self, instance):
        return rewrite_mpolynomial(instance)
        
    class Index:
        # Name of the Elasticsearch index
        name = 'mpolynomials_index'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Mpolynom # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        # tukaj bi mogla dodat še new_comments, ...
        fields = [
            'structure_name',
           # 'Mid',
            'keywords',
            'comments',
            'references',
            'links',
            'author',
            'publication_date',
            'nb_tokens',
            
        ]

# create an object
# import os
# import base64
# THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# my_file = os.path.join(THIS_FOLDER, 'poliomina.png')
# with open(my_file, 'rb') as picture:
# #picture = open(os.path.join(THIS_FOLDER, 'poliomina.png'), 'rb')
# #django_file = File(picture)
#     django_file = base64.b64encode(picture.read())

# poli = Mpolynom(
# mpolynomyal= ' x^2', 
# structure_name = 'nnnnnooooovvooivvvvvvvv',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, rolinom',
# comments = 'zeloo lep',
# references = 'ni, ni',
# links = 'naštimaj settingse da je lahko polje prazno',
# author = 'Mate Matik',
# )
# poli.save()

# Mpoli = Mpolynom(
# mpolynomyal= '2x^2', 
# structure_name = 'Mpppolirolii',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura, kemijski graf',
# comments = 'neki pa je',
# references = 'čakamo',
# links = 'link',
# author = 'Mate Fik in P. Olde',
# )
# Mpoli.save()

# M1poli = Mpolynom(
# mpolynomyal= '2x^3 +22 x^2 -2x +2', 
# structure_name = 'M1poliroli, roolo poolo',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura, kemijski graf in še kaj',
# comments = 'neki pa je ane',
# references = 'čakamo na boljše čase',
# links = 'link',
# author = 'Fik in P. Olde'
# )
# M1poli.save()

# p= Mpolynom(
# mpolynomyal= '22p (m-  1 ) x^2 y^2 + 3', 
# structure_name = 'poosseben graf, rolo polo',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# p.save()

# sss= Mpolynom(
# mpolynomyal= ' 2x^2y^2 +(2r−a−2b+2)x^2y^3 +(a+2b)x^2y^4+(3k−6r+1+a+3b)x^3 y^3 +(4r−a−4b−4)x^3 y^4 +bx^4 y^4 ', 
# structure_name = 'sssttuujras',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' (2p+6)x^2 y^2 +(8p+8q−4)x^2 y^3 +(15pq−10p+2q−1)x^3 y^3 ', 
# structure_name = 'njkkli',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinkom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' (n−a)xy^2 +axy^n +(K+a−2n)x^2 y^2 +(n−a)x^2 y^n',
# structure_name = 'sssttuurkjh',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()




# sss= Mpolynom(
# mpolynomyal= ' (mn−3n+2)x^2 y^2 +2nx^2 y^4 +(n−2)x^4 y^4 ', 
# structure_name = 'sssttuurahs',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= '(m(n−1)(n−2)/2) x^(n−1)y^(n−1) +(n−1)m x^(n−1)y^(m+n−2) + m(m − 1)/2 x^(m+n−2) y^(m+n−2) +2xy, 
# structure_name = 'sssttuuhras',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= '2x^2 y^2 +2nx^2 y^4 +(n−2)x^4y^4 ', 
# structure_name = 'ssshttuuras',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' 5x^2 + 3', 
# structure_name = 'sshhsttuuhghas',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= '2(n+2)x^2 y^2 +4nx^2 y^3 +(4n−3)x^3 y ^3', 
# structure_name = 'ssstyttuhutuuras',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= '6x^2 y^2 +8(n−1)x^2 y^3 +(n(3n−4)+1)x^3 y^3 ', 
# structure_name = 'ssggsshhhhktkkjjtufggfffgurasj',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' (2p+6) x^2 y^3 + 4n x^2 y^3 + (4n−3) x^3 y^3', 
# structure_name = 'sdtssttuuras',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= '  2(n+2) x^4 y^4 + 4n x^2 y^3 + (4n−3) x^3 y^3 ', 
# structure_name = 'ssoias',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' 2x^2y^5 + 3xy^4', 
# structure_name = 'ssooou',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' 5x^2 + 3', 
# structure_name = 'ssisttuoooouras',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' 5x^2 + 45x + 3', 
# structure_name = 'sssttuoopgggoouras',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' 12x^3', 
# structure_name = 'sssttuooiioofdfuras',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' x^2 + 45x^2 - x + 3', 
# structure_name = 'sssttuoooourasii',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' 512x^2 + 45x^2 - 2x + 3', 
# structure_name = 'sssiooifrttuoooouras',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' x^2', 
# structure_name = 'sssttuoooouras',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' 2x^3 +22 x^2 -2x +2', 
# structure_name = 'sssttuoooknjimouras',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= '  22 x^2', 
# structure_name = 'sssiiiiujuttuoooouras',

# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()
# sss= Mpolynom(
# mpolynomyal= '  - x^2', 
# structure_name = 'sssttkkkkkkuoooouryuyas',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' 2x^2', 
# structure_name = 'sssttkkkghjghjkkkuoooouras',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' (mn−3n+2) x^2 y^2 + 2n x^2 y^4 + (n−2) x^4 y', 
# structure_name = 'ras',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'boss'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= '(mn−3n) x^2 y^2 + 2n x^2 y^4 + (n−2) x^4 y^4', 
# structure_name = 'ssst',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Sara Kdo'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' (mn−3n+2) x^2 y^2 +  x^2 y^3 + (n−2) x^4 y^4', 
# structure_name = 'sghjghras',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tretji'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' (mn) x^3 y^2 +  x^2 y^3 + (n−2) x^4 y^4', 
# structure_name = 'sghgyas',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tretji'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= ' (mn+h) x^3 y^2 + 3 x^2 y^3 + (n−2) x^4 y^4', 
# structure_name = 'kjhygyas',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tretji'
# )
# sss.save()

# sss= Mpolynom(
# mpolynomyal= '  3 x^2 y^3 + (n−2) x^4 y^4', 
# structure_name = 'kjhygyasdjdjdjd',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tretji'
# )
# sss.save()