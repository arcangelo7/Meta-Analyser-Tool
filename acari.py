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


def do_get_ids(data, str_value, field_set=None):
    items = set()
    regex = re.escape(str_value)
    ##escape toglie eventuali caratteri speciali che hanno un significato per re
    if '*' in str_value:
        regex = re.sub(r'\\\*', r'.*?', regex)
        ##ogni volta che c'è un asterisco nella stringa trasformalo in un quantificatore pigro
        ##che segue il simbolo speciale \.
    for line in data:
        if field_set is not None:
            for field in field_set:
                match_lst = re.findall(r'(\b' + regex + r'\b)(?:\s.*?\[(.*?)\])?', line[field],
                                       re.IGNORECASE)
                ##crea una lista di tuple (stringa, id1;1d2;etc.)
                if len(match_lst) > 0:
                    if field == 'title':
                        items.add(line['id'])
                        ##se quello matchato è il titolo
                        ##aggiungi all'insieme line[id]
                    else:
                        for match in match_lst:
                            if match[1] != '':
                                items.add(match[1])
                        ##se c'è un match, fornisci il secondo valore nella tupla
                        ##se questo non è una stringa vuota(= nessun id1;id2;etc. trovato)

        else:
            ##fa la stessa cosa ma iterando su ogni coppia key-value dei dizionari nella lista
            for key, value in line.items():
                match_lst = re.findall(r'(\b' + regex + r'\b)(?:\s.*?\[(.*?)\])?', line[key],
                                       re.IGNORECASE)
                if len(match_lst) > 0:
                    if key == 'title':
                        items.add(line['id'])
                    else:
                        for match in match_lst:
                            if match[1] != '':
                                items.add(match[1])
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



def do_filter(data, field_value_list):
    regex = re.sub(r'\\\*', r'.*?', re.escape(field_value_list[1]))
    for line in data:
        if field_value_list[0] != '':
            match_lst = re.findall(r'\b' + regex + r'\b', line[field_value_list[0]], re.IGNORECASE)
            if len(match_lst) != 0:
                output_string = line['author'] + ' (' + line['pub_date'] + '). ' + line['title'] + '. ' + line['venue']
                output_string = re.sub(r'\s\[.*?\]', r'', output_string)
                print(output_string)
        else:
            for key in line.keys():
                match_lst = re.findall(r'\b' + regex + r'\b', line[key], re.IGNORECASE)
                if len(match_lst) != 0:
                    output_string = line['author'] + ' (' + line['pub_date'] + '). ' + line['title'] + '. ' + line[
                        'venue']
                    output_string = re.sub(r'\s\[.*?\]', r'', output_string)
                    print(output_string)


def find_authors_recursively(data, string_to_search, dictionary, level):
    if level == 0 or len(string_to_search) == 0:
        return dictionary

    coauthors = set()
    for item in string_to_search:
        if item not in dictionary:
            is_an_id = True if ":" in item else False
            author_name = item.split('[')[1].split(']')[0] if is_an_id else item
            for line in data:
                if author_name in line["author"]:
                    author = line["author"].split(f"[{author_name}")[0].split(";")[-1].strip() if is_an_id else author_name
                    no_ids = re.sub("\[.*?\]", "", line["author"])
                    coauthors_names = {name.strip() for name in no_ids.split(";") if author not in name}
                    coauthors.update(coauthors_names)
            dictionary[author] = coauthors

    string_to_search.extend(coauthors)
    level -= 1
    return find_authors_recursively(data, string_to_search, dictionary, level)
    # Bug: it doesn't merge authors with the same id but different string


def do_coauthor_graph(data, string_to_search, level):
    authors_to_visit = deque()
    authors_to_visit.append(string_to_search)
    final_dict = find_authors_recursively(data, authors_to_visit, dict(), level)
    coauthor_graph = nx.from_dict_of_lists(final_dict, create_using=nx.MultiGraph)
    return coauthor_graph


def do_author_network(mdata):
    coauthgraph = nx.Graph()
    for row in mdata:
        if (row['author']):
            auths = row['author'].split(';')
            auths = [aut.strip() for aut in auths]
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


