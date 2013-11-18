#!/usr/bin/env python
# Part of the pfile-tools package
# Copyright (c) 2012, Board of Regents of the University of Wisconsin
# Written by Nathan Vack <njvack@wisc.edu>
#
# A script to strip the identifying information from a GE p-file.

import optparse
import sys
import shutil
import logging
logger = logging.getLogger(__name__)

import pfile_tools
from pfile_tools import headers, anonymizer


def build_option_parser(anonymization_list):
    revision_opt_strs = ", ".join([str(r) for r in headers.known_revisions()])
    p = optparse.OptionParser(
        usage="usage: %prog [OPTIONS] pfile pfile_out",
        description="Removes personally-identifying information from a GE P-file",
        version="%prog "+pfile_tools.VERSION)
    p.add_option(
        "-r", "--revision", action="store", choices=headers.known_revisions(),
        help="Force a header revision (available: %s)" % revision_opt_strs)
    p.add_option("--inplace", action="store_true",
        help="Edit file in-place. Ignores pfile_out.")
    p.add_option("-v", "--verbose", action="store_true",
        help="Print lots of extra debugging.")
    group = optparse.OptionGroup(p, "Anonymization options")
    for entry in anonymization_list:
        group.add_option(
            "--"+entry.option_name, action="store", type="choice",
            choices=["yes", "no"], default="yes", metavar="yes/no",
            help="Set %s to %r (yes)" % (entry.description, entry.value))
    p.add_option_group(group)
    return p


def filter_anonymization_list(l, options):
    filtered = []
    for entry in l:
        opt_val = getattr(options, entry.option_name)
        if opt_val == "yes":
            logger.debug("Anonymizing %s" % entry.option_name)
            filtered.append(entry)
        else:
            logger.debug("Not anonymizing %s" % entry.option_name)
    return filtered


def setup_logger(options):
    log_level = logging.ERROR
    if options.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)


def setup_files(options, args):
    pfile_in = args[0]
    if not options.inplace:
        pfile_out = args[1]
    else:
        logger.debug("Editing %s in place" % (pfile_in))
        pfile_out = pfile_in
    return (pfile_in, pfile_out)


def read_pfile(pfile_in, options):
    rev = options.revision
    logger.debug("Reading %s, revision %s" % (pfile_in, rev))
    return headers.Pfile.from_file(pfile_in, force_revision=rev)


def write_header(f, ph):
    """
    Write a pfle header to a file (file or filename)
    """
    if hasattr(f, 'seek'):
        return _write_header_inner(f, ph)
    else:
        with open(f, "r+b") as infile:
            return _write_header_inner(infile, ph)


def _write_header_inner(f, ph):
    f.write(ph)


def main():
    parser = build_option_parser(anonymizer.DEFAULT_LIST)
    (options, args) = parser.parse_args()
    if len(args) < 2 and not options.inplace:
        parser.error("Both pfile_in and pfile_out are required")
    if len(args) < 1:
        parser.error("pfile_in is required")
    setup_logger(options)
    pfile_in, pfile_out = setup_files(options, args)
    pfile = read_pfile(pfile_in, options)

    anon_list = filter_anonymization_list(anonymizer.DEFAULT_LIST, options)
    a = anonymizer.Anonymizer(anon_list)
    a.anonymize(pfile.header)

    if not options.inplace:
        logger.debug("Copying %s to %s" % (pfile_in, pfile_out))
        shutil.copyfile(pfile_in, pfile_out)
    write_header(pfile_out, pfile.header)


if __name__ == "__main__":
    main()
