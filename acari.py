import csv


def process_metadata(metadata_file_path):
    with open(metadata_file_path, 'r', encoding="UTF-8") as csvfile:
        reader = csv.reader(csvfile)  # each row of the file is a list
        return reader


def do_get_ids(data, str_value, field_set):
    pass


def do_get_by_id(data, id, field_set):
    pass


def do_filter(data, field_value_list):
    pass


def do_coauthor_graph(data, author_id, level):
    pass


def do_author_network(data):
    pass


def do_retrieve_tree_of_venues(data, no_ids):
    pass