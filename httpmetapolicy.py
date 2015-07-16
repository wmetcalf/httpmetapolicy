#!/bin/sh
from glob import glob
from optparse import OptionParser
import re
import sys
import os

parser = OptionParser()
parser.add_option("-i", dest="input_target", type="string", help="rules files to append http metadata service tags and stick in a file standard glob stuff supported")
parser.add_option("-o", dest="output_target", type="string", help="dir to dump new rules files")
threshold_ar = []

(options, args) = parser.parse_args()
if options == []:
   print parser.print_help()
   sys.exit(-1)
if not options.input_target or options.input_target == "":
   print parser.print_help()
   sys.exit(-1)
if not options.output_target or options.output_target == "":
   print parser.print_help()
   sys.exit(-1)

try:
    if not os.path.exists(options.output_target):
        os.makedirs(options.output_target)
except:
    print("failed to create directory %s bailing" % (options.output_target))
    
rules_files = glob(options.input_target)
rules_files.sort()
for e in rules_files:
    print "working on %s " % (e)
    rules_file_tmp_ar = []
    lines = open(e,"rb").readlines()
    for l in lines:
#        if re.search(r"(?:http_(?:raw_(?:cookie|header|uri)|c(?:lient_body|ookie)|stat_(?:code|msg)|encode|header|method|uri)|(?:pcre:[\x22]\\\/.+?\\\/[A-Za-z]*?[UIPHDMCKSY][A-Za-z]*?[\x22]|\s\$HTTP_PORTS.+?file_data)\x3b|uri(?:content|len))",l) != None and "metadata: service http;" not in l:
        if re.search(r"(?:http_(?:raw_(?:cookie|header|uri)|c(?:lient_body|ookie)|stat_(?:code|msg)|encode|header|method|uri)|(?:pcre:[\x22]\\\/.+?\\\/[A-Za-z]*?[UIPHDMCKSY][A-Za-z]*?[\x22]|\s\$HTTP_PORTS.+?file_data);|ET(?:PRO)? (?:WEB_S(?:PECIFIC_APPS|ERVER)|ACTIVEX)|\s*?$HTTP_PORTS.*?ET(?:PRO)? WEB_CLIENT|uri(?:content|len))",l) != None and "metadata: service http;" not in l:
            rules_file_tmp_ar.append(re.sub(r"\x29\n?$","\x20metadata\x3a\x20service http\x3b\x29",l))
        else:
            rules_file_tmp_ar.append(l)

    new_rule_file = "%s/%s" % (options.output_target,os.path.basename(e))
    try:
        f = open(new_rule_file,"wb")
    except Exception as ferr:
        print "failed to open new output file: %s error: %s" % (new_rule_file,ferr)
        sys.exit(1)
 
    for l in rules_file_tmp_ar:
        if "\n" in l:
            f.write(l)
        else:
            f.write(l + '\n')
    f.close()

print "Done: Your so http meta....\n"             
