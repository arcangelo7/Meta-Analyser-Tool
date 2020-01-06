import csv
import re

master_of_regex = r'([^;\[]+)(\[.*?\])?;?'
authorsinitials = '([\w][^\s,]*)(?:[,\s]+([A-Z])[^\s\.\-]*(?:[\.\-\s]+([A-Z])[^\.\s\-]*)*)?'

with open('metadata_sample.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)

authors = list()
for line in data:
    authors.append(line['author'])

authors_list = list()
for author in authors:
    x = re.findall(r'([^;\[]+)(\[.*?\])?;?', author)
    authors_list.extend(x)
print(authors_list[0:10])

authors_name = list()
for authors_tuple in authors_list:
    authors_name.append(authors_tuple[0])

test_list = authors_name[0:100]
authors_rep = list()
for author in test_list:
    rep = re.findall('([\w][^\s,]*)(?:[,\s]+([A-Z])[^\s\.\-]*(?:[\.\-\s]+([A-Z])[^\.\s\-]*)*)?', author)
    authors_rep.append(' '.join(rep[0]))

print(authors_rep)


