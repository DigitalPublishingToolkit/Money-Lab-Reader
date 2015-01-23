#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(C) 2015 Andre Castro

License: [GPL3](http://www.gnu.org/copyleft/gpl.html)

"""

"""
REMOVE LITERAL ESCAPTES FROM MARKDOWN hyperlink 
E.G.  [http://link.springer.com/chapter/10.1007/978-1-4757-0602-4\_18](http://link.springer.com/chapter/10.1007/978-1-4757-0602-4\_18)

[http://link.springer.com/chapter/10.1007/978-1-4757-0602-4\_18](http://link.springer.com/chapter/10.1007/978-1-4757-0602-4_18)

\_18 -> _18

"""

import re, sys, os


input_filename=os.path.abspath(sys.argv[1])

input_file = open(input_filename, "r") # open and parse
input_file_lines = input_file.readlines()
edited_text = ""

url_regex = '.*http[s]?://.*' # any url 
hyper_md_regex_under = '\[.*\](\(http[s]?://.*?\\.*?\))' # hyperlink in ma# rdown link ()[http...]
img_regex =  '\!\[.*\]\(.*\)'
edited_text = ''

for line in  input_file_lines:
    line = line.decode("utf-8")

    underscore_hyperlink = re.search(hyper_md_regex_under, line)

    if bool(re.search(img_regex, line)) == False and bool(underscore_hyperlink) == True:
        print line
        found = ( re.findall(hyper_md_regex_under, line))[0]
        print 'group', underscore_hyperlink.group(0)
        found_replacement = found.replace('\_', '_')
        new_line = line.replace(found, found_replacement)
        print 'new_line', new_line
        
    else:
        edited_text = edited_text + line


edited_file = open(input_filename, 'w') 
edited_file.write(edited_text.encode("utf-8"))
edited_file.close()

