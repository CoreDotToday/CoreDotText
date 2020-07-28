# -*- coding: utf8 -*-
"""
# Original Code
https://github.com/hrs/python-tf-idf/blob/master/tfidf.py

The simplest TF-IDF library imaginable.
Add your documents as two-element lists `[docname, [list_of_words_in_the_document]]` with `addDocument(docname, list_of_words)`. Get a list of all the `[docname, similarity_score]` pairs relative to a document by calling `similarities([list_of_words])`.

: 2014-10-17 by Kyunghoon Kim.
  Document type changed to dict Type. ( Original : List )
  This is for Hickle input format.

import tfidf

table = tfidf.tfidf()
table.addDocument("foo", ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel"])
table.addDocument("bar", ["alpha", "bravo", "charlie", "india", "juliet", "kilo"])
table.addDocument("baz", ["kilo", "lima", "mike", "november"])

print(table.similarities (["alpha", "bravo", "charlie"]) # => [['foo', 0.6875], ['bar', 0.75], ['baz', 0.0]])
"""

from .similarity import cosine_similarity


class Tfidf:
    """

    """
    def __init__(self):
        self.weighted = False
        self.documents = {}
        self.corpus_dict = {}

    def add_document(self, doc_name, list_of_words):
        # building a dictionary
        doc_dict = {}
        for w in list_of_words:
            doc_dict[w] = doc_dict.get(w, 0.) + 1.0
            self.corpus_dict[w] = self.corpus_dict.get(w, 0.0) + 1.0

        # normalizing the dictionary
        # length = float(len(list_of_words))
        for k in doc_dict:
            doc_dict[k] = doc_dict[k]
            # doc_dict[k] = doc_dict[k] / length

        # add the normalized document to the corpus
        self.documents[doc_name] = doc_dict

    def similarities(self, list_of_words):
        """Returns a list of all the [docname, similarity_score] pairs relative to a list of words."""

        # building the query dictionary
        query_dict = {}
        for w in list_of_words:
            query_dict[w] = query_dict.get(w, 0.0) + 1.0

        # normalizing the query
        length = float(len(list_of_words))
        for k in query_dict:
            query_dict[k] = query_dict[k] / length

        # computing the list of similarities
        sims = []
        for dockey in self.documents.keys():
            score = 0.0
            doc_dict = self.documents[dockey]
            for k in query_dict:
                if k in doc_dict:
                    score += (query_dict[k] / self.corpus_dict[k]) + (doc_dict[k] / self.corpus_dict[k])
            sims.append([dockey, score])

        return sims