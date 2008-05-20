#!/bin/sh
PRODUCTNAME=feedfeeder
I18NDOMAIN=$PRODUCTNAME

# Synchronise the .pot with the templates.
# Also merge it with generated.pot, which includes the items
# from schema.py
i18ndude rebuild-pot --pot i18n/${PRODUCTNAME}.pot --create ${I18NDOMAIN} --merge i18n/generated.pot skins/${PRODUCTNAME}

# Synchronise the resulting .pot with the .po files
i18ndude sync --pot i18n/${PRODUCTNAME}.pot i18n/${PRODUCTNAME}*.po

# Synchronise the plone*.po files with the hand-made plone-PRODUCTNAME.pot
#i18ndude sync --pot i18n/plone-${PRODUCTNAME}.pot i18n/plone*.po
