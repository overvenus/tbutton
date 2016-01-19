#!/usr/bin/make -f
# -*- makefile -*-

VERSION=0.1
LATESTDIR=indicator-tbutton-$(VERSION)
TEMPLATE=indicator-tbutton-template

update:
	mkdir -m 755 -p $(LATESTDIR)
	cp -r indicator-tbutton-template/debian $(LATESTDIR)
	cp $(TEMPLATE)/Makefile $(LATESTDIR)
	cp $(TEMPLATE)/indicator-tbutton.desktop $(LATESTDIR)/indicator-tbutton.desktop
	cp ../tbutton.py $(LATESTDIR)/indicator-tbutton
	cp ../logow.png $(LATESTDIR)/tbutton-icon.png

pack: update
	tar -cvzf indicator-tbutton-$(VERSION)_$(VERSION).orig.tar.gz $(LATESTDIR)

clean:
	-rm -rf $(LATESTDIR)
	-rm *.tar.gz
	-rm *.deb
	-rm *.dsc
	-rm *.changes

build: pack
	$(MAKE) -C $(LATESTDIR) build
	cp *.deb deb
