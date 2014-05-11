# This program is designed to read in the IPEDS file on higer ed instutution data and 
# return a subset of interest for plotting retention data as a function of 
# tuition and Pell grant per institution.  It can easily be adapted to return other 
# fields as well.
#
#
# Mark Riedsel, April 29, 2014
#
# The information on the fields in the input CSV file is contained in the 
# "Delta Data Dictory 1987_2010.xls"
#

import sys
import argparse
import string
import os
import csv
from decimal import *

getcontext().prec = 1

# Read in the name for the input file and the output file from the command line
parser = argparse.ArgumentParser()
parser.add_argument("filein", help="Type the name of the input text file here")
# parser.add_argument("fileout", help="Type the name of the output file here")
parser.add_argument("yearin", help="Type the year for the data to collect here")
args = parser.parse_args()
yearin = args.yearin
out_name = "delta_" + args.yearin + ".csv"
file_out = open(out_name,'w')

cnt = 0
with open(args.filein,'r') as input_file:
    for line in input_file:
        cnt = cnt + 1
        words = line.split(',')
        if cnt == 1:
            for index in range(len(words)):
                words[index] = words[index].strip('"')
        year = words[1]
        institution = words[5].strip('"')
        city = words[7].strip('"')
        state = words[8].strip('"')
        zipcode = words[9].strip('"')
        insttype = words[12]
        carnegie2000 = words[19]
        enrollment = words[44]
        pellgrants = words[94]
        tuition = words[123]
        gradrate_p4yr = words[282]
        try: 
            if cnt == 1:
                file_out.write(year + "," + institution + "," + city + "," + state + "," + zipcode + "," + insttype + \
                   "," + carnegie2000 + "," + enrollment + "," + pellgrants + "," + tuition + "," + gradrate_p4yr + "\n")
            if cnt > 1 and tuition != ""  \
                       and gradrate_p4yr != "" \
                       and year == yearin \
                       and float(enrollment) >= 800. \
                       and float(gradrate_p4yr) < .999 \
                       and int(insttype) <= 3 :
                if int(insttype) == 1 :
                    insttype = "Public"
                elif int(insttype) == 2 :     
                    insttype = "Private Not-For-Profit"
                elif int(insttype) == 3 :
                    insttype = "Private For-Profit"
                else:
                    print "This should never occur, something is wrong"
                gradrate = str(float(gradrate_p4yr)*100.)
                enrollment = str(int(round(float(enrollment))))
                pellgrants = str(int(round(float(pellgrants))))
                file_out.write(year + "," + institution + "," + city + "," + state + "," + zipcode + "," + insttype + \
                   "," + carnegie2000 + "," + enrollment + "," + pellgrants + "," + tuition + "," + gradrate + "\n")
        except ValueError:
            pass
        finally:
            pass
    file_out.close()
