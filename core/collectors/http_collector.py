# -*- coding: utf-8 -*-
import time
import urllib2
from core.registry import METRIC_REGISTRY
from core.configuration import HTTP_REQUEST_TIMEOUT
from core.collectors.abstract_collector import AbstractCollector


class HTTPCollector(AbstractCollector):

    def _get_metric(self, node, node_dict):
        status_code = 0
        start_time = 0
        end_time = 0
        response = ""
        method = node_dict.get("method").lower()
        url = node_dict.get("url")
        request = urllib2.Request(url)
        if method == "get":
            request.get_method = lambda: 'GET'
        if method == "post":
            request.get_method = lambda: 'POST'
        if method == "head":
            request.get_method = lambda: 'HEAD'

        try:
            start_time = time.time()
            response = urllib2.urlopen(request, timeout=HTTP_REQUEST_TIMEOUT)
            end_time = time.time()
            status_code = str(response.getcode())
            response = response.read()
        except urllib2.HTTPError as error:
            status_code = "%s" % error.code
        except Exception:
            pass

        status_string = "1" if status_code == node_dict.get("status_code") else "0"
        labels_string = self.get_labels_string(node_dict.get("labels"))
        info_string = "endpoint_check{name=\"%s\", url=\"%s\", %s}" % (node, node_dict.get("url"), labels_string)
        METRIC_REGISTRY[info_string] = status_string
        if node_dict.get("check_response_time") and node_dict.get("check_response_time").lower() == "true":
            info_string = "endpoint_check{name=\"%s\", url=\"%s\", %s, validation=\"response_time\"}" % \
                          (node, node_dict.get("url"), labels_string)
            status_string = end_time - start_time
            METRIC_REGISTRY[info_string] = status_string
        if node_dict.get("check_page_non_empty") and node_dict.get("check_page_non_empty").lower() == "true":
            info_string = "endpoint_check{name=\"%s\", url=\"%s\", %s, validation=\"page_non_empty\"}" % \
                          (node, node_dict.get("url"), labels_string)
            status_string = "0" if response == "" else "1"
            METRIC_REGISTRY[info_string] = status_string
