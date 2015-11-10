import sys
import time

from measures import Measure
from tornado.util import import_object, unicode_type
from tornado.httpclient import AsyncHTTPClient

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


class MeasuredClientMixIn(object):

    def initialize(self, client, address, dimensions, *args, **kwargs):
        super(MeasuredClientMixIn, self).initialize(*args, **kwargs)

        self.measure = Measure(client, address)
        self.dimensions = dimensions

    def fetch_impl(self, request, callback):
        now = time.time()

        def new_callback(response):
            response_time = time.time() - now
            self.write_metric(request, response, response_time)
            return callback(response)

        return super(MeasuredClientMixIn, self).fetch_impl(request, new_callback)

    def write_metric(self, request, response, response_time):
        dimensions = {
            'url': request.url,
            'host': urlparse(request.url).netloc,
            'status_code': response.code,
            'response_time': response_time
        }

        if self.dimensions:
            dimensions.update(self.dimensions)

        self.measure.count('http_response', dimensions=dimensions)


def setup_measures(client, address, dimensions=None,
                   client_class='tornado.simple_httpclient.SimpleAsyncHTTPClient',
                   **kwargs):

    if isinstance(client_class, (unicode_type, bytes)):
        client_class = import_object(client_class)

    HTTPMeasureClient = type("HTTPMeasureClient",
                             (MeasuredClientMixIn, client_class), {})

    AsyncHTTPClient.configure(
        HTTPMeasureClient, client=client, address=address,
        dimensions=dimensions, **kwargs
    )
