# Makefile for INC hybrid publications

## Issues:
# * why can't i make icmls before making markdowns ??

alldocx=$(wildcard docx/*.docx)
allmarkdown=$(filter-out md/book.md, $(shell ls md/*.md)) # TODO: add if, so that if no md is present no error: "ls: cannot access md/*.md: No such file or directory"
markdowns_compound=compound_src.md
epub=book.epub
icmls=$(wildcard icml/*.icml)


test: $(allmarkdown)
	echo "start" ; 
	echo $(allmarkdown) ; 
	echo "end" ;

folders:
	mkdir docx/ ; \
	mkdir md/ ; \
	mkdir md/imgs/ ; \
	mkdir icml/ ; \
	mkdir lib/ ;


markdowns:$(alldocx) # convert docx to md
	for i in $(alldocx) ; \
	do md=md/`basename $$i .docx`.md ; \
	pandoc $$i \
	       	--from=docx \
		--to=markdown \
	       	--atx-headers \
		--template=essay.md.template \
		-o $$md ; \
	./scripts/md_unique_footnotes.py $$md ; \
	done



icmls: $(allmarkdown)
	for i in $(allmarkdown) ; \
	do icml=icml/`basename $$i .md`.icml ; \
	./scripts/md_stripmetada.py $$i > md/tmp.md ; \
	pandoc md/tmp.md \
		--from=markdown \
		--to=icml \
		--self-contained \
		-o $$icml ; \
	done



book.md: clean $(allmarkdown)
	for i in $(allmarkdown) ; \
	do ./scripts/md_stripmetada.py $$i >> md/book.md ; \
	done



book.epub: clean $(allmarkdown) book.md epub/metadata.xml epub/styles.epub.css epub/cover.png
	cd md && pandoc \
		--from markdown \
		--to epub3 \
		--self-contained \
		--epub-chapter-level=1 \
		--epub-stylesheet=../epub/styles.epub.css \
		--epub-cover-image=../epub/cover.png \
		--epub-metadata=../epub/metadata.xml \
		--default-image-extension png \
		--epub-embed-font=../lib/open-sans-v13-latin-300.woff \
		--epub-embed-font=../lib/open-sans-v13-latin-300.ttf \
		--epub-embed-font=../lib/open-sans-v13-latin-300italic.woff \
		--epub-embed-font=../lib/open-sans-v13-latin-300italic.ttf \
		--epub-embed-font=../lib/open-sans-v13-latin-700.woff \
		--epub-embed-font=../lib/open-sans-v13-latin-700.ttf \
		--epub-embed-font=../lib/open-sans-v13-latin-700italic.woff \
		--epub-embed-font=../lib/open-sans-v13-latin-700italic.ttf \
		-o ../book.epub \
		book.md ; \
	cd ../ ; \
	python scripts/epub_process.py book.epub ;

#		--epub-embed-font=lib/UbuntuMono-B.ttf \

clean:  # remove outputs
	rm -f md/book.md  
	rm -f book.epub 
	rm -f *~ */*~  #emacs files
# improve rule: rm if file exits
