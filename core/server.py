# -*- coding: utf-8 -*-
from __future__ import print_function
from core.registry import METRIC_REGISTRY

try:
    from http.server import BaseHTTPRequestHandler
except:
    from BaseHTTPServer import BaseHTTPRequestHandler


class MetricsHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.serve()

    def do_GET(self):
        self.serve()

    def serve(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # Get all unique metrics names from registry
        _metrics = set([m.rpartition("{")[0] for m in METRIC_REGISTRY.keys()])

        for metric in _metrics:
            self.wfile.write(bytes("# HELP %s Information about lifetech %s.\n" % (metric, metric)))
            self.wfile.write(bytes("# TYPE %s gauge\n" % metric))
            for meta, status in METRIC_REGISTRY.items():
                if metric in meta:
                    self.wfile.write(bytes("%s %s\n" % (meta, status)))
