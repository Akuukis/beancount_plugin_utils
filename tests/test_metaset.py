from context import metaset

def test_meta_with_dict():
    assert len(metaset.get({"foo": "bar"}, "foo")) == 1

def test_meta_with_empty_dict():
    assert len(metaset.get({}, "foo")) == 0

def test_meta_with_none():
    assert len(metaset.get(None, "foo")) == 0
