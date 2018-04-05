from dnsplug import lookup

# yes, I know, this is technically a unit tests as it hits a server on the internet.


# these behaviours have been manually verified to be the same as the dns() method in pyspf


def test_lookup_a():
    response = lookup('dnsplug0.resare.com', 'A')
    assert response == ['10.10.10.10']


def test_lookup_mx():
    response = lookup('dnsplug1.resare.com', 'MX')
    assert sorted(response) == [
        (1, 'dnsplug0.resare.com'), (1, 'dnsplug1.resare.com')
    ]


def test_lookup_aaaa():
    response = lookup('dnsplug4.resare.com', 'AAAA')
    assert response == [
        b'*\x03\xb0\xc0\x00\x02\x00\xd0\x00\x00\x00\x00\x02\xd8\x90\x01'
    ]


def test_lookup_spf():
    response = lookup('dnsplug2.resare.com', 'SPF')
    assert response == [[b'v=spf1 include:e2.example.com']]


def test_lookup_txt():
    response = lookup('dnsplug2.resare.com', 'TXT')
    assert response == [[b'v=spf1 include:e2.example.com']]


def test_lookup_ptr():
    response = lookup('dnsplug3.resare.com', 'PTR')
    assert response == ['dnsplug0.resare.com']


def test_non_existing():
    assert lookup('non_existing.resare.com', 'A') == []
