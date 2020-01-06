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
from anytree import Node, search
import re
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from itertools import product


def process_metadata(file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader) # It returns a list of ordered dictionaries. It means that it keeps the order of the keys since Python 3.7


def do_get_match (my_regex, my_dict, retrieve_keys):
    output_lst = set()
    for key in retrieve_keys:
        match_lst = re.findall(r'\b' + my_regex + r'\b(?:[^;]*?\[(.*?)\])?;?', my_dict[key], re.IGNORECASE)
        if len(match_lst) > 0:
            output_lst.update(my_dict.get('id').split('; '))
            for match in match_lst:
                if match != '':
                    output_lst.update(match.split('; '))
    return output_lst


def do_get_ids(data, str_value, field_set):
    items = set()
    regex = re.sub(r'\\\*', r'.*?', re.escape(str_value))
    if field_set is None:
        field_set = data.keys()
    for line in data:
        id_lst = do_get_match(regex, line, field_set)
        items.update(id_lst)
    return items


def do_get_by_id(data, id, field_set):
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


def do_get_str(my_regex, my_dict, retrieve_keys):
    for key in retrieve_keys:
        match_lst = re.findall(r'\b' + my_regex + r'\b', my_dict.get(key), re.IGNORECASE)
        if len(match_lst) != 0:
            output_string = my_dict['author'] + ' (' + my_dict['pub_date'] + '). ' + my_dict['title'] + '. ' + my_dict['venue']
            output_string = re.sub(r'\s\[.*?\]', r'', output_string)
            return output_string
    return None


def do_filter(data, field_value_list):
    regex = re.sub(r'\\\*', r'.*?', re.escape(field_value_list[1]))
    items = []
    if field_value_list[0] != '':
        field_set = {field_value_list[0]}
    else:
        field_set = data[0].keys()
    for line in data:
        txt_rep = do_get_str(regex, line, field_set)
        items.append(txt_rep)
    return items


def find_authors_recursively(data, authors_to_visit, visited_authors, dictionary, level):
    if level == 0:
        return dictionary

    level_coauthors = set()
    while len(authors_to_visit) > 0:
        author_to_visit = authors_to_visit.popleft()
        author_coauthors = set()
        for line in data:
            if author_to_visit.lower() in line["author"].lower():
                authors_and_ids = [(name[0] + name[1]).strip() for name in re.findall(r'([^;\[]+)(\[.*?\])?;?', line["author"])]
                is_an_id = re.findall('[^;]+' + re.escape(author_to_visit) + ']', line["author"])
                author = is_an_id[0].strip() if is_an_id else author_to_visit
                visited_authors.add(author)
                coauthors_names = {name.strip() for name in authors_and_ids if name.lower() != author.lower()}
                author_coauthors.update(coauthors_names)
                level_coauthors.update(coauthors_names)
        dictionary[author] = author_coauthors

    for coauthor in level_coauthors:
        if coauthor not in visited_authors:
            authors_to_visit.append(coauthor)

    level -= 1
    return find_authors_recursively(data, authors_to_visit, visited_authors, dictionary, level)
    # Bug: it doesn't merge authors with the same id but different string


def do_coauthor_graph(data, string_to_search, level):
    authors_to_visit = deque()
    authors_to_visit.append(string_to_search)
    visited_authors = set()
    final_dict = find_authors_recursively(data, authors_to_visit, visited_authors, dict(), level)
    coauthor_graph = nx.from_dict_of_lists(final_dict, create_using=nx.Graph)
    return coauthor_graph


def do_author_network(mdata):
    coauthgraph = nx.MultiGraph()
    for row in mdata:
        auths = {aut.strip() for aut in row['author'].split(';')}
        for aut1, aut2 in product(auths,auths):
            if not coauthgraph.has_node(aut1):
                coauthgraph.add_node(aut1)
            if not coauthgraph.has_node(aut2):
                coauthgraph.add_node(aut2)
            if(aut1 != aut2) and not coauthgraph.has_edge(aut1, aut2):
                coauthgraph.add_edge(aut1,aut2)
    return coauthgraph


def build_tree(root, line, venues_found):
    global existing_volume
    if line["venue"] not in venues_found and line["venue"] != "":
        venues_found.add(line["venue"])
        venue_node = Node(line["venue"], root)
        if line["volume"] != "":
            volume_node = Node(line["volume"], venue_node)
        if line["issue"] != "":
            Node(line["issue"], volume_node)
    else:
        venue_node = search.find(root, lambda node: node.name == line["venue"], maxlevel=2)
        if venue_node is not None:
            existing_volume = search.findall(venue_node, lambda node: node.name == line["volume"], maxlevel=3)
        if not existing_volume and line["volume"] != "":
            volume_node = Node(line["volume"], venue_node)
            if line["issue"] != "":
                Node(line["issue"], volume_node)


def do_retrieve_tree_of_venues(data, no_ids):
    root = Node("venues")
    venues_found = set()
    for line in data:
        if no_ids is None:
            build_tree(root, line, venues_found)
        else:
            for id in no_ids:
                if id not in line["venue"]:
                    build_tree(root, line, venues_found)
    return root


