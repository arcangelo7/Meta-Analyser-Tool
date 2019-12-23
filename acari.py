# -*- coding: utf-8 -*-
# Copyright (c) 2019, Silvio Peroni <essepuntato@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.
#
#
# This file is just a stub of the particular module that every group should
# implement for making its project work. In fact, all these functions returns None,
# which is not compliant at all with the specifications that have been provided at
# https://comp-think.github.io/2019-2020/slides/14%20-%20Project.html


import csv


def process_metadata(file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader) # It returns a list of ordered dictionaries. It means that it keeps the order of the keys since Python 3.7


def do_get_ids(data, str_value, field_set):
    return None


def do_get_by_id(data, id, field_set=None):
    items = set()
    for line in data:
        if field_set is not None:
            for field in field_set:
                if id in line[field]:
                    items.add(line[field])
        else:
            for key, value in line.items():
                if id in value:
                    items.add(value)
    return items



def do_filter(data, field_value_list):
    return None


def do_coauthor_graph(data, author_id, level):
    return None


def do_author_network(data):
    return None


def do_retrieve_tree_of_venues(data, no_ids):
    return None

