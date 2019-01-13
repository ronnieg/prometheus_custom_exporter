# -*- coding: utf-8 -*-
import subprocess
from core.registry import METRIC_REGISTRY
from core.collectors.abstract_collector import AbstractCollector


class ProcessCollector(AbstractCollector):

    def _get_metric(self, node, node_dict):
        cmd = "ps -ef | grep \"%s\" | grep -cv grep" % node_dict.get("search_name")
        process_count = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        process_count = process_count.stdout.read().strip()
        labels_string = self.get_labels_string(node_dict.get("labels"))
        info_string = "process_check{process_name=\"%s\", %s}" % (node, labels_string)
        METRIC_REGISTRY[info_string] = process_count
