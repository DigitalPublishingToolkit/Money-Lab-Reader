#!/bin/sh

in=$1
out=`basename $in .docx`.md
pandoc -f docx -t markdown --atx-headers --extract-media=media  --template essay.md.template $in -o $out
echo $out

