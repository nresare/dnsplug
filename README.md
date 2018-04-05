dnsplug - a thin wrapper and caching layer for dns lookups
==========================================================

This project provides a simple high level api for performing
DNS lookups. The actual DNS protocol implementation is provided
by either py3dns/pydns or dnspython, depending on which of these
is available. Additionally, responses are cached to improve
the performance of multiple queries for the same value.

This code was originally written by Stuart D. Gathman as part of the
[pymilter project](https://github.com/sdgathman/pymilter/blob/master/Milter/dns.py)

Dependencies
------------

Dnsplug depends on either pydns/py3dns or dnspython (attempted in
that order). If running in python2, the `typing` module is also needed


Testing the module
------------------

in your virtualenv, run `pip install tox` and then invoke `tox`. This
expects a python 2.7 and python 3.6 to be available.


Why is the module below src?
----------------------------

Short answer: to be able to correctly test with tox, long answer 
[here](https://blog.ionelmc.ro/2014/05/25/python-packaging)

TODO
----

* As the copied code from pymilter notes, it is a bit inconsistent
  that AAAA records are returned as binary strings but A is returned
  as a dot separated octet ascii string. Let's figure out something
  better.
* Figure out a way to do testing that doesn't depend on internet
  connectivity. Let's mock the remote end.
* Testing of various failure modes.
* Set up automated testing somewhere (Travis CI?)