from dnsplug import lookup


def test_lookup_mx():
    response = lookup('jresolvertest.resare.com', 'MX')
    assert response == [(10, 'mail.resare.com')]
