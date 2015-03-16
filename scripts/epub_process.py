#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys, zipfile, os, shutil, glob, textwrap, re
from os.path import join
from xml.etree import ElementTree as ET
import html5lib
import argparse
<<<<<<< Updated upstream
=======
#from django.utils.html import urlize

>>>>>>> Stashed changes
"""
(C) 2014 Andre Castro

License: [GPL3](http://www.gnu.org/copyleft/gpl.html)
"""

"""
Script enhances the EPUB created from from Pandoc conversion to EPUB3, namely:

* Removes <sub> from footnotes, since these interferes with the iPad response; relies on CSS instead 
* Replaces back arrows - '↩' - with work 'back'
* makes cover linear inside content.opf <spine>
"""

"""
Note: Script needs Django installed https://code.djangoproject.com/wiki/Distributions
to run urlize def (now commented)


"""

filename = sys.argv[1]
# unzip ePub
fh = open(str(filename), 'rb')
z = zipfile.ZipFile(fh)
for name in z.namelist():
    outpath = "temp"
    z.extract(name, outpath)
fh.close()
temp_dir="temp/"
os.remove(temp_dir+'mimetype') # delete mimetype (will be added later with epub.writestr)

<<<<<<< Updated upstream

def rm_captioncode(tree, element):
    for parag in tree.findall(element):        
        caption = parag.findall('.//code[@class="caption"]')
        if caption:
            caption = caption[0]
            parag.remove(caption)

            
=======
>>>>>>> Stashed changes
def fn_rm_sup(tree, element): # Removes Footnotes <sub>
    for fn in tree.findall(element):
        for child in list(fn):
            if child.tag == 'sup':                
                number = child.text
                fn.remove(child)
                fn.text=number

def replace_fn_links(tree, element): #replace back arrows with work "back"
<<<<<<< Updated upstream
    for parag in tree.findall(element):
        anchors = parag.findall("./a")
        for anchor in anchors:
            if '#fn'in anchor.get('href'):
                anchor.text = 'back'
=======
    for tag in tree.findall(element):
        if tag.text is not None:
            text=(tag.text).encode('utf-8')
            if text == '↩':#'&#8617;':
                tag.text = 'back'
>>>>>>> Stashed changes

   
def spine(filename): # makes cover & title page linear is <spine>
    tree = ET.parse(filename)
    ET.register_namespace('epub', 'http://www.idpf.org/2007/ops')
    spine = tree.find('.//{http://www.idpf.org/2007/opf}spine')
    manifest = tree.find('.//{http://www.idpf.org/2007/opf}manifest')
    for child in spine.getchildren():
        if child.attrib['idref'] == 'cover_xhtml'or child.attrib['idref'] == 'title_page_xhtml':            
<<<<<<< Updated upstream

            #(child.attrib).pop("linear")
            child.attrib['linear'] = 'yes'
=======
            (child.attrib).pop("linear")
            #child.attrib['linear'] = 'yes'
>>>>>>> Stashed changes
    return tree


def save_html(content_dir, content_file, tree ):
    doctype = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n'
    html = ET.tostring(tree,  encoding='utf-8', method='xml')
    html = doctype + html
    xhtml_file = open(content_dir + content_file, "w") 
    xhtml_file.write(html) 
    xhtml_file.close()


temp_ls=os.listdir("temp/")
temp_ls.sort()

<<<<<<< Updated upstream
=======
'''
# URLIZE DEF - NEEDS DJANGO Installed
url_regex = '.*http[s]?://.*' # any url                 
def urlize_text(tree, element):
    for tag in tree.findall(element):
        if tag.text is not None:
            text=(tag.text).encode('utf-8')
            text=urlize(text, nofollow=False)
'''
>>>>>>> Stashed changes
            
for f in temp_ls: #loop epub contained files     
    if f[:2]=='ch' and f[-6:]==".xhtml": # all ch*.xhtml        
        filename = "temp/"+f
        xhtml = open(filename, "r") 
        xhtml_parsed = html5lib.parse(xhtml, namespaceHTMLElements=False)
        fn_rm_sup(xhtml_parsed, './/a[@class="footnoteRef"]')
<<<<<<< Updated upstream
        replace_fn_links(xhtml_parsed, './/section[@class="footnotes"]/ol/li/p')        
        rm_captioncode(xhtml_parsed, './/p')
=======
        replace_fn_links(xhtml_parsed, './/li/p/a')        
#        urlize_text(xhtml_parsed, './/p')
#        urlize_text(xhtml_parsed, './/li')
>>>>>>> Stashed changes
        
        save_html(
            content_dir=temp_dir,
            content_file=f,
            tree=xhtml_parsed )
        
    elif f == 'content.opf': # the opf
        filename = "temp/"+f
        xhtml = open("temp/"+f, "r")
        tree = spine(filename)
        ET.register_namespace('', 'http://www.idpf.org/2007/opf')
        tree.write(filename, encoding='utf-8', xml_declaration='True' )
        
# Step 3: zip epub
epub = zipfile.ZipFile("book.epub", "w")
epub.writestr("mimetype", "application/epub+zip")
temp_dir = "temp"

def fileList(source):
    matches = []
    for root, dirnames, filenames in os.walk(source):
        for filename in filenames:
            matches.append(os.path.join(root, filename))
    return matches

dirlist=fileList(temp_dir)

for name in dirlist:
    path = name[5:] # removes 'temp/'
    epub.write(name, path, zipfile.ZIP_DEFLATED)

<<<<<<< Updated upstream
    
=======
>>>>>>> Stashed changes
epub.close()

# Step 4: clean up: rm temp zipname
shutil.rmtree(temp_dir)

print
print "** EPUB (processed) was generated without errors **"

