from sys import argv

from rabbitmq_statsd_bridge import HttpPollMonitor, ReadyInQueue


_, MQ_HOST, STATS_HOST = argv
m = HttpPollMonitor(MQ_HOST, STATS_HOST)
m.add(ReadyInQueue('work'))
m.add(ReadyInQueue('results'))
m()
