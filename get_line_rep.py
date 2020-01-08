import csv
import re

with open('metadata_sample.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)

def do_get_line_rep(line):
    authors_rep = []
    authors_collection = re.findall(r'([^;\[]+)(\[.*?\])?;?', line['author'])
    for author in authors_collection:
        author_name = author[0]
        family_n, given_n = author_name.split(',')
        given_init = re.findall(r'\b[A-Z]', given_n)
        init = "".join(given_init)
        name_rep = family_n + " " + init
        authors_rep.append(name_rep)
    line_rep = ", ".join(authors_rep) + ' (' + line['pub_date'] + '). ' + line['title'] + '. ' + line['venue']
    line_rep = re.sub(r'\s\[.*?\]', r'', line_rep)
    return line_rep

for paper in data[0:15]:
    print(do_get_line_rep(paper))