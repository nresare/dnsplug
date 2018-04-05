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

# This code is copied pretty much as is from
# https://github.com/sdgathman/pymilter/blob/master/Milter/dns.py

# Provide a higher level interface to pydns.

from __future__ import print_function
from __future__ import absolute_import

try:
    import DNS
    pydns = True
except ImportError:
    from dns.resolver import query, NoAnswer, NXDOMAIN
    from dns.exception import DNSException as dnspython_DNSException
    pydns = False

MAX_CNAME = 10


class DNSException(Exception):
    pass


## Lookup DNS records by label and RR type.
# The response can include records of other types that the DNS
# server thinks we might need.
# @param name the DNS label to lookup
# @param qtype the name of the DNS RR type to lookup
# @return a list of ((name,type),data) tuples
def pydns_lookup(name, qtype):
    try:
        # To be thread safe, we create a fresh DnsRequest with
        # each call.  It would be more efficient to reuse
        # a req object stored in a Session.
        req = DNS.DnsRequest(name, qtype=qtype)
        resp = req.req()
        #resp.show()
        # key k: ('wayforward.net', 'A'), value v
        # FIXME: pydns returns AAAA RR as 16 byte binary string, but
        # A RR as dotted quad.  For consistency, this driver should
        # return both as binary string.
        return [((a['name'], a['typename']), a['data']) for a in resp.answers]
    except IOError as x:
        raise DNSException(str(x))


def dnspython_lookup(name, query_type):
    ret_val = []
    try:
        answers = query(name, query_type)
        for response in answers:
            if query_type == 'A':
                ret_val.append(((name, query_type), response.address))
            elif query_type == 'AAAA':
                ret_val.append(((name, query_type), response.to_digestable()))
            elif query_type == 'MX':
                exchange = response.exchange.to_text()
                if exchange.endswith('.'):
                    exchange = exchange[:-1]
                ret_val.append(((name, query_type), (response.preference, exchange)))
            elif query_type == 'PTR':
                ret_val.append(((name, query_type), response.target.to_text(True)))
            elif query_type == 'TXT' or query_type == 'SPF':
                ret_val.append(((name, query_type), response.strings))
    except NoAnswer:
        pass
    except NXDOMAIN:
        pass
    except dnspython_DNSException as x:
        raise DNSException('DNS ' + str(x))
    return ret_val



class Session(object):
  """A Session object has a simple cache with no TTL that is valid
   for a single "session", for example an SMTP conversation."""
  def __init__(self):
    self.cache = {}

  ## Additional DNS RRs we can safely cache.
  # We have to be careful which additional DNS RRs we cache.  For
  # instance, PTR records are controlled by the connecting IP, and they
  # could poison our local cache with bogus A and MX records.
  # Each entry is a tuple of (query_type,rr_type).  So for instance,
  # the entry ('MX','A') says it is safe (for milter purposes) to cache
  # any 'A' RRs found in an 'MX' query.
  SAFE2CACHE = frozenset((
    ('MX','MX'), ('MX','A'),
    ('CNAME','CNAME'), ('CNAME','A'),
    ('A','A'),
    ('AAAA','AAAA'),
    ('PTR','PTR'),
    ('NS','NS'), ('NS','A'),
    ('TXT','TXT'),
    ('SPF','SPF')
  ))

  ## Cached DNS lookup.
  # @param name the DNS label to query
  # @param qtype the query type, e.g. 'A'
  # @param cnames tracks CNAMES already followed in recursive calls
  def dns(self, name, qtype, cnames=None):
    """DNS query.

    If the result is in cache, return that.  Otherwise pull the
    result from DNS, and cache ALL answers, so additional info
    is available for further queries later.

    CNAMEs are followed.

    If there is no data, [] is returned.

    pre: qtype in ['A', 'AAAA', 'MX', 'PTR', 'TXT', 'SPF']
    post: isinstance(__return__, types.ListType)
    """
    if name.endswith('.'): name = name[:-1]

    labels = name.split(".")
    if not labels:
        return []
    for label in labels:
        if not 0 < len(label) < 64:
            return []

    name = name.lower()
    result = self.cache.get( (name, qtype) )
    cname = None
    if result: return result
    cnamek = (name,'CNAME')
    cname = self.cache.get( cnamek )

    if cname:
        cname = cname[0]
    else:
        safe2cache = Session.SAFE2CACHE
        for k, v in pydns_lookup(name, qtype) if pydns else dnspython_lookup(name, qtype):
            if k == cnamek:
                cname = v
            if k[1] == 'CNAME' or (qtype,k[1]) in safe2cache:
                self.cache.setdefault(k, []).append(v)
        result = self.cache.get( (name, qtype), [])
    if not result and cname:
        if not cnames:
            cnames = {}
        elif len(cnames) >= MAX_CNAME:
            #return result    # if too many == NX_DOMAIN
            raise DNSException('Length of CNAME chain exceeds %d' % MAX_CNAME)
        cnames[name] = cname
        if cname.lower().rstrip('.') in cnames:
            raise DNSException('CNAME loop')
        result = self.dns(cname, qtype, cnames=cnames)
        if result:
            self.cache[(name,qtype)] = result
    return result

  def dns_txt(self, domainname, enc='ascii'):
    "Get a list of TXT records for a domain name."
    if domainname:
        try:
            return [''.join(s.decode(enc) for s in a)
                for a in self.dns(domainname, 'TXT')]
        except UnicodeEncodeError:
            raise DNSException('Non-ascii character in SPF TXT record.')
    return []

if pydns:
    DNS.DiscoverNameServers()
