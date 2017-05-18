#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# File       : monexcrunch.py
# Author     : Steffen Eichhorn (mail@indubio.org)
# Copyright  : Copyright Steffen Eichhorn
# Licence    : MIT
# Date       : 2013-09-26
# Last Update: 2017-05-18
# Comment:
# convert m1 export file to csv

import sys
from optparse import OptionParser
import io
import csv

def main(options):
    """main program"""
    inblock_counter = 0
    global_counter = 0
    csvout = []
    event = {}
    first_row_out = True
    with io.open (options.infilename, encoding = options.codecinfile) as m1_file:
        for line in m1_file:
            line = line.rstrip()
            global_counter += 1
            inblock_counter += 1
            if global_counter > 3:
                #line = line.rstrip()
                if line[0:5] == '=====':
                    break
                if line[0:5] == '-----':
                    inblock_counter = 0
                if inblock_counter == 1:
                    # PatientID line
                    patID = line[13:]
                if inblock_counter == 2:
                    # PatientData line
                    dummy1 = line.split(';')
                    dummy2 = dummy1[1].split(',')
                    patName = dummy1[0][1:]
                    patBirthdate = dummy2[0][3:]
                if inblock_counter > 2:
                    # wenn durch rstrip die Zeile keine Zeichen enthält wird der line string wieder aufgefüllt
                    if len(line) < 28:
                        line = " " * 28
                    newline = False
                    if line[0:8] != "        ":
                        line_date = line[0:8]
                        newline = True
                    if line[9:12] != "   ":
                        line_signer = line[9:12]
                        newline = True
                    if line[15:18] != "   ":
                        line_surgery = line[15:18]
                        newline = True
                    if line[23:26] != "   ":
                        line_ctyp = line[23:26].rstrip()
                        newline = True
                    line_content = line[28:]
                    if newline:
                        if first_row_out:
                            first_row_out = False
                        else:
                            csvout.append(event)
                        newline = False
                        event = {
                            'date'         : line_date,
                            'patID'        : patID,
                            'patName'      : patName,
                            'patBirthdate' : patBirthdate,
                            'signer'       : line_signer,
                            'surgery'      : line_surgery,
                            'ctyp'         : line_ctyp,
                            'content'      : line_content
                            }
                    else:
                        event['content'] += line_content

    fieldnames = ['date', 'patID', 'patName', 'patBirthdate', 'signer', 'surgery', 'ctyp', 'content']
    with io.open(options.outfilename, 'wb',) as out_file:
        #csvwriter = csv.DictWriter(out_file, fieldnames, dialect = "excel")
        csvwriter = csv.DictWriter(out_file, fieldnames, delimiter = ',', quotechar='"')
        csvwriter.writeheader()
        for row in csvout:
            row = {key.encode('utf8'): value.encode('utf8') for key, value in row.items()}
            csvwriter.writerow(row)

if __name__ == '__main__':
    parser = OptionParser("m1_2_csv.py [Optionen]")
    parser.add_option(
        "-i",
        "--infile",
        help = "input filename",
        dest = "infilename")
    parser.add_option(
        "-o",
        "--outfile",
        help = "output filename",
        dest = "outfilename")
    parser.add_option(
        "",
        "--codecin",
        help = "codec input filename [default: %default]",
        dest = "codecinfile",
        default = "cp1252")
    (progoptionen, progargs) = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        exit()
    else:
        main(progoptionen)
