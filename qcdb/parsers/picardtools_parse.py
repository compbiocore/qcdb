#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 13:36:11 2019

@author: jwalla12
"""

from qcdb.parsers.parse import BaseParser
import json, logging, os, glob2, re

log = logging.getLogger(__name__)

class picardtoolsParser(BaseParser):
    
    def __init__(self, file_handle):
        log.info("Initializing picardtoolsParser...")
        BaseParser.__init__(self,file_handle)
        programs = ['alignment_metrics_picard.txt', 'insertsize_metrics_picard.txt', 'summary_gcbias_metrics_picard.txt']        
        self.parse(programs, os.path.dirname(file_handle))

    def parse(self, programs, directory):
        for program in programs:
            files = glob2.glob(os.path.join(directory, '*'+program))
            for file in files:
                f = open(file, 'r', encoding = "ISO-8859-1")           
                content = f.read()
                m = re.search(r"METRICS\sCLASS\s*(\w+)\.[^.]*\.(\w+)\n([^\n]+)\n(([^\n#]+\n)+)", content)
                qc_program = m.group(1)
                qc_metric = m.group(2)
                header = m.group(3)
                d = m.group(4)
                p = re.search(r"^(PAIR|UNPAIRED)[^\n]*", m.group(4), flags=re.M)
                if p:
                    d = p.group(0)
                data = d.strip("\n").split("\t")
                data_dictionary = dict(zip(header, data))
                json_table = json.dumps(data_dictionary)
                picard_dict = dict(
                    {'sample_id': self.sample_id, 'qc_program': qc_program, 'qc_metric': qc_metric, 'json': json_table})
            self.metrics.append(picard_dict)
