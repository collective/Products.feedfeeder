#!/bin/sh
PRODUCTNAME=feedfeeder
I18NDOMAIN=$PRODUCTNAME

# Synchronise the .pot with the templates.
# Also merge it with handmade.pot, which includes some items
# that are not picked up by i18ndude
i18ndude rebuild-pot --pot i18n/${PRODUCTNAME}.pot --create ${I18NDOMAIN} --merge i18n/handmade.pot skins/${PRODUCTNAME} ./

# Synchronise the resulting .pot with the .po files
i18ndude sync --pot i18n/${PRODUCTNAME}.pot i18n/${PRODUCTNAME}-*.po

# Synchronise the plone-*.po files with the hand-made plone.pot
i18ndude sync --pot i18n/plone.pot i18n/plone-*.po
