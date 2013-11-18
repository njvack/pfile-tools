# Part of the pfile-tools package
# Copyright (c) 2012, Board of Regents of the University of Wisconsin
# Written by Nathan Vack <njvack@wisc.edu>
# A library for performing anonymization of GE p-file headers.

from collections import namedtuple

import struct_utils
import logging
logger = logging.getLogger(__name__)

# option_name and description are for the command-line tool
AnonEntry = namedtuple("AnonEntry",
    ["key", "value", "option_name", "description"])

# Note: key and option_name should be unique in the list.
DEFAULT_LIST = [
    AnonEntry("patient_name",     "ANONYMIZED", "name",        "patient name"),
    AnonEntry("patient_id",       "ANONYMIZED", "id",          "patient ID"),
    AnonEntry("patient_name_2",   "ANONYMIZED", "name_2",      "patient name 2"),
    AnonEntry("patient_id_2",     "ANONYMIZED", "id_2",        "patient ID 2"),
    AnonEntry("date_of_birth",    "",           "dateofbirth", "date of birth"),
    AnonEntry("patient_age",      0,            "age",         "age"),
    AnonEntry("patient_weight_g", 0,            "weight",      "weight"),
    AnonEntry("patient_sex",      0,            "sex",         "sex"),
]


class Anonymizer(object):

    def __init__(self, anonymization_list=DEFAULT_LIST):
        """Creates a new Anonymizer.

        Arguments:
        anonymization_list -- a list of objects specifying what attributes
            are to anonymized, and how. Objects must contain "key" and "value"
            properties. Keys are dotted string struct value identifiers.
            See DEFAULT_LIST for examples. Defaults to DEFAULT_LIST.
        """
        self.anonymization_list = anonymization_list

    def anonymize(self, header):
        """Runs through self.anonymization_list and anonymizes the header
        in place.

        Arguments:
        header -- a pfile header. NOTE: This structure will be modified
            in place!
        """
        logger.debug("Working with a %s" % (type(header)))
        for entry in self.anonymization_list:
            if struct_utils.has_struct_value(header, entry.key):
                logger.debug("Setting %s to %s" % (entry.key, entry.value))
                struct_utils.set_struct_value(header, entry.key, entry.value)
            else:
                logger.debug("%s not found in header" % entry.key)
