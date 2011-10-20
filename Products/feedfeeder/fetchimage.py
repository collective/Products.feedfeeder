"""

    Add images to feedfeeder items.

"""
import logging

import lxml
from lxml.html import fromstring
import requests

from five import grok

from Products.feedfeeder.interfaces.item import IFeedItem, IFeedItemConsumedEvent

# Don't let slow remote server stall us forever
FETCH_TIMEOUT = 30

# Skip images having these marker string in URLs (ads)
IMAGE_BLACKLIST = ["feedads.g.doubleclick.net"]

logger = logging.getLogger("fetchimage")
logger.info("Initialized Feedfeeder image fetcher")

@grok.subscribe(IFeedItem, IFeedItemConsumedEvent)
def fetch_image_on_creation(context, event):
    """
    Check for the image changes when RSS item is fetched.
    
    http://collective-docs.readthedocs.org/en/latest/components/events.html#subscribing-using-the-grok-api
    """
    fetch_image(context)
    
def fetch_image(context, force=False):
    """
    Check if RSS HTML has an image and fetch it.
    
    @parma force: Always fetch - don't check if previous image exists
    """
    
    logger.info("Checking the lead image for %s" % context.absolute_url())
        
    # Get RSS feed payload
    # - which might depend whether we got full text or just summary
    if context.getHasBody():
        # Directly access HTML data to avoid possible 
        # unneeded re-encoding when using accessor method 
        html = context.getRawText()
    else:
        html = context.Description()
        
    if html is not None:
        if html.strip() in ["", '<!--paging_filter-->']:
            # This RSS item contains only a title
            # For <!--paging_filter--> I have no idea what it is...
            # some obscrube undocumented Plone stuff again 
            return
                
    image_url = None
    try:
        image_url = pick_first_image_source(html)
    except Exception, e:
        logger.error(html)
        logger.error("Could not parse HTML")
        logger.exception(e)
        return
    
    # The playload did not have images
    if not image_url:
        return
    
    try:
        download_and_attach_image(context, image_url, force)
    except Exception, e:
        logger.error("Could not fetch remote image")
        logger.exception(e)
        return
    
        
def pick_first_image_source(html):
    """
    Parse HTML using lxml and get the first <img src> or None if it doesn't contain any
    """
    doc = fromstring(html)
    
    def is_blacklisted(src):
        for x in IMAGE_BLACKLIST:
            if x in src:
                return True
            
        return False
    
    for img in doc.iter('img'):
        if "src" in img.attrib:
            src = img.attrib["src"]
            
            # Skip certain kind of images
            if is_blacklisted(src):
                logger.info("Detected blaclisted image:" + src)
                continue
            return src
        
    return None

def download_and_attach_image(context, image_url, force):
    """
    Fetch the image from the remote server and save a local copy of it as ZODB blob.
    """
    
    # Don't try to re-fetch images
    if not force:
        if context.getLeadImage() not in [None, ""]:
            logger.info("Lead image already exists for %s" % context)
            return
    
    logger.info("Fetching remote image: %s" % image_url)
    r = requests.get(image_url, timeout=FETCH_TIMEOUT)
    
    mimetype = r.headers.get("content-type", "").lower()
    if mimetype not in ["image/gif", "image/png", "image/jpeg"]:
        # We don't want those BMPs here...
        logger.warn("Bad image mimetype: %s" % mimetype)
        return
    
    # Products.feedfeeder item Archetypes content type has field called lead image
    # The value is usually set through upload, but we now set it here directly    
    context.setLeadImage(r.content, mimetype=mimetype)
    
    