# -*- coding: utf-8 -*-
import requests
import json
import uuid
import logging
import re
from coredottext.nlp import collection

__author__ = "Core.Today"
__version__ = "0.0.1"

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, tclient, name):

        if not isinstance(name, string_type):
            raise TypeError("name must be an instance "
                            "of %s" % (string_type.__name__,))

        self.__name = _unicode(name)
        self.__client = tclient

    @property
    def tclient(self):
        """The client instance for this :class:`Database`."""
        return self.__tclient

    def __repr__(self):
        return "Database(%r, %r)" % (self.__client, self.__name)

    def __getattr__(self, name):
        """Get a collection of this database by name.
        Raises InvalidName if an invalid collection name is used.
        :Parameters:
          - `name`: the name of the collection to get
        """
        if name.startswith('_'):
            raise AttributeError(
                "Database has no attribute %r. To access the %s"
                " collection, use database[%r]." % (name, name, name))
        return self.__getitem__(name)

    def __getitem__(self, name):
        """Get a collection of this database by name.
        Raises InvalidName if an invalid collection name is used.
        :Parameters:
          - `name`: the name of the collection to get
        """
        return Collection(self, name)

