import pandas as pd
import requests
import textwrap

from pandas.io.json import json_normalize
from string import Template
from tqdm import tqdm

import config

from text import normalize

from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel


def lda(domain):

    common_texts = normalize(domain=domain)

    common_dictionary = Dictionary(common_texts)
    common_corpus = [common_dictionary.doc2bow(text) for text in common_texts]

    lda = LdaModel(common_corpus, num_topics=2, per_word_topics=True, id2word=common_dictionary)

    # print(common_dictionary.token2id)
    return lda
