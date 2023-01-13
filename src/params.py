# -*- coding: utf-8 -*-
"""
For: UMR TETIS RESEARCH UNIT
Author: rodrique_kafando
"""

import spacy

## NLP transformers model
nlp_model = spacy.load('en_core_web_trf')

#########  geonames var
import geocoder
key='kafando.rodrique'

country_alias = {'US' : ['United States', 'United States of America'],
                 'USA': ['United States of America', 'United States'],
                 'UK' : ['United Kingdom'], 'NY': ["New York"],
                 'DRC' : ['DR Congo', 'Democratic Republic of Congo' ],
                 'DR Congo' : ['Democratic Republic of Congo', 'DRC'],
                 "Côte d'Ivoire" : ['Ivory Coast' , 'RCI'],
                 'CA' : ['Canada'], 'NSW' : ['New South Wales']
}
