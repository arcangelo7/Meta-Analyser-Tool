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
from collections import deque
from itertools import product, tee


def find_all_ids(cur_entity_ids, all_entity_ids):
    for id in cur_entity_ids:
        new_ids_set = set()
        cur_ids_set = {id.strip() for id in id.split(";")}
        key_to_change = set()
        for found_id, cur_id in product(all_entity_ids, cur_ids_set):
            found_id_list = found_id.split("; ")
            if cur_id in found_id_list:
                new_ids_set.update(found_id_list)
                new_ids_set.update(cur_ids_set)
                key_to_change.add(found_id)

        if len(key_to_change) > 0:
            for key in key_to_change:
                all_entity_ids.remove(key)
            all_entity_ids.add("; ".join(new_ids_set))
        else:
            all_entity_ids.add("; ".join(cur_ids_set))


def add_all_ids(line, all_entity_ids, field, counter):
    name_and_ids = set((name[0] + name[1]).strip() for name in re.findall(r'([^;\[]+)(\[.*?\])?(?:;|$)', line[field]))
    for name_and_id in name_and_ids:
        if "[" in name_and_id:
            ids = re.findall(r'\[(.*?)\](?=;|$)', name_and_id)[0]
            cur_ids_set = {id.strip() for id in ids.split(";")}
            for list_of_keys, cur_id in product(all_entity_ids, cur_ids_set):
                if cur_id in list_of_keys.split("; "):
                    new_line = line[field].replace(ids, list_of_keys)
                    line[field] = new_line
                    break
        else:
            new_line = line[field].replace(name_and_id, name_and_id + " [acarid:" + str(counter[0]) + "]")
            counter[0] += 1
            line[field] = new_line


