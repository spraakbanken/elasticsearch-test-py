import time
import requests
import tempfile
import pytest

import elasticsearch_test


def test_start_block():
    instance = elasticsearch_test.ElasticsearchTest()
    instance.start()
    assert instance.is_started()
    assert_response(instance)
    instance.stop()
    assert not instance.is_started()


def test_start_non_block():
    instance = elasticsearch_test.ElasticsearchTest()
    instance.start(block=False)
    assert not instance.is_started()
    while not instance.is_started():
        time.sleep(1)
    assert_response(instance)
    instance.stop()
    assert not instance.is_started()


def test_context_manager():
    with elasticsearch_test.ElasticsearchTest() as instance:
        assert_response(instance)


def test_file_instead_of_dir():
    (_, name) = tempfile.mkstemp()
    instance = elasticsearch_test.ElasticsearchTest(es_path=name)
    with pytest.raises(RuntimeError):
        instance.start()


def test_non_es_dir():
    directory = tempfile.mkdtemp()
    instance = elasticsearch_test.ElasticsearchTest(es_path=directory)
    with pytest.raises(RuntimeError):
        instance.start()


def test_other_port():
    with elasticsearch_test.ElasticsearchTest(port=9222) as instance:
        url = instance.get_url()
        assert url == 'http://127.0.0.1:9222'
        assert_response(instance)


def assert_response(instance):
    url = instance.get_url()
    response = requests.get(url).json()
    assert 'You Know, for Search' in response['tagline']
