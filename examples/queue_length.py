from sys import argv

import statsd

from rabbitmq_statsd_bridge import HttpPollMonitor, ReadyInQueue


HOST = argv[1]
stats_client = statsd.StatsClient(HOST)
MQ_BASE_URL = 'http://{}:15672'.format(HOST)
m = HttpPollMonitor(MQ_BASE_URL, stats_client)
m.add(ReadyInQueue('work'))
m.add(ReadyInQueue('results'))
m()
