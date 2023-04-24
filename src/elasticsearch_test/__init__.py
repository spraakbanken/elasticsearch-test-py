# -*- coding: utf-8 -*-
import os
import tempfile
import subprocess
import string
import random
import json

from urllib.request import urlopen

name = "elasticsearch_test"


class ElasticsearchTest:

    def __init__(self, port=9200, es_path=None, data_dir=None, es_java_opts=None):
        self.port = port
        self.es_path = self.get_es_path(es_path)
        self.data_dir = data_dir if data_dir else tempfile.mkdtemp()
        self.es_java_opts = es_java_opts

        self.process = None
        self.started = False

    def start(self, block=True):
        executable = os.path.join(self.es_path, 'bin/elasticsearch')
        data_arg = '-Epath.data=%s' % os.path.join(self.data_dir, 'data')
        logs_arg = '-Epath.logs=%s' % os.path.join(self.data_dir, 'logs')
        port_arg = '-Ehttp.port=%s' % self.port
        host_arg = '-Enetwork.host=127.0.0.1'
        cluster_arg = '-Ecluster.name=%s' % self.generate_cluster_name()

        env_copy = os.environ.copy()
        if self.es_java_opts:
            env_copy['ES_JAVA_OPTS'] = self.es_java_opts

        try:
            self.process = subprocess.Popen([executable, data_arg, logs_arg, port_arg, cluster_arg, host_arg],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            env=env_copy)
        except Exception:
            raise RuntimeError('Failed to start Elasticsearch')
        if block:
            while True:
                line = self.process.stdout.readline().decode()
                if line == '' and self.process.poll() is not None:
                    raise RuntimeError('Failed to start Elasticsearch')
                if 'Node' in line and 'started' in line:
                    self.started = True
                    break

    def is_started(self):
        return self._check_status(('green', 'yellow'))

    def is_data_initialized(self):
        return self._check_status('green')

    def _check_status(self, levels):
        try:
            url = 'http://127.0.0.1:%d/_cluster/health' % self.port
            ret = json.loads(urlopen(url).read().decode('utf-8'))
            return ret['status'] in levels
        except Exception:
            return False

    def stop(self):
        self.started = False
        if self.process:
            self.process.kill()

    def get_connection_info(self):
        return {
            'hosts': ['127.0.0.1:%d' % self.port]
        }

    def get_url(self):
        return 'http://' + self.get_connection_info()['hosts'][0]

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stop()

    @staticmethod
    def get_es_path(es_path):
        if es_path:
            return es_path
        elif 'ES_HOME' in os.environ:
            return os.environ.get('ES_HOME')
        else:
            raise RuntimeError('cannot find Elasticsearch executable')

    @staticmethod
    def generate_cluster_name():
        return ''.join([random.choice(string.ascii_letters) for _ in range(6)])
