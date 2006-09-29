#!/bin/sh
# I'm assuming an archgenxml that's setup.py-installed, currently
# that's in a special branch. Well, this at least gives an idea how to
# run it.
#
# Alternatively, just put a symlink called 'archgenxml' in some bin
# directory that links to ...../ArchGenXML/ArchGenXML.py

MODELDIR=feedfeeder/model

cd ..
archgenxml --cfg=${MODELDIR}/generate.conf ${MODELDIR}/feedfeeder.zuml
