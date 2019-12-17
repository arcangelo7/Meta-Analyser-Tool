from acari import *

class MetaAnalyserTool(object):
    def __init__(self, metadata_file_path):
        self.data = process_metadata(metadata_file_path)


    def get_ids(self, str_value, field_set):
        return do_get_ids(self.data, str_value, field_set)


    def get_by_id(self, id, field_set):
        return do_get_by_id(self.data, id, field_set)


    def filter(self, field, value):
        return do_filter(self.data, field_value_list)


    def coauthor_graph(self, author_id, level):
        return do_coauthor_graph(self.data, author_id, level)


    def author_network(self):
        return do_author_network(self.data)


    def retrieve_tree_of_venues(self, no_ids):
        return do_retrieve_tree_of_venues(self.data, no_ids)