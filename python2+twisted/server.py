import sys
import logging

from twisted.internet import reactor, defer
from twisted.web.client import getPage
from twisted.web.client import Agent, HTTPConnectionPool, readBody
from twisted.python import log
import cyclone.web

def sleep(n):
    '''Sleep n seconds inside reactor without blocking other co-routines.
    :param n: float
    :return: Deferred()
    '''
    d = defer.Deferred()
    reactor.callLater(n, d.callback, True)
    return d

class RootHandler(cyclone.web.RequestHandler):
    def get(self):
        text = 'Hello from python2.7+twisted'
        self.write(text)

class CpuLoad(cyclone.web.RequestHandler):
    def get(self):
        min_value = int(self.get_argument('min', 1))
        max_value = int(self.get_argument('max', 1000))
        s = sum(range(min_value, max_value + 1))
        text = 'sum({}..{})={}'.format(min_value, max_value, s)
        self.write(text)


class SlowResp(cyclone.web.RequestHandler):
    @defer.inlineCallbacks
    def get(self):
        timeout = float(self.get_argument('timeout', 1.0))
        yield sleep(timeout)
        text = 'Slow hello from python2.7+twisted'
        self.write(text)

class OldGateway(cyclone.web.RequestHandler):
    @defer.inlineCallbacks
    def get(self):
        url = str(self.get_argument('url', 'http://localhost'))
        resp = yield getPage(url, method='GET')
        self.write(resp)

class Gateway(cyclone.web.RequestHandler):
    @defer.inlineCallbacks
    def get(self):
        url = str(self.get_argument('url', 'http://localhost'))
        resp = yield self.application.agent.request('GET', url)
        body = yield readBody(resp)
        self.write(body)

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s')
    logging.root.setLevel(logging.ERROR)

    pool = HTTPConnectionPool(reactor)
    pool.maxPersistentPerHost = 100
    agent = Agent(reactor, pool=pool)

    application = cyclone.web.Application([
        (r'/', RootHandler),
        (r'/cpu_load', CpuLoad),
        (r'/slow_resp', SlowResp),
        (r'/gateway', Gateway),
        (r'/old_gateway', OldGateway),
    ])
    application.agent = agent

    observer = log.PythonLoggingObserver()
    observer.start()

    reactor.listenTCP(2700, application)
    reactor.run()
