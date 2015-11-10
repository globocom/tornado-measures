from tornado.httpclient import AsyncHTTPClient
from tornado.testing import gen_test, AsyncTestCase
from mock import MagicMock
from tornado_measures import setup_measures


class TornadoMeasuresTestCase(AsyncTestCase):

    def setUp(self):
        super(TornadoMeasuresTestCase, self).setUp()

        response = MagicMock()
        response.code = 201
        response.error = None

        class MyHTTPClient(AsyncHTTPClient):

            def fetch_impl(self, request, callback):
                callback(response)

        setup_measures(
            client='my-test-app',
            address=('localhost', 123),
            dimensions={'tsuru-appname': 'My-App'},
            client_class=MyHTTPClient,
        )

        self.response = response
        self.client = AsyncHTTPClient()

    @gen_test
    def test_write_metric(self):
        self.client.measure.count = MagicMock()
        yield self.client.fetch('http://globo.com/g1')

        metric = self.client.measure.count.call_args[0][0]
        self.assertEqual(metric, 'http_response')

        dimensions = self.client.measure.count.call_args[1]['dimensions']
        self.assertEqual(dimensions['url'], 'http://globo.com/g1')
        self.assertEqual(dimensions['status_code'], 201)
        self.assertEqual(dimensions['host'], 'globo.com')
        self.assertEqual(dimensions['tsuru-appname'], 'My-App')
