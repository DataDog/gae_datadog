# stdlib
from collections import defaultdict
from datetime import datetime, timedelta
import os
import time
import json

# google api
from google.appengine.api import app_identity, logservice, memcache, taskqueue
from google.appengine.ext.db import stats as db_stats
from google.appengine.ext.db import to_dict

# framework
import webapp2


class DatadogStats(webapp2.RequestHandler):
    def get(self):
        api_key = self.request.get('api_key')
        if api_key != os.environ.get('DATADOG_API_KEY'):
            self.abort(403)

        FLAVORS = ['requests', 'services', 'all']

        flavor = self.request.get('flavor')
        if flavor not in FLAVORS:
            self.abort(400)

        def get_task_queue_stats(queues=None):
            if queues is None:
                queues = ['default']
            else:
                queues = queues.split(',')
            task_queues = [taskqueue.Queue(q).fetch_statistics() for q in queues]
            q_stats = []
            for q in task_queues:
                stats = {
                    'queue_name': q.queue.name,
                    'tasks': q.tasks,
                    'oldest_eta_usec': q.oldest_eta_usec,
                    'executed_last_minute': q.executed_last_minute,
                    'in_flight': q.in_flight,
                    'enforced_rate': q.enforced_rate,
                }
                q_stats.append(stats)
            return q_stats

        def get_request_stats(after=None):
            if after is None:
                one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
                after = time.mktime(one_minute_ago.timetuple())
            else:
                # cast to float
                after = float(after)

            logs = logservice.fetch(start_time=after)
            stats = defaultdict(list)
            for req_log in logs:
                stats['start_time'].append(req_log.start_time)
                stats['api_mcycles'].append(req_log.api_mcycles)
                stats['cost'].append(req_log.cost)
                stats['finished'].append(req_log.finished)
                stats['latency'].append(req_log.latency)
                stats['mcycles'].append(req_log.mcycles)
                stats['pending_time'].append(req_log.pending_time)
                stats['replica_index'].append(req_log.replica_index)
                stats['response_size'].append(req_log.response_size)
                stats['version_id'].append(req_log.version_id)
            return stats

        stats = {
            'project_name': app_identity.get_application_id()
        }
        if flavor == 'services' or flavor == 'all':
            global_stat = db_stats.GlobalStat.all().get()
            if global_stat is not None:
                stats['datastore'] = to_dict(global_stat)

            stats['memcache'] = memcache.get_stats()
            stats['task_queue'] = get_task_queue_stats(self.request.get('task_queues', None))

        if flavor == 'requests' or flavor == 'all':
            stats['requests'] = get_request_stats(self.request.get('after', None))

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(stats))


app = webapp2.WSGIApplication([
    ('/datadog', DatadogStats),
])
