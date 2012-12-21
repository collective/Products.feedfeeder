#! /bin/sh
i18ndude rebuild-pot --pot locales/feedfeeder.pot --create feedfeeder --merge locales/manual.pot .

for po in locales/*/LC_MESSAGES/feedfeeder.po; do
    i18ndude sync --pot locales/feedfeeder.pot $po
done

# Search for plone domain entries specifically in the profiles.
i18ndude rebuild-pot --pot locales/plone.pot --create plone profiles/

# Synchronise the plone-*.po files with the plone.pot
for po in locales/*/LC_MESSAGES/plone.po; do
    i18ndude sync --pot locales/plone.pot $po
done

# Run checks
for po in $(find . -name '*po'); do
    msgfmt -c $po;
done
rm messages.mo
