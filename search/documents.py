from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Mpolynom, rewrite_mpolynomial_see

from django.core.files import File
import datetime

from elasticsearch_dsl import connections

connections.create_connection(hosts=['localhost'], timeout=20)
# create Elasticsearch index
@registry.register_document
class MpolynomDocument(Document):
    mpolynomial = fields.TextField(analyzer='whitespace')
    Mid = fields.KeywordField()
    status = fields.KeywordField()

    def prepare_mpolynomial_see(self, instance):
        return rewrite_mpolynomial_see(instance)
        
    class Index:
        # Name of the Elasticsearch index
        name = 'mpolynomials_index'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        # The model associated with this Document
        model = Mpolynom 

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'structure_name',
            'keywords',
            'comments',
            'references',
            'links',
            'author',
            'publication_date',
            'nb_tokens',
            'new_keywords',
            'new_comments',
            'new_references',
            'new_links',
            'new_comments_authors',
            'mpolynomial_see',
        ]