# -*- coding: utf-8 -*-
import time
from threading import Thread
from core.configuration import COLLECT_METRICS_INTERVAL


class AbstractCollector(Thread):

    config = None

    def __init__(self, config, section):
        super(AbstractCollector, self).__init__()
        self.config = config
        self.section_items = self.config.get(section).items()

    @staticmethod
    def get_labels_string(section_dict):
        labels = []
        for key, value in section_dict.items():
            labels.append("%s=\"%s\"" % (key, value))
        return ",".join(labels)

    def run(self):
        while True:
            threads = []
            for item, item_dict in self.section_items:
                thread = Thread(target=self._get_metric, args=(item, item_dict))
                threads.append(thread)
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            time.sleep(COLLECT_METRICS_INTERVAL)

    def _get_metric(self, node, node_dict):
        raise NotImplementedError
