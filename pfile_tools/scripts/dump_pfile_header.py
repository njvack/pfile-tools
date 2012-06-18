#!/usr/bin/env python

import sys
import optparse

from pfile_tools import headers, struct_utils

def known_revisions():
    return sorted(headers.REVISIONS().keys())


def build_option_parser():
    revision_opt_strs = ", ".join([str(r) for r in known_revisions()])
    p = optparse.OptionParser(
        usage="usage: %prog [OPTIONS] pfile",
        description="Dumps header information from a GE P-file")
    p.add_option(
        "-r", "--revision", action="store", choices=known_revisions(),
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
    return p


def main():
    parser = build_option_parser()
    opts, args = parser.parse_args()
    if len(args) < 1:
        parser.error("Must specify a p-file.")
    rev = opts.revision
    if rev is not None:
        rev = int(rev)
    ph = headers.Pfile.from_file(args[0], force_revision=rev)
    dumped = struct_utils.dump_struct(ph.header)
    for info in dumped:
        if (info.label.find("pad") == 0) and not opts.padding:
            continue
        s = "%s: %s" % (info.label, info.value)
        if opts.offsets:
            s += " offset: %#x" % (info.offset)
        if opts.sizes:
            s += " size: %s" % (info.size)
        print(s)


if __name__ == "__main__":
    main()