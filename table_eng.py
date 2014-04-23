#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
   Copyright (C) 2014 David Colmenero - D_Skywalk
    http://david.dantoine.org

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   higher any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software Foundation,
   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
"""

# Example for Zelda aLttP :D

# safe value (not in table used in replaces)
SAFE = "@"

# end value for an end repeating value
ENDVAL = "FF"

# replace this table with your values
# TODO: made a generator :P
TABLE = {
        "00":"A",
        "01":"B",
        "02":"C",
        "03":"D",
        "04":"E",
        "05":"F",
        "06":"G",
        "07":"H",
        "08":"I",
        "09":"J",
        "0A":"K",
        "0B":"L",
        "0C":"M",
        "0D":"N",
        "0E":"O",
        "0F":"P",
        "10":"Q",
        "11":"R",
        "12":"S",
        "13":"T",
        "14":"U",
        "15":"V",
        "16":"W",
        "17":"X",
        "18":"Y",
        "19":"Z",
        "1A":"a",
        "1B":"b",
        "1C":"c",
        "1D":"d",
        "1E":"e",
        "1F":"f",
        "20":"g",
        "21":"h",
        "22":"i",
        "23":"j",
        "24":"k",
        "25":"l",
        "26":"m",
        "27":"n",
        "28":"o",
        "29":"p",
        "2A":"q",
        "2B":"r",
        "2C":"s",
        "2D":"t",
        "2E":"u",
        "2F":"v",
        "30":"w",
        "31":"x",
        "32":"y",
        "33":"z",
        "34":"0",
        "35":"1",
        "36":"2",
        "37":"3",
        "38":"4",
        "39":"5",
        "3A":"6",
        "3B":"7",
        "3C":"8",
        "3D":"9",
        "3E":"!",
        "3F":"?",
        "40":"-",
        "41":".",
        "42":",",
        "43":"[43]",
        "44":"|>",
        "45":"(",
        "46":")",
        "47":"ñ",
        "48":"ú",
        "49":"á",
        "4C":"\"",
        "51":"'",
        "5A":"<|",
        "5B":"[A]",
        "5C":"[B]",
        "5D":"[X]",
        "5E":"[Y]",
        "59":" ",
        "60":"[60]",
        "61":"[61]",
        "68":"[Choose]",
        "71":"[Choose2]",
        "6A":"[Name]",
        "73":"[Scroll]",
        "7E":"[Waitkey]",
        "74":"[1]",
        "75":"[2]",
        "76":"[3]",
        "7F":"[END]\n\n\n", # using linux endline (\r\n for win32... i think)
        "8A":"[Espacio 2]",

        # eng
        "8B":"'s ",
        "8C":"and ",
        "8D":"are ",
        "8E":"all ",
        "8F":"ain",
        "90":"and",
        "91":"at ",
        "92":"ast",
        "93":"an",
        "94":"at",
        "95":"ble",
        "96":"ba",
        "97":"be",
        "98":"bo",
        "99":"can ",
        "9A":"che",
        "9B":"com",
        "9C":"ck",
        "9D":"des",
        "9E":"di",
        "9F":"do",
        "A0":"en ",
        "A1":"er ",
        "A2":"ear",
        "A3":"ent",
        "A4":"ed ",
        "A5":"en",
        "A6":"er",
        "A7":"ev",
        "A8":"for",
        "A9":"fro",
        "AA":"give ",
        "AB":"get",
        "AC":"go",
        "AD":"have",
        "AE":"has",
        "AF":"her",
        "B0":"hi",
        "B1":"ha",
        "B2":"ight ",
        "B3":"ing ",
        "B4":"in",
        "B5":"is",
        "B6":"it",
        "B7":"just",
        "B8":"know",
        "B9":"ly ",
        "BA":"la",
        "BB":"lo",
        "BC":"man",
        "BD":"ma",
        "BE":"me",
        "BF":"mu",
        "C0":"n't ",
        "C1":"non",
        "C2":"not",
        "C3":"open",
        "C4":"ound",
        "C5":"out ",
        "C6":"of",
        "C7":"on",
        "C8":"or",
        "C9":"per",
        "CA":"ple",
        "CB":"pow",
        "CC":"pro",
        "CD":"re ",
        "CE":"re",
        "CF":"some",
        "D0":"se",
        "D1":"sh",
        "D2":"so",
        "D3":"st",
        "D4":"ter ",
        "D5":"thin",
        "D6":"ter",
        "D7":"tha",
        "D8":"the",
        "D9":"thi",
        "DA":"to",
        "DB":"tr",
        "DC":"up",
        "DD":"ver",
        "DE":"with",
        "DF":"wa",
        "E0":"we",
        "E1":"wh",
        "E2":"wi",
        "E3":"you",
        "E4":"Her",
        "E5":"Tha",
        "E6":"The",
        "E7":"Thi",
        "E8":"You",


}
