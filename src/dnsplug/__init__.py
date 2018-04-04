# dnsplug - a thin wrapper and caching layer for dns lookups
# Copyright (C) 2007-2016 Stuart Gathman <stuart@gathman.org>
# Copyright (C) 2018 Noa Resare <noa@resare.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from .dns import Session
from typing import Union, Tuple, List

SESSION_SINGLETON = Session()

ResultType = Union[
    str,               # used for A, PTR
    Tuple[int, str],   # used for MX
    List[bytes],       # used for TXT and SPF
    bytes              # used for AAAA
]


def lookup(name, query_type):
    # type: (str, str) -> List[ResultType]
    """Lookup and return the DNS record with name and query_type. The result is
    cached for improved performance.

    :param name: a name, such as "google.com"
    :param query_type: a dns record type, such as "A" or "TXT"
    :return: a list of strings with the lookup result, or None if there was
    no record.
    """
    return SESSION_SINGLETON.dns(name, query_type)
