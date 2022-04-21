# -*- coding: utf-8 -*-
#
# Please refer to AUTHORS.md for a complete list of Copyright holders.
# Copyright (C) 2020-2022 Luis Alejandro Martínez Faneyth.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import time
import datetime
from urllib.request import urlopen
from html import unescape

from atoma import parse_rss_bytes
from pyfacebook import GraphAPI


count = 0
access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
page_id = os.environ.get('FACEBOOK_PAGE_ID')
feed_url = os.environ.get('FEED_URL')
max_count = int(os.environ.get('MAX_COUNT', 1))
post_lookback = int(os.environ.get('POST_LOOKBACK', 1 * 60 * 60))

if not feed_url:
    raise Exception('No FEED_URL provided.')

if not page_id:
    raise Exception('No FACEBOOK_PAGE_ID provided.')

graph = GraphAPI(access_token=access_token, version="13.0")

feed_data = parse_rss_bytes(urlopen(feed_url).read())
today = datetime.datetime.now()
last_run = today - datetime.timedelta(seconds=post_lookback)
last_timestamp = int(last_run.strftime('%Y%m%d%H%M%S'))

for post in feed_data.items:

    if count >= max_count:
        break

    item_timestamp = int(post.pub_date.strftime('%Y%m%d%H%M%S'))
    data = {'message': unescape(post.title), 'link': post.guid}

    if item_timestamp > last_timestamp:
        count += 1
        fb = graph.post_object(object_id=page_id,
                               connection='feed',
                               data=data)
        time.sleep(10)
        graph.delete_object(object_id=fb['id'])
