#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(C) 2015 Andre Castro

License: [GPL3](http://www.gnu.org/copyleft/gpl.html)

"""

"""
CORRECT MARKDOWN HYPERLINKS WITH LOCAL .XML DOCUMENTS AS DESTINATION

e.g.  [http://link.springer.com/chapter/10.1007/978-1-4757-0602-4\_18](styles.xml) -> 
 [http://link.springer.com/chapter/10.1007/978-1-4757-0602-4\_18](http://link.springer.com/chapter/10.1007/978-1-4757-0602-4\_18)

"""

import re, sys, os


input_filename=os.path.abspath(sys.argv[1])

input_file = open(input_filename, "r") # open and parse
input_file_lines = input_file.readlines()
edited_text = ""

url_regex = '.*http[s]?://.*' # any url 
hyper_md_regex = '\[.*\]\(http[s]?://.*\)' # hyperlink in mardown link ()[http...]
monyelab_hyperlinks_regex = '\[(http[s]?://.*)\]\((.*?)\)'
img_regex =  '\!\[.*\]\(.*\)'
edited_text = ''
for line in  input_file_lines:
    line = line.decode("utf-8")

    # search url # if is not already a mardown link
    monyelab_hyperlink = re.search(monyelab_hyperlinks_regex, line)
    if bool(re.search(img_regex, line)) == False and bool(monyelab_hyperlink) == True:
        linkname, url = ( re.findall(monyelab_hyperlinks_regex, line))[0]
        if '.xml'in url:
            match = monyelab_hyperlink.group(0)
            print 'URL:',url
            print 'monyelab_hyperlink', monyelab_hyperlink
            print 'LINE:', line.encode('utf-8')
            print 'match', match

            # action: replace url by link name OR replace whole hyperlink with linkname
            new_line = line.replace(url, linkname)
            print 'new_line', new_line.encode('utf-8')
            edited_text = edited_text + new_line
    else:
        edited_text = edited_text + line


edited_file = open(input_filename, 'w') 
edited_file.write(edited_text.encode("utf-8"))
edited_file.close()

