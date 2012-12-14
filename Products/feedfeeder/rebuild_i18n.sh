#!/bin/sh
PRODUCTNAME=feedfeeder
I18NDOMAIN=$PRODUCTNAME

# Synchronise the .pot with the templates.
i18ndude rebuild-pot --pot i18n/${PRODUCTNAME}.pot --create ${I18NDOMAIN} skins/${PRODUCTNAME} ./

# Synchronise the resulting .pot with the .po files
i18ndude sync --pot i18n/${PRODUCTNAME}.pot i18n/${PRODUCTNAME}-*.po

# Search for plone domain entries specifically in the profiles.
i18ndude rebuild-pot --pot i18n/plone.pot --create plone profiles/

# Synchronise the plone-*.po files with the plone.pot
i18ndude sync --pot i18n/plone.pot i18n/plone-*.po
