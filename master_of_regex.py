import csv
import re

master_of_regex = r'([^;\[]+)(\[.*?\])(?:;|$)'
#finds a tuple with tuple[0] = author's name, tuple[1] = id

with open('metadata_sample.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)

authors = list()
for line in data:
    authors.append(line['author'])

authors_list = list()
for author in authors:
    x = re.findall(r'([^;\[]+)(\[.*?\])(?:;|$)', author)
    authors_list.extend(x)
print(authors_list[0:10])

authors_name = list()
for authors_tuple in authors_list:
    authors_name.append(authors_tuple[0])
authors_id = list()
for authors_tuple in authors_list:
    authors_id.append(authors_tuple[1])

print(authors_name)
print(authors_id)