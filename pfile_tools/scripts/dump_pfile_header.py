#!/usr/bin/env python
# Part of the pfile-tools package
# Copyright (c) 2012, Board of Regents of the University of Wisconsin
# Written by Nathan Vack <njvack@wisc.edu>
#
# An executable script to dump the data from a p-file.

import sys
import optparse
import csv

import pfile_tools
from pfile_tools import headers, struct_utils


def build_option_parser():
    revision_opt_strs = ", ".join([str(r) for r in headers.known_revisions()])
    p = optparse.OptionParser(
        usage="usage: %prog [OPTIONS] pfile",
        description="Dumps header information from a GE P-file",
        version="%prog "+pfile_tools.VERSION)
    p.add_option(
        "-r", "--revision", action="store", choices=headers.known_revisions(),
        help="Force a header revision (available: %s)" % revision_opt_strs)
    p.add_option(
        "--offsets", action="store_true", default=False, dest="offsets",
        help="Show offsets to data elements")
    p.add_option(
        "--sizes", action="store_true", default=False, dest="sizes",
        help="Show data element sizes")
    p.add_option(
        "--show-padding", action="store_true", default=False, dest="padding",
        help="Print unknown 'padding' elements")
    p.add_option(
        "--separator", action="store", default="\t",
        help="Output field separator (default: \\t)")
    return p


def header_columns(opts):
    headers = ["field", "value"]
    if opts.offsets:
        headers.append("offset")
    if opts.sizes:
        headers.append("size")
    return headers


def to_list(info, opts):
    out = [info.label, str(info.value)]
    if opts.offsets:
        out.append("%#x" % (info.offset))
    if opts.sizes:
        out.append(str(info.size))
    return out


def main():
    parser = build_option_parser()
    opts, args = parser.parse_args()
    if len(args) < 1:
        parser.error("Must specify a p-file.")
    rev = opts.revision
    ph = headers.Pfile.from_file(args[0], force_revision=rev)
    dumped = struct_utils.dump_struct(ph.header)
    writer = csv.writer(sys.stdout, delimiter=opts.separator)
    writer.writerow(header_columns(opts))
    for info in dumped:
        if (info.label.find("pad") == 0) and not opts.padding:
            continue
        writer.writerow(to_list(info, opts))


if __name__ == "__main__":
    main()
