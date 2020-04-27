from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Mpolynom

from django.core.files import File
import datetime

from elasticsearch_dsl import connections

connections.create_connection(hosts=['localhost'], timeout=20)
# create elasticsearch index
@registry.register_document
class MpolynomDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'mpolynomials_index'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Mpolynom # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'mpolynomyal',
            'structure_name',
            #'structure_picture',
            'keywords',
            'comments',
            'references',
            'links',
            'author',
            'publication_date'
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

    poli = Mpolynom(
    mpolynomyal= '2x + 3', 
    structure_name = 'poliroli',
    #poli.structure_picture.save('poliomina.png', django_file, save=True)
    keywords = 'polinom, rolinom',
    comments = 'zeloo lep',
    references = 'ni, ni',
    links = 'naštimaj settingse da je lahko polje prazno',
    author = 'Mate Matik',
    publication_date = '2020-04-23'
    )
    poli.save()

    Mpoli = Mpolynom(
    mpolynomyal= '5x^2 + 3', 
    structure_name = 'Mpoliroli',
    #poli.structure_picture.save('poliomina.png', django_file, save=True)
    keywords = 'polinom, struktura, kemijski graf',
    comments = 'neki pa je',
    references = 'čakamo',
    links = 'link',
    author = 'Mate Fik in P. Olde',
    publication_date = '2020-03-23'
    )
    Mpoli.save()