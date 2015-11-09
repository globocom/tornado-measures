from tornado.ioloop import IOLoop
from tornado import gen
from tornado_measures import setup_measures
from tornado.httpclient import AsyncHTTPClient

setup_measures(
    client='MyApplicationName',
    address=('host', 1984),  # logstash host and port
    # optional: if you want to use pycurl instead default tornado client
    client_class = 'tornado.curl_httpclient.CurlAsyncHTTPClient'
)
# don't use AsyncHTTPClient.configure anymore
http_client = AsyncHTTPClient()


@gen.coroutine
def blah():
    response = yield http_client.fetch(
        "http://globo.com/", raise_error=True)

blah()
IOLoop.current().start()
