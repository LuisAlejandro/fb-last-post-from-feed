#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.parse import urlencode

from atoma import parse_rss_bytes

from utils import escape, html_unescape, u, s


FACEBOOK_PAGE_ID = os.environ.get('FACEBOOK_PAGE_ID')
FACEBOOK_ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')
FACEBOOK_API_END = 'https://graph.facebook.com/{0}/feed'.format(FACEBOOK_PAGE_ID)
FEED_URL = os.environ.get('FEED_URL')
FEED_DATA = parse_rss_bytes(urlopen(FEED_URL).read())


for post in FEED_DATA.items:

    ITEM_TIMESTAMP = int(post.pub_date.strftime('%Y%m%d%H%M%S'))
    LAST_TIMESTAMP = int(datetime.now().strftime('%Y%m%d%H%M%S')) - 10000
    ITEM_TITLE = u(html_unescape(post.title))
    ITEM_LINK = u(post.guid)

    # if ITEM_TIMESTAMP >= LAST_TIMESTAMP:

    FACEBOOK_API_DATA = {'message': ITEM_TITLE,
                            'link': ITEM_LINK,
                            'access_token': FACEBOOK_ACCESS_TOKEN}

    HTTP_REQUEST = Request(url=FACEBOOK_API_END,
                            data=s(urlencode(FACEBOOK_API_DATA)))

    print(vars(HTTP_REQUEST))

    while True:

        RESULT = json.loads(urlopen(HTTP_REQUEST).read())

        if 'error' not in RESULT:
            print('Publicación exitosa: '+ITEM_LINK)
            break
    raise