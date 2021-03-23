from example_web_server.utils import camelcase


def test_camelcase():
    assert camelcase('invalid_fields') == 'invalidFields'
    assert camelcase('foo') == 'foo'
    assert camelcase('foo_bar') == 'fooBar'
    assert camelcase('fooBar') == 'fooBar'
    assert camelcase('ABCD_EFGH_IJKL') == 'ABCDEfghIjkl'
