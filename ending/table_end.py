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

# In Spanish we don't have enough room to put all the lines
#   in the original place (x73F4C) so we have to move them.
# we used 0x742E1 as new ptr
# and 0x76C90 for the new data address

# original data (WITHOUT HEADER)
ORIGINAL_PTR = 0x73F4C

# max space available on the NEW place
MAXSIZE = 0x760

# replace this table with your values
# TODO: made a generator :P

TABLE = {
        "1A":"A",
        "1B":"B",
        "1C":"C",
        "1D":"D",
        "1E":"E",
        "1F":"F",
        "20":"G",
        "21":"H",
        "22":"I",
        "23":"J",
        "24":"K",
        "25":"L",
        "26":"M",
        "27":"N",
        "28":"O",
        "29":"P",
        "2A":"Q",
        "2B":"R",
        "2C":"S",
        "2D":"T",
        "2E":"U",
        "2F":"V",
        "30":"W",
        "31":"X",
        "32":"Y",
        "33":"Z",
# ALT
        "38":"[v_A]",
        "39":"[v_B]",
        "3A":"[v_C]",
        "3B":"[v_D]",
        "3C":"[v_E]",
        "3D":"[v_F]",
        "3E":"[v_G]",
        "3F":"[v_H]",
        "40":"[v_I]",
        "41":"[v_J]",
        "42":"[v_K]",
        "43":"[v_L]",
        "44":"[v_M]",
        "45":"[v_N]",
        "46":"[v_O]",
        "47":"[v_P]",
        "48":"[v_Q]",
        "49":"[v_R]",
        "4A":"[v_S]",
        "4B":"[v_T]",
        "4C":"[v_U]",
        "4D":"[v_V]",
        "4E":"[v_W]",
        "4F":"[v_X]",
        "50":"[v_Y]",
        "51":"[v_Z]",
        "52":"[V_·]",
# UPPER
        "5D":"[A]",
        "5E":"[B]",
        "5F":"[C]",
        "60":"[D]",
        "61":"[E]",
        "62":"[F]",
        "63":"[G]",
        "64":"[H]",
        "65":"[I]",
        "66":"[J]",
        "67":"[K]",
        "68":"[L]",
        "69":"[M]",
        "6A":"[N]",
        "6B":"[O]",
        "6C":"[P]",
        "6D":"[Q]",
        "6E":"[R]",
        "6F":"[S]",
        "70":"[T]",
        "71":"[U]",
        "72":"[V]",
        "73":"[W]",
        "74":"[X]",
        "75":"[Y]",
        "76":"[Z]",
        "77":"[']",
        "78":"[!]",
        "16":"[Ñ]", # substituye W_ROJO
        "18":"[¡]", # substituye Y_ROJO
# LOWER
        "83":"[a]",
        "84":"[b]",
        "85":"[c]",
        "86":"[d]",
        "87":"[e]",
        "88":"[f]",
        "89":"[g]",
        "8A":"[h]",
        "8B":"[i]",
        "8C":"[j]",
        "8D":"[k]",
        "8E":"[l]",
        "8F":"[m]",
        "90":"[n]",
        "91":"[o]",
        "92":"[p]",
        "93":"[q]",
        "94":"[r]",
        "95":"[s]",
        "96":"[t]",
        "97":"[u]",
        "98":"[v]",
        "99":"[w]",
        "9A":"[x]",
        "9B":"[y]",
        "9C":"[z]",
        "9E":"[_!]", 
        "9D":"[_']",
        "17":"[ñ]",  # substituye X_ROJO
        "19":"[_¡]", # substituye Z_ROJO
# OTROS
        "34":"[¬]", # acento     - substituye la coma
        "35":"[~]", # virgulilla - substituye la coma
        "36": "-",
        "37": ".",
        "9F":" ",
        "FF":"[END]\n\n" # using linux endline (\r\n for win32... i think)
}

