
from django_elasticsearch_dsl.registries import registry
from .models import Mpolynom

from django.core.files import File
import datetime

from elasticsearch_dsl import connections, TokenCount, Object, Text, Document, analyzer, Date
#from elasticsearch_dsl import Document


connections.create_connection(hosts=['localhost'], timeout=20)

 
# create elasticsearch index
#@registry.register_document
class MpolynomDocument(Document):
    mpolynomyal = Text(
        fields={'nb_tokens': TokenCount(analyzer=analyzer('whitespace'))}
    )
    structure_name = Text()
            #'structure_picture',
    keywords = Text()
    comments = Text()
    references = Text()
    links = Text()
    author = Text()
    publication_date = Date()
    
    # mpolynomyal = fields.ObjectField(properties={
    #     "mpolynomyal" : fields.TextField(fields = {
    #         'nb_tokens': TokenCount(analyzer='whitespace')})
    
    #dsl.Object(properties={
    #    'name': seeker.RawString,
    #    'age': dsl.Integer(),
    #})
    #fields.TextField(fields={
    #        'length': fields.IntegerField(type='token_count',analyzer='whitespace')
    #    })
    def prepare_mpolynomyal(self, instance):
        b = ""
        for elt in instance:
            if elt == "-" or elt == "+":
                b = b + " " + elt + " "
            elif elt == "x" or elt == "y":
                b = b + " " + elt
            elif elt == " ":
                b = b
            else:
                b = b + elt
        if b[0] == " ":
            b = b[1:len(b)]
        if b[len(b)-1] == " ":
            b == b[0:len(b) - 1]
        return b
        
    class Index:
        # Name of the Elasticsearch index
        name = 'mpolynomials_index'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

        # mappings = {
        #      "properties": {
        #         "mpolynomyal": { 
        #             "type": "text",
        #             "fields": {
        #             "length": { 
        #                 "type":     "token_count",
        #                 "analyzer": "whitespace"
        #             }
        #             }
        #         },
        #         "keywords" : {"type" : "text"},
        #         "comments" : {"type" : "text"},
        #         "references" : {"type" : "text"},
        #         "links" : {"type" : "text"},
        #         "author" : {"type" : "text"},
        #         "publication_date" : {"type" : "date"}
        #         }
        #     }


    class Django:
        model = Mpolynom # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
           # 'mpolynomyal',
            'structure_name',
            #'structure_picture',
            'keywords',
            'comments',
            'references',
            'links',
            'author',
            'publication_date'
        ]

MpolynomDocument.init()

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
# mpolynomyal= '2x + 3', 
# structure_name = 'novovv',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, rolinom',
# comments = 'zeloo lep',
# references = 'ni, ni',
# links = 'naštimaj settingse da je lahko polje prazno',
# author = 'Mate Matik',
# publication_date = '2020-04-23'
# )
# poli.save()

# Mpoli = Mpolynom(
# mpolynomyal= '5x^2 + 3', 
# structure_name = 'Mpoliroli',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura, kemijski graf',
# comments = 'neki pa je',
# references = 'čakamo',
# links = 'link',
# author = 'Mate Fik in P. Olde',
# publication_date = '2020-03-23'
# )
# Mpoli.save()

# M1poli = Mpolynom(
# mpolynomyal= '5x^2 + 45x + 3', 
# structure_name = 'M1poliroli, rolo polo',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura, kemijski graf in še kaj',
# comments = 'neki pa je ane',
# references = 'čakamo na boljše čase',
# links = 'link',
# author = 'Fik in P. Olde'
# )
# M1poli.save()

# p= Mpolynom(
# mpolynomyal= '12x^2 + 45x^2 - 2x + 3', 
# structure_name = 'poseben graf, rolo polo',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# p.save()

# sss= Mpolynom(
# mpolynomyal= '-x^2', 
# structure_name = 'ssssturasss',
# #poli.structure_picture.save('poliomina.png', django_file, save=True)
# keywords = 'polinom, struktura',
# comments = 'ni komentarjev',
# references = 'poglej za ovinek',
# links = 'link, link1',
# author = 'Tomo the boss'
# )
# sss.save()