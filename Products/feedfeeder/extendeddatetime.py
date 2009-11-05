from DateTime import DateTime

#http://www.timeanddate.com/library/abbreviations/timezones/na/
alttzmap= dict( ndt=u'GMT-0230',
                adt=u'GMT-0300',
                edt=u'GMT-0400',
                cdt=u'GMT-0500',
                mdt=u'GMT-0600',
                pdt=u'GMT-0700',
                akdt=u'GMT-0800',
                hadt=u'GMT-0900')

def extendedDateTime(dt):
    """takes a very pragmatic approach to the timezone variants in feeds"""
    try:
        return DateTime(dt)
    except DateTime.SyntaxError:
        frags = dt.split()
        newtz = alttzmap.get(frags[-1].lower(), None)
        if newtz is None:
            raise
        frags[-1] = newtz
        newdt = ' '.join(frags)
        return DateTime(newdt)


