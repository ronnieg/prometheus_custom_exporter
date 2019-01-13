# -*- coding: utf-8 -*-
import re
import platform
import subprocess
from core.registry import METRIC_REGISTRY
from core.collectors.abstract_collector import AbstractCollector


class ProcessCountCollector(AbstractCollector):

    CURRENT_OS = platform.system()

    if CURRENT_OS == 'HP-UX':
        CMD = 'UNIX95= ps -eo args | sort | uniq -c | sort -rn'
    else:
        CMD = 'ps -eo cmd | sort | uniq -c | sort -rn'

    def _get_metric(self, node, node_dict):

        cmd_out = subprocess.Popen([self.CMD], stdout=subprocess.PIPE, shell=True)
        cmd_stdout = cmd_out.stdout.read().strip()

        pattern = re.compile(r'(?P<count>^\d+)\s+(?P<proc_name>.*)')
        match = pattern.match(cmd_stdout)
        count = match.group('count')
        proc_name = match.group('proc_name')

        labels_string = self.get_labels_string(node_dict.get('labels'))

        info_string = 'process_counter{process_name=\"%s\", %s}' % (proc_name, labels_string)
        METRIC_REGISTRY[info_string] = count
