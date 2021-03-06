History of feedfeeder
=====================


3.0.2 (unreleased)
------------------

- Nothing changed yet.


3.0.1 (2016-09-05)
------------------

- Bug fix: really call ``getObjectInfo()`` when checking if an entry was updated.
  This avoids unnecessary updates to ``FeedFeederItems``.
  [tiberiuichim]


3.0.0 (2016-02-22)
------------------

- Compatible with Plone 4.3 and 5.0.  [maurits]

- Removed separate registry profile that was only needed for
  compatibility with Plone 4.1 and lower.  Moved ``registry.xml`` to
  the default profile.  [maurits]

- Disabled CSRF protection on our update/clean feed views.  Otherwise
  you would have to add
  ``?_authenticator=user_specific_authentication_string`` to the urls
  in your cronjobs.  Fixes issue
  https://github.com/collective/Products.feedfeeder/issues/13
  [maurits]

- Use ``main_template/macros/master``, instead of strange old
  ``@@standard-macros/view`` which would show only the core content on
  Plone 5.  [maurits]


2.8 (2015-05-16)
----------------

- Prevent UnicodeEncodeError in logging messages .
  [ulisdd]


2.7 (2014-12-26)
----------------

- Updated Spanish translations.
  [Manuel Gualda Caballero]


2.6 (2014-11-27)
----------------

