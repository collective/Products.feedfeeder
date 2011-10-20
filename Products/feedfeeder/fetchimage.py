"""

    Add images to feedfeeder items.

"""
import logging

import lxml
from lxml.html import fromstring
import requests

from five import grok

from Products.feedfeeder.interfaces.item import IFeedItem

# Don't let slow remote server stall us forever
FETCH_TIMEOUT = 30

logger = logging.getLogger("fetchimage")

@grok.subscribe(IFeedItem, IObjectEditedEvent)
def fetch_image(context, event):
    """
    Check for the image changes when RSS item is fetched.
    
    http://collective-docs.readthedocs.org/en/latest/components/events.html#subscribing-using-the-grok-api
    """
    
    logger.info("Getting lead image for %s" % context)
    
    # Get RSS feed payload
    # - which might depend whether we got full text or just summary
    if context.hasBody():
        html = context.getText()
    else:
        html = context.Description()
        
    image_url = None
    try:
        image_url = pick_first_image_source(html)
    except Exception, e:
        logger.error("Could not parse HTML")
        logger.exception(e)
        return
    
    # The playload did not have images
    if not image_url:
        return
    
    try:
        download_and_attach_image(context, image_url)
    except Exception, e:
        logger.error("Could not fetch remote image")
        logger.exception(e)
        return
        
def pick_first_image_source(html):
    """
    Parse HTML using lxml and get the first <img src> or None if it doesn't contain any
    """
    dom = fromstring(html)
    
    for img in doc.iter('img'):
        if "src" in img.attrib:
            return img.attrib["src"]
        
    return None

def download_and_attach_image(context, image_url):
    """
    Fetch the image from the remote server and save a local copy of it as ZODB blob.
    """
    logger.info("Fetching image: %s" % image_url)
    r = requests.get(image_url, timeout=FETCH_TIMEOUT)
    
    # Products.feedfeeder item Archetypes content type has field called lead image
    # The value is usually set through upload, but we now set it here directly    
    context.setLeadImage(r.content, mimetype=r.headers["content-type"])
    
    