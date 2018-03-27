from dnsplug.dns import Session


def test_lookup():
    s = Session()
    response = s.dns("jresolvertest.resare.com", "MX")
    assert response == [(10, "mail.resare.com")]
