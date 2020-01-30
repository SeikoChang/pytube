# -*- coding: utf-8 -*-
"""Implements a simple wrapper around urlopen."""
import sys
from pytube.compat import urlopen

# 403 forbidden fix
PY3K = sys.version_info >= (3, 0)
if PY3K:
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2 
    import urlparse


def get(
    url=None, headers=False,
    streaming=False, chunk_size=8 * 1024,
):
    """Send an http GET request.

    :param str url:
        The URL to perform the GET request for.
    :param bool headers:
        Only return the http headers.
    :param bool streaming:
        Returns the response body in chunks via a generator.
    :param int chunk_size:
        The size in bytes of each chunk.
    """

    # 403 forbidden fix
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    #req = urllib2.request.Request(url, headers = {"User-Agent": "Mozilla/5.0"})
    request = urllib2.Request(url, headers=hdr)
    #response = urlopen(url)
    response = urllib2.urlopen(request)

    if streaming:
        return stream_response(response, chunk_size)
    elif headers:
        # https://github.com/nficano/pytube/issues/160
        return {k.lower(): v for k, v in response.info().items()}
    return (
        response
        .read()
        .decode('utf-8')
    )


def stream_response(response, chunk_size=8 * 1024):
    """Read the response in chunks."""
    while True:
        buf = response.read(chunk_size)
        if not buf:
            break
        yield buf
