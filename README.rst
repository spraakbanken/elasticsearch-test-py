Python Elasticsearch Test
=========================

Start Elasticsearch using Python.

Settings
--------

::

    elasticsearch_test.ElasticsearchTest(
      port=1234
      es_path='/home/maria/elasticsearch-5.2.4'
      data_dir='/home/maria/es-data'
      es_java_opts='-Xms512m -Xmx512m'
    )

``port``

Default: ``9200``

``es_path``

Path to the Elasticsearch directory (home of ``/bin``). Default: uses ``$ES_HOME``

``es_java_opts``

Sets ``$ES_JAVA_OPTS`` for process to this value if present.


``data_dir``

Directory to place ``/data`` and ``/logs`` in. Default: uses ``tempfile``.

Running
-------

::

    import time
    import elasticsearch_test
    instance = elasticsearch_test.ElasticsearchTest()

    # This blocks until either an error is found
    # or Elasticsearch has been initialized.

    instance.start()

    # or

    instance.start(block=False)

    while True:
        if instance.is_started():
            break
        time.sleep(1)

Testing
-------

Use it as a resource:::

    import elasticsearch_test
    import elasticsearch

    with elasticsearch_test.ElasticsearchTest() as instance:
        connection_info = instance.get_connection_info()
        client = elasticsearch.Elasticsearch(connection_info)


Use it as a Pytest fixture:::

    import elasticsearch_test

    @pytest.fixture(scope="session")
    def es():
        instance = elasticsearch_test.ElasticsearchTest()
        instance.start()
        yield instance
        instance.stop()


When using ``data_dir``, if there are preexisting data in the directory,
you should also wait for the data to be initialized:::

    with elasticsearch_test.ElasticsearchTest(data_dir='my_data') as instance:
        while not instance.is_data_initialized():
            time.sleep(1)
        # do something!


Test this package
-----------------

Needed: ``pyenv`` and the plugin ``pyenv-virtualenv``.

1. Create a normal virtualenv and activate it

2. Install extras ``pip install .[testing]``

3. Install the needed Python versions using ``pyenv``: ``3.8``, ``3.9``, ``3.10``, ``3.11``

4. Setup virtualenvs for all but the Python version you are using, for example if you use ``3.8``

    ::

      $ pyenv virtualenv -p python3.9 3.9.8 py39
      $ pyenv virtualenv -p python3.10 3.10.8 py310
      $ pyenv virtualenv -p python3.11 3.11.0 py311

5. Setup path to Elasticsearch

    ::

      $ export ES_HOME=/opt/elasticsearch-6.8.23/

6. Activate everything and run `tox`:

    ::

      $ pyenv shell py39 py310 py311
      $ source ./venv/bin/activate
      $ tox

