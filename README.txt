Feedfeeder
==========

Feedfeeder has just a few things it needs to do:

- Read in a few ATOM feeds (not too many).

- Create FeedFeederItems out of the entries pulled from the ATOM feeds.
  Any feed items that contain enclosures will have the enclosures
  pulled down and added as File items to the feed item.

- This means figuring out which items are new, which also means having
  a good ID generating mechanism.


Wait, no existing product?
--------------------------

There's a whole slew of RSS/ATOM reading products for zope and
plone. None of them seemed to be a good fit. There was only one
product that actually stored the entries in the zope database, but
that was aimed at a lot of users individually adding a lot of feeds,
so it needed either a separate ZEO process (old version) or a
standalone mysql database (new version).

All the other products didn't store the entries in the database, were
old/unmaintained/etc.

In a sense, we're using an existing product as we use Mark Pilgrim's
excellent feedparser (http://feedparser.org) that'll do the actual
ATOM reading for us.


Product name
------------

The product feeds the content of ATOM feeds to plone as document/file
content types. So "feedfeeder" sort of suggested itself as a funny
name. Fun is important :-)


Product structure
-----------------

I'm using archgenxml to generate the boiler plate stuff. There's a
'generate.sh' shell script that'll call archgenxml for you. Nothing
fancy.

The feedfeeder's content types are: 
  - folder.FeedfeederFolder
  - item.FeedFeederItem


How it works
------------

A feedfeeder is a folder which contains all the previously-added feed
entries as documents or files. It has a 'feeds' attribute that
contains a list of feeds to read.

Feedparser is called periodically (through a cron job?) to parse the
feeds. The UID of the items in the feed are converted to a suitable
filename (md5 hex hash of the atom id of the entry), that way you can
detect whether there are new items.

New items are turned into feed items.
Feed data are filled into feed items (see field named objectInfo).

Scheduled updates for feed folders

Zope can be configured to periodically trigger a url call.
In zope.conf you can use the <clock-server> directive to define a schedule and url
with the following data::

  <clock-server>
     method /path_to_feedfolder/update_feed_items
     period 3600 # seconds
     user admin
     password 123
     host localhost:8080
  </clock-server>

Updating all feeds once
+++++++++++++++++++++++

If your site has several feed folders and you 
want update them all once you can do:: 

   <clock-server>
     method /yoursiteid/feed-mega-update
     period 3600 # seconds
     user admin
     password 123
     host localhost:8080
   </clock-server>
   

Dependencies
------------

We need Plone 4.x.  Compatibility with Plone 4.3 has been checked.

If you use Plone 3, please use a Products.feedfeeder version from the
2.0 line.  The current latest is 2.0.9.


Upgrade notes
-------------

If you have installed Products.feedfeeder 2.1.x in Plone 4.0 or 4.1
and you upgrade to Plone 4.2 or higher, then you will be missing some
functionality for listing or ordering feedfeeder items in new style
collections.  To solve this, you should go to ``portal_setup`` in the
Zope Management Interface, visit the Import tab, select the
"Feedfeeder registry" profile and import all steps.


Tests
-----

The look-here-first test is the doctest at 'doc/feedfeeder-integration.txt'.

Assuming you have a buildout, testing is best done with a propely set up ``bin/test`` command::

  bin/test -s Products.feedfeeder

We are now testing with Travis:

.. image:: https://secure.travis-ci.org/collective/Products.feedfeeder.png
    :target: http://travis-ci.org/collective/Products.feedfeeder
