# -*- coding: utf-8 -*-
import subprocess
from core.registry import METRIC_REGISTRY
from core.collectors.abstract_collector import AbstractCollector


class CliCollector(AbstractCollector):

    def _get_metric(self, node, node_dict):
        cmd = node_dict.get("command".format(node_dict.get("args")))
        out = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = out.communicate()
        labels_string = self.get_labels_string(node_dict.get("labels"))
        info_string = "commandline_check{name=\"%s\",%s}" % (node, labels_string)

        # return both stdout and stderr in one string
        METRIC_REGISTRY[info_string] = stdout.strip() + stderr.strip()
