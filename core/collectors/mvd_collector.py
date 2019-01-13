# -*- coding: utf-8 -*-
import urllib2
from core.registry import METRIC_REGISTRY
from core.configuration import HTTP_REQUEST_TIMEOUT
from core.collectors.abstract_collector import AbstractCollector


class MVDCollector(AbstractCollector):

    def _get_metric(self, node, node_dict):
        """
        @type node: string
        @type node_dict: dict
        """
        content = ""
        labels_string = self.get_labels_string(node_dict.get("labels"))
        info_string = "validator_check{%s}" % labels_string

        try:
            with open(node_dict.get("body"), "r") as body:
                req = urllib2.Request(url=node_dict.get("url"),
                                      data=body.read(),
                                      headers={'Content-Type': 'text/xml'})
                response = urllib2.urlopen(req, timeout=HTTP_REQUEST_TIMEOUT)
                content = response.read().decode('utf-8')
        except Exception:
            pass

        status_string = "1" if node_dict.get("string_to_check") in content else "0"
        METRIC_REGISTRY[info_string] = status_string
