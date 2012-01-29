#!/usr/bin/python

# Basic table generator from a CSV file
# usage: python tablegen.py test.csv

import csv
import pytex
import sys

def main(csvfile):
    reader = csv.reader(open(csvfile, 'rb'))
    rows = [reader.next()]
    for row in reader:
        if len(row) != len(rows[0]):
            raise ValueException("All row lengths must be the same")
        rows.append(row)
    table = pytex.latex.LaTeXTabular("tabular", "c"*len(rows[0]))
    for row in rows:
        table.addObj(pytex.TeXRow(row))
    table.objs[-1].end = ""
    print pytex.latex.simple_latex_document(table)

if __name__ == "__main__":
    main(sys.argv[1])
