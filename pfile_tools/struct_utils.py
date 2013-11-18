# Part of the pfile-tools package
# Copyright (c) 2012, Board of Regents of the University of Wisconsin
# Written by Nathan Vack <njvack@wisc.edu>
# Some utilities for working with ctypes Structures

import ctypes
from collections import namedtuple

StructInfo = namedtuple("StructInfo",
    ["label", "depth", "value", "field_type", "size", "offset"])


def dump_struct(struct, include_structs=False):
    """
    Recursively travels through a ctypes.Structure and returns a list of
    namedtuples, containing label, depth, value, size, and offset.
    If include_structs is true, output will include lines for individual
    structures and their sizes and offsets -- not just non-structure fields.
    """
    output = []
    _dump_struct_rec(struct, output, include_structs)
    return output


def _dump_struct_rec(
    struct, output, include_structs=False, prefix='', depth=0, base_offset=0):
    """
    Internal recursive method for dumping structures.
    Appends to the "output" parameter.
    """
    struct_class = type(struct)
    if include_structs:
        output.append(StructInfo(
            "%s (%s)" % (prefix, struct_class.__name__),
            depth, '', str(struct_class), ctypes.sizeof(struct_class), base_offset))
    for f in struct._fields_:
        name = f[0]
        field_type = f[1]
        field_meta = getattr(struct_class, name)
        field = getattr(struct, name)
        cur_prefix = "%s%s." % (prefix, name)
        field_offset = base_offset + field_meta.offset
        if isinstance(field, ctypes.Structure):
            _dump_struct_rec(field, output, include_structs, cur_prefix,
                depth+1, field_offset)
        else:
            label = prefix+name
            output.append(StructInfo(
                label, depth, field, field_type.__name__, field_meta.size, field_offset))


def set_struct_value(struct, field_name, value):
    """
    Sets a value in a ctypes struct, by dotted struct name
    """
    parts = field_name.split(".")
    sh = struct
    while len(parts) > 1:
        subhead_key = parts[0]
        parts = parts[1:]
        sh = getattr(sh, subhead_key)
    setattr(sh, parts[0], value)


def has_struct_value(struct, field_name):
    parts = field_name.split(".")
    sh = struct
    while len(parts) > 1:
        subhead_key = parts[0]
        parts = parts[1:]
        if not hasattr(sh, subhead_key):
            return False
        sh = getattr(sh, subhead_key)
    return hasattr(sh, field_name)