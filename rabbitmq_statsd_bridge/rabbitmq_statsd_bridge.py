from collections import defaultdict
from abc import ABCMeta, abstractmethod
from time import sleep

import requests
import statsd


class HttpPollMonitor:
    def __init__(
            self, mq_host, stats_host, mq_port=15672, stat_base='rabbitmq',
            poll_interval=10):
        self._stat_handlers = defaultdict(list)
        self._stat_base = stat_base
        self._stats = statsd.StatsClient(stats_host)
        self._poll_interval = poll_interval
        self._mq_base_url = 'http://{}:{}'.format(mq_host, mq_port)
        self._auth = requests.auth.HTTPBasicAuth('guest', 'guest')

    def _json_getter(self, path):
        response = requests.get(self._mq_base_url + path, auth=self._auth)
        return response.json()

    def _poll(self):
        for path, handlers in self._stat_handlers.items():
            try:
                poll_data = self._json_getter(path)
            except requests.ConnectionError as e:
                print('Poll failed: ConnectionError')
                return
            for handler in handlers:
                handler(self._stats, self._stat_base, poll_data)

    def __call__(self):
        while True:
            self._poll()
            sleep(self._poll_interval)

    def add(self, stat):
        self._stat_handlers[stat.poll_path].append(stat.report)


class Reporter:
    __metaclass__ = ABCMeta

    def __init__(self, poll_path):
        self.poll_path = poll_path

    @abstractmethod
    def report(self, stats_client, poll_data):
        pass


class ReadyInQueue(Reporter):
    def __init__(self, queue, vhost='%2F'):
        super(ReadyInQueue, self).__init__(
            '/api/queues/{}/{}/'.format(vhost, queue))

    def report(self, stats_client, stat_base, poll_data):
        stats_client.gauge(
            '{}.{}.ready'.format(stat_base, poll_data['name']),
            poll_data['messages_ready'])
