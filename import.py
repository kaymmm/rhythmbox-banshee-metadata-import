#!/usr/bin/python

"""
Copyright (c) 2017 Keith Miyake
Copyright (c) 2009 Wolfgang Steitz

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

"""

import sqlite3
from lxml import etree
from os.path import expanduser
import shutil

# Change the following paths as appropriate on your system
user_home = expanduser('~')
RB_DB = user_home + '/.local/share/rhythmbox/rhythmdb.xml'
BA_DB = user_home + '/.config/banshee-1/banshee.db'

RB_DB_BAK = RB_DB + '.backup'

shutil.copy2(RB_DB, RB_DB_BAK)


class banshee_db():
    def __init__(self, file):
        self.con = sqlite3.connect(file)

    def get_song_info(self, url):
        res = self.con.execute(
            'SELECT Rating, Playcount, LastPlayedStamp \
                    FROM CoreTracks WHERE Uri=?', (url,)
            ).fetchone()
        if res is None:
            return None, None, None
        else:
            return res


banshee = banshee_db(BA_DB)

tree = etree.parse(RB_DB)
root = tree.getroot()
for song in (root.findall('entry[@type="song"]')):
    location = song.find('location').text
    # title = song.find('title').text
    rating = song.find('rating')
    rating = rating.text if rating is not None else None
    playcount = song.find('play-count')
    playcount = int(playcount.text) if playcount is not None else None
    lastplayed = song.find('last-played')
    lastplayed = int(lastplayed.text) if lastplayed is not None else None

    rating_b, playcount_b, lastplayed_b = banshee.get_song_info(location)
    if rating is None:  # don't overwrite rhythmbox ratings
        if not (rating_b == 0 or rating_b is None):
            rating = rating_b
            # print('Update rating for "' + title + '" to ' + str(rating))

    if not (playcount_b == 0 or playcount_b is None):
        if playcount is None or playcount_b > playcount:
            playcount = playcount_b
            # print('Update playcount for "' + title +
            #       '" to ' + str(playcount))

    if lastplayed is None and lastplayed_b is not None:
        lastplayed = lastplayed_b
    elif lastplayed is not None and lastplayed_b is not None \
            and lastplayed < lastplayed_b:
        lastplayed = lastplayed_b

    # insert rating into rb db
    if rating is not None:
        element = etree.Element('rating')
        element.text = str(rating)
        song.append(element)

    # update playcount
    if playcount is not None:
        element = etree.Element('play-count')
        element.text = str(playcount)
        song.append(element)

    # update last played
    if lastplayed is not None:
        element = etree.Element('last-played')
        element.text = str(lastplayed)
        song.append(element)

tree.write(RB_DB)
