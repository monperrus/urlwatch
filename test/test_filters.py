from urlwatch.filters import GetElementById
from urlwatch.filters import GetElementByTag
from urlwatch.filters import JsonFormatFilter
from urlwatch.filters import Html2TextFilter


def eq_(a, b):
    assert a == b, '%r != %r' % (a, b)


def test_get_element_by_id():
    get_element_by_id = GetElementById(None, None)
    result = get_element_by_id.filter("""
    <html><head></head><body>
    <div id="foo">asdf <span>bar</span></div>
    <div id="bar">asdf <span>bar</span> hoho</div>
    </body></html>
    """, 'bar')
    print(result)
    eq_(result, '<div id="bar">asdf <span>bar</span> hoho</div>')


def test_get_element_by_tag():
    get_element_by_tag = GetElementByTag(None, None)
    result = get_element_by_tag.filter("""
    <html><head></head><body>foo</body></html>
    """, 'body')
    print(result)
    eq_(result, '<body>foo</body>')


def test_get_element_by_tag_nested():
    get_element_by_tag = GetElementByTag(None, None)
    result = get_element_by_tag.filter("""
    <html><head></head><body>
    <div>foo</div>
    <div>bar</div>
    </body></html>
    """, 'div')
    print(result)
    eq_(result, """<div>foo</div><div>bar</div>""")


def test_json_format_filter():
    json_format_filter = JsonFormatFilter(None, None)
    result = json_format_filter.filter(
        """{"field1": {"f1.1": "value"},"field2": "value"}""")
    print(result)
    eq_(result, """{
    "field1": {
        "f1.1": "value"
    },
    "field2": "value"
}""")


def test_json_format_filter_subfilter():
    json_format_filter = JsonFormatFilter(None, None)
    result = json_format_filter.filter(
        """{"field1": {"f1.1": "value"},"field2": "value"}""", "2")
    print(result)
    eq_(result, """{
  "field1": {
    "f1.1": "value"
  },
  "field2": "value"
}""")


HTML2TEXT_INPUT = ('<html><head><script>var x=1;</script></head><body>'
                   '<h1>Title</h1><p>Hello <a href="/x">link</a></p>'
                   '<table><tr><td>a</td><td>b</td></tr></table></body></html>')


def test_html2text_default_is_inscriptis():
    html2text_filter = Html2TextFilter(None, None)
    eq_(html2text_filter.filter(HTML2TEXT_INPUT, {}), 'Title\n\nHello link\n\na  b')


def test_html2text_inscriptis_options():
    html2text_filter = Html2TextFilter(None, None)
    result = html2text_filter.filter(HTML2TEXT_INPUT, {'method': 'inscriptis', 'display_links': True})
    eq_(result, 'Title\n\nHello [link](/x)\n\na  b')


def test_html2text_re_still_available():
    html2text_filter = Html2TextFilter(None, None)
    eq_(html2text_filter.filter(HTML2TEXT_INPUT, {'method': 're'}), 'var x=1;TitleHello linkab')
