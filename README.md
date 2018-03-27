dnsplug - a thin wrapper and caching layer for dns lookups
==========================================================

This project provides a simple high level api for performing
DNS lookups. The actual DNS protocol implementation is provided
by either py3dns/pydns or dnspython, depending on which of these
is available. Additionally, responses are cached to improve
the performance of multiple queries for the same value.

This code was originally written by Stuart D. Gathman as part of the
[pymilter project](https://github.com/sdgathman/pymilter/blob/master/Milter/dns.py)

Testing the module
------------------

Soon, very soon, there will be good test coverage. Test by running 'tox'



Why is the module below src?
----------------------------

Short answer: to be able to correctly test with tox, long answer 
[here](https://blog.ionelmc.ro/2014/05/25/python-packaging)

