#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import socket
from BaseHTTPServer import HTTPServer

from core.server import MetricsHandler
from core.collectors.http_collector import HTTPCollector
from core.collectors.cli_collector import CliCollector
from core.collectors.mvd_collector import MVDCollector
from core.collectors.process_collector import ProcessCollector
from core.collectors.process_count_collector import ProcessCountCollector

from core.configuration import *

__author__ = "D.Kruchek, E.Bukatkin"
__copyright__ = "Copyright 2018, Lifetech LLC"


def get_config():
    config = None
    hostname = socket.gethostname()
    cwd = os.path.dirname(os.path.realpath(__file__))
    conf_path = os.path.join(cwd, "config/%s/config.json" % hostname)
    try:
        with open(conf_path, "r") as config:
            config = json.loads(config.read())
    except Exception as error:
        print(error)
        print("Please make sure the file %s is present on host." % conf_path)
        quit(1)
    return config


def main():
    config = get_config()

    for section in config.keys():
        if section == HTTP_SECTION:
            h_collector = HTTPCollector(config, HTTP_SECTION)
            h_collector.start()
        if section == VALIDATOR_SECTION:
            m_collector = MVDCollector(config, VALIDATOR_SECTION)
            m_collector.start()
        if section == PROCESS_SECTION:
            p_collector = ProcessCollector(config, PROCESS_SECTION)
            p_collector.start()
        if section == CLI_SECTION:
            c_collector = CliCollector(config, CLI_SECTION)
            c_collector.start()
        if section == PROCESS_COUNTER_SECTION:
            pc_collector = ProcessCountCollector(config, PROCESS_COUNTER_SECTION)
            pc_collector.start()

    address = ("", SERVER_PORT)
    print("Starting http server on port %s ..." % SERVER_PORT)
    try:
        server = HTTPServer(address, MetricsHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        os._exit(1)


if __name__ == "__main__":
    main()