def process_metadata(file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        it1, it2, it3 = tee(reader, 3)

        all_the_author_ids = set()
        all_the_venue_ids = set()
        all_the_publisher_ids = set()

        for line in it1:
            authors_ids = set(id.strip() for id in re.findall(r'\[(.*?)\](?:;|$)', line["author"]))
            venue_ids = set(id.strip() for id in re.findall(r'\[(.*?)\](?:;|$)', line["venue"]))
            publisher_ids = set(id.strip() for id in re.findall(r'\[(.*?)\](?:;|$)', line["publisher"]))

            find_all_ids(authors_ids, all_the_author_ids)
            find_all_ids(venue_ids, all_the_venue_ids)
            find_all_ids(publisher_ids, all_the_publisher_ids)

        counter = [0] # Must be mutable to change, otherwise it is copied everytime and restarts from zero
        for line in it2:
            add_all_ids(line, all_the_author_ids, "author", counter)
            add_all_ids(line, all_the_venue_ids, "venue", counter)
            add_all_ids(line, all_the_publisher_ids, "publisher", counter)

        # toCSV = list(it3)
        # keys = toCSV[0].keys()
        # with open('ouput.csv', 'w', encoding='utf-8') as output_file:
        #     dict_writer = csv.DictWriter(output_file, keys)
        #     dict_writer.writeheader()
        #     dict_writer.writerows(toCSV)

        return list(it3)


def do_get_id_set (my_regex, my_dict, retrieve_keys):
    output_set = set()
    for key in retrieve_keys:
        if key in my_dict.keys():
            if key in {'author', 'venue', 'publisher'}:
                strings_lst = re.findall(r'([^;\[]+)\[(.*?)\](?:;|$)', my_dict[key])
                for string, ids in strings_lst:
                    matchobj = re.match(my_regex + r'$', string.strip(), re.IGNORECASE)
                    if matchobj:
                        output_set.update([itemid.strip() for itemid in my_dict['id'].split(';')])
                        if 'acari' not in ids:
                            output_set.update([id.strip() for id in ids.split(';')])
            elif key == 'id':
                strings_lst = my_dict[key].split(';')
                for string in strings_lst:
                    matchobj = re.match(my_regex + r'$', string.strip(), re.IGNORECASE)
                    if matchobj:
                        output_set.update([itemid.strip() for itemid in my_dict['id'].split(';')])
            else:
                matchobj = re.match(my_regex + r'$', my_dict[key], re.IGNORECASE)
                if matchobj:
                    output_set.update([itemid.strip() for itemid in my_dict['id'].split(';')])
    return output_set

def do_get_ids(data, str_value, field_set):
    items = set()
    regex = re.sub(r'\\\*', r'.*?', re.escape(str_value))
    if field_set is None or len(field_set) == 0:
        field_set = data[0].keys()
    for line in data:
        id_set = do_get_id_set(regex, line, field_set)
        items.update(id_set)
    return items


def do_get_by_id(data, id, field_set):
    list_of_papers = []
    set_of_reps = set()

    for row in data:
        if field_set is None or len(field_set) == 0:
            for key, value in row.items():
                if id in value:
                    list_of_papers.append(row)
        else:
            for field in field_set:
                if id in row[field]:
                    list_of_papers.append(row)

    for dictionary in list_of_papers:
        set_of_reps.add(do_get_line_rep(dictionary))

    return set_of_reps


def do_get_line_rep(dict):
    authors_rep = []
    authors_collection = re.findall(r'([^;\[]+)\[.*?\](?:;|$)', dict['author'])
    for author in authors_collection:
        if ',' in author:
            family_n_given_n = author.split(',')
            init_lst = re.findall(r'\b[A-Z]', family_n_given_n[1])
            init_str = "".join(init_lst)
            name_rep = family_n_given_n[0].strip() + " " + init_str
            authors_rep.append(name_rep)
        else:
            authors_rep.append(author.strip())
    line_rep = ", ".join(authors_rep) + '. (' + dict['pub_date'] + '). ' + dict['title'] + '. ' + dict['venue']
    line_rep = re.sub(r'\s\[.*?\](?=;|$)', r'', line_rep)
    return line_rep


def recursive_field_search(dict, stack, result=None):
    if len(stack) > 0:
        curr_tuple = stack.pop()
        regex = re.sub(r'\\\*', r'.*?', re.escape(curr_tuple[1]))
        field_to_search = curr_tuple[0]
        if field_to_search not in dict.keys():
            return None
        else:
            no_id_str = re.sub(r'\s\[.*?\](?=;|$)', r'', dict[field_to_search])
            lst_of_strings = no_id_str.split(';')
            for string in lst_of_strings:
                result = re.match(regex + r'$', string.strip(), re.IGNORECASE)
                if result is not None:
                    return recursive_field_search(dict, stack, result)
    else:
        return result


def do_filter(data, field_value_list):
    items = []
    for line in data:
        if field_value_list is not None and len(field_value_list) > 0:
            field_value_stack = deque(field_value_list)
            match = recursive_field_search(line, field_value_stack)
            if match is not None:
                items.append(do_get_line_rep(line))
        else:
            items.append(do_get_line_rep(line))
    return items


def merge_authors(coauthors_names, level_coauthors, dictionary):
    id_regex = '\[.*?\](?=;|$)'
    for level_coauthor in level_coauthors:
        level_coauthor_id = re.search(id_regex, level_coauthor).group()
        coauthors_names = {name if level_coauthor_id not in name else level_coauthor for name in coauthors_names}

    for visited_author, visited_author_coauthors in dictionary.items():
        key_id = re.search(id_regex, visited_author).group()
        coauthors_names = {name if key_id not in name else visited_author for name in coauthors_names}
        for visited_author_coauthor in visited_author_coauthors:
            value_id = re.search(id_regex, visited_author_coauthor).group()
            coauthors_names = {name if value_id not in name else visited_author_coauthor for name in coauthors_names}
    return coauthors_names


def find_authors_recursively(data, authors_to_visit, visited_authors, dictionary, level):
    if level == 0:
        return dictionary

    level_coauthors = set()

    while len(authors_to_visit) > 0:
        author_to_visit = authors_to_visit.popleft()
        author = None
        author_coauthors = set()
        for line in data:
            if author_to_visit in line["author"]:
                authors_and_ids = [(name[0] + name[1]).strip() for name in re.findall(r'([^;\[]+)(\[.*?\])(?:;|$)', line["author"])]
                is_an_id = [(name[0] + name[1]).strip() for name in re.findall(r'([^;\[]+)(\[.*?\])(?:;|$)', line["author"]) if author_to_visit in name[1]]
                author = is_an_id[0] if is_an_id else author_to_visit
                visited_authors.add(author)
                coauthors_names = {name.strip() for name in authors_and_ids if name != author}
                coauthors_names = merge_authors(coauthors_names, level_coauthors, dictionary)
                author_coauthors.update(coauthors_names)
                level_coauthors.update(coauthors_names)
        dictionary[author] = author_coauthors

    for coauthor in level_coauthors:
        if coauthor not in visited_authors:
            authors_to_visit.append(coauthor)

    level -= 1
    return find_authors_recursively(data, authors_to_visit, visited_authors, dictionary, level)


def do_coauthor_graph(data, string_to_search, level):
    authors_to_visit = deque()
    authors_to_visit.append(string_to_search)
    visited_authors = set()
    final_dict = find_authors_recursively(data, authors_to_visit, visited_authors, dict(), level)
    coauthor_graph = nx.from_dict_of_lists(final_dict, create_using=nx.Graph)
    return coauthor_graph


def do_author_network(data):
    coauthgraph = nx.Graph()
    for row in data:
        auths = {"".join(aut).strip() for aut in re.findall(r'([^;\[]+)(\[.*?\])(?:;|$)', row['author'])}
        for aut1, aut2 in product(auths, auths):
            if not coauthgraph.has_node(aut1):
                coauthgraph.add_node(aut1)
            if not coauthgraph.has_node(aut2):
                coauthgraph.add_node(aut2)
            if aut1 != aut2 and not coauthgraph.has_edge(aut1, aut2):
                coauthgraph.add_edge(aut1, aut2)
    return coauthgraph


def build_tree(root, line, cur_id, venues_found):
    if cur_id not in venues_found:
        venues_found.add(cur_id)
        node_name = re.findall(r'([^;\[]+)(?:\[.*?\])(?:;|$)', line["venue"])[0].strip()
        venue_node = Node(node_name, root, id=cur_id)
        if line["volume"] != "":
            volume_node = Node(line["volume"], venue_node)
            if line["issue"] != "":
                Node(line["issue"], volume_node)
    elif cur_id in venues_found:
        venue_node = search.findall_by_attr(root, name="id", value=cur_id, maxlevel=2)[0]
        if venue_node is not None and line["volume"] != "":
            existing_volume = search.findall(venue_node, lambda node: node.name == line["volume"], maxlevel=3)
            if not existing_volume:
                volume_node = Node(line["volume"], venue_node)
                if line["issue"] != "":
                    Node(line["issue"], volume_node)
            elif existing_volume and line["issue"] != "":
                existing_issue = search.findall(existing_volume[0], lambda node: node.name == line["issue"], maxlevel=4)
                if not existing_issue:
                    Node(line["issue"], existing_volume[0])


def do_retrieve_tree_of_venues(data, no_ids):
    root = Node("venues")
    venues_found = set()
    for line in data:
        if line["venue"] != "":
            cur_id = re.findall(r'\[(.*?)\](?=;|$)', line["venue"])[0]
            if no_ids is None or len(no_ids) == 0:
                build_tree(root, line, cur_id, venues_found)
            else:
                if len(no_ids.intersection({id.strip() for id in cur_id.split(";")})) == 0:
                    build_tree(root, line, cur_id, venues_found)
    return root