- Add option to prefix feed link titles using a pipe ``|`` as
  separator (``My place: |http://myplace/feed``)
  [jbofill]


2.5 (2014-01-18)
----------------

- Reindex feed item when setting the description.
  [jbofill]

- Solve `KeyError u'+0000'` in some DateTime objects.  Related to
  https://github.com/collective/Products.feedfeeder/issues/7
  [jbofill]

- Update to beautifulsoup4 and use python's built-in HTML parser.
  [jbofill]


2.4 (2013-11-12)
----------------

- Depend on ``feedparser`` instead of ``FeedParser``.  Issue #6.
  [maurits]


2.3 (2013-11-11)
----------------

- Add maximum size to 10 MB for enclosures.  This avoids downloading
  gigabytes of iso files, for example.
  [jbofill]


2.2 (2013-10-01)
----------------

- Take the title as basis for the uid of an item if both guid and link
  are not found.  They are optional in rss.
  [maurits]

- Update permissions.  Protect updating a feed with the "feedfeeder:
  Update feed" permission.  Protect updating all feeds in a mega
  update with the "feedfeeder: Update all feeds" permission.  We give
  these to the Manager and Site Administrator roles in an upgrade step.
  Fixes https://github.com/collective/Products.feedfeeder/issues/4
  [maurits]


2.1 (2012-12-27)
----------------

- Use locales instead of an i18n directory.
  [maurits]

- Support our criterion in new style collections.  Add new profile for
  this.  Make sure not to fail on Plone 4.0 or 4.1 where this is not
  needed at all.
  [maurits]

- Update feed folder after its creation
  i18n for untranslated strings
  Added div#content in feed folder template
  Fixed tests
  Lots of cleanup (old content type definitions in content/folder.py and content/item.py)
  Removed double for "update feed items" action
  French translations
  [cedricmessiant]

- Source is open in a new page.
  [thomasdesvenain]

- Use png icons.
  Use icon_expr instead of content_icon.
  [thomasdesvenain]

- Support only Plone 4.
  [maurits]


2.0.9 (2012-11-12)
------------------

- Fixed possible TypeError when updating feed items.
  Fixes https://plone.org/products/feedfeeder/issues/42
  [maurits]


2.0.8 (2012-10-14)
------------------

- Moved to https://github.com/collective/Products.feedfeeder
  [maurits]


2.0.7 (2011-12-27)
------------------

- Avoid BadRequest error when an entry has two enclosures with the
  same href; we ignore all subsequent ones.
  Fixes http://plone.org/products/feedfeeder/issues/41
  [maurits]

- Try to avoid possible ExpatError for some feeds.
  Fixes http://plone.org/products/feedfeeder/issues/40
  [maurits]

- Cleaned up our type info, removing some cruft from Plone 2.5.
  Added upgrade step for this.
  [maurits]

- protect against UnicodeDecode errors in getting the UID
  of an entry.
  [vangheem]


2.0.6 (2011-10-03)
------------------

- Guard against links (enclosures) not having a type.
  Fixes http://plone.org/products/feedfeeder/issues/39
  [maurits]


2.0.5 (2011-09-03)
------------------

- Use feed-item.pt on Plone 4, filling the content-core slot, and
  feed-item3.pt on Plone 3, filling the body slot as before.
  Fixes http://plone.org/products/feedfeeder/issues/36
  [maurits]

- Register our own documentbyline viewlet for feed items, which
  displays the feed item author as creator.
  Refs http://plone.org/products/feedfeeder/issues/36
  [Maurits]

- Fixed possible UnicodeDecodeError when updating feed items.
  Refs http://plone.org/products/feedfeeder/issues/37
  [maurits]

- Fixed Plone 4.1 compatibility
  [iElectric]


2.0.4 (2011-03-24)
------------------

- Avoid DeprecationWarning on python2.6 by preferring hashlib over md5
  when available.
  [maurits]

- Do not reindex the feed item when nothing has changed.  Only update
  the objectInfo field when there has been a change.
  Fixes http://plone.org/products/feedfeeder/issues/34
  [maurits]


2.0.3 (2011-01-17)
------------------

- Respect the Plone setting on the 'about' information: only show the
  document byline if the user is logged in or anonymous users are
  allowed to view the about information.
  [markvl]


2.0.2 (2010-12-17)
------------------

- Modified import RSS and added a new field on feed items named
  objectInfo. All feed data will be stored on this field,
  as a python dict.
  Just changing the remote RSS template, you will able to memoize
  additional info without having to modify the feed item schema.
  [dmoro]

- Added an option on feed folder that let you choose to redirect
  automatically to remote resources. If you have modify permissions
  on feed items there will not be any redirect
  [dmoro]

- Added new tests
  [sithmel]


2.0.1 (2010-11-26)
------------------

- Added @@feed-mega-update view so you can update all feed folders at
  once, for example in a clock server.
  [miohtoma]

- Import HTMLParseError from the standard python HTMLParser instead of
  BeautifulSoup.  This makes feedfeeder compatible with BeautifulSoup
  3.0.x again.
  [maurits]


2.0 (2010-07-05)
----------------

- Solve some Plone 4 compatibility issues.
  [sureshvv]

- Ignore unidentifiable entries without id or link, instead of
  throwing an AttributeError.
  Fixes http://plone.org/products/feedfeeder/issues/26
  [maurits]


1.0.1 (2010-04-02)
------------------

- Fix errors when viewing a folder or item on Plone 4, while still
  keeping Plone 2.5 and Plone 3 compatibility.
  Refs http://plone.org/products/feedfeeder/issues/25
  [maurits]


1.0 (2009-12-23)
----------------

- Some summaries are a snippet from the full content, and then they
  can contain broken html; in this case we are now saving the raw
  broken html, parsing it only when possible.
  [lucmult]


1.0rc7 (2009-11-06)
-------------------

- Improved the translations stuffs
  [lucmult]

- Changed the way to translate xml/html entities from summary, now
  using BeautifulSoup. Old way was breaking with some non ascii
  characters.
  [lucmult]

- When setting the text of a feed item during updating, store the
  mimetype as well if it is a supported one.
  Refs http://plone.org/products/feedfeeder/issues/24
  [maurits]


1.0rc6 (2009-09-21)
-------------------

- Bug fix: curly quotes getting mangled when Descriptions are built.
  Fixes http://plone.org/products/feedfeeder/issues/7
  (Merged branch maurits-cleaner-entityrefs-in-description.)
  [maurits]


1.0rc5 (2009-07-02)
-------------------

- Do not add our skin layer to Plone Default and certainly not to
  Plone Tableless, but just to all (*).  [maurits]


1.0rc4 (2009-06-18)
-------------------

- When both the updated and published date of an item is not known,
  take today as the date when first adding it.  When updating, do not
  change the original item.
  Fixes http://plone.org/products/feedfeeder/issues/21
  [maurits]

- Read tags/categories/keywords of feed items and store them on the
  created content item.  No Archetypes field, just a simple getter and
  setter called feed_tags.   Idea: Robin Harms Oredsson.
  [maurits]

- DateTime.SyntaxError is thrown with some very common US
  Daylight Saving zones, such as EDT. We now wrap the DateTime parsing
  of feeds, to try to recognise those zones before politely giving up, using
  maurits' fix, below.
  [russf]

- Catch DateTime.SyntaxError when parsing the updated and published
  dates of an entry and continue with the next entry.
  Fixes http://plone.org/products/feedfeeder/issues/18
  [maurits]

- Avoid swallowing too much exceptions when applying our GenericSetup
  profile.
  Fixes http://plone.org/products/feedfeeder/issues/19
  [maurits]

1.0rc3 (2008-10-04)
-------------------

- Moved profile definition from python to GenericSetup.  Profile is
  now not 'profile-feedfeeder:default' but
  'profile-Products.feedfeeder:default'.  [maurits]

- In the Extensions/ dir: removed Install.py and renamed AppInstall.py
  to install.py.  [maurits]

- Made feed item updated date available for Collections/Smart Folders.
  [maurits]

- Extensions/AppInstall.py: first try installing our own profile in
  the Plone 3 way and when that fails try the Plone 2.5 way.
  [maurits]

- Removed own feedparser.py.  Instead added an install_requires
  dependency on FeedParser in setup.py.  [maurits]

- Moved fix for feeds starting with 'feed:' instead of 'http:' from
  feedparser.py to utilities.py, so we use an unchanged feedparser.py
  again.  [maurits]


1.0 rc 2 (2008-07-23)
---------------------

- Re-release of rc1: rc1 was missing all .txt files, making install impossible
  as setup.py reads version.txt. [reinout]


1.0 rc 1 (2008-07-15)
---------------------

- Accept entries without a title, which is allowed in rss.
  See http://cyber.law.harvard.edu/rss/rss.html#hrelementsOfLtitemgt
  [maurits]


1.0 beta 4 (2008-05-20)
-----------------------

- Eggification: you can now install it as the Products.feedfeeder
  egg.  [maurits]


1.0 beta 3 (2008-05-13)
-----------------------

- In the tests, use plone_workflow explicitly, so it is easier to test
  on both Plone 2.5 and 3.0.  [maurits]

- Make update_feed_items available in the object_buttons for Plone 3,
  using new small @@is_feedcontainer as condition.  [maurits]

- Avoid deprecation warnings for events and interfaces.  [maurits]

- Remove semicolon in page template that broke in Plone 3.  [maurits]

- Fix imports so they work in Plone 3 as well, without deprecation
  warnings.  [derstappenit]


1.0 beta 2 (2008-01-02)
-----------------------

- History begins.
