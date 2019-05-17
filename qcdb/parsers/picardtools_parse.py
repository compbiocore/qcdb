#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 13:36:11 2019

@author: jwalla12
"""

from qcdb.parsers.parse import BaseParser
import json, logging


log = logging.getLogger(__name__)
dirname = os.path.dirname(__file__)

class picardtoolsParser(BaseParser):
    def __init__(self, file_handle):
        log.info("Initializing picardtoolsParser...")
        BaseParser.__init__(self,file_handle)
        self.parse(file_handle)

    def parse(self, file):
        f = open(file, 'r', encoding = "ISO-8859-1")           
        contents = f.readlines()    
        for i, content in enumerate(contents):
            if 'METRICS CLASS' in content:
                qc_program = content.strip("\n").split(".")[-3].split("\t")[-1] 
                qc_metric = content.strip("\n").split(".")[-1]    
                header = (contents[i+1]).strip("\n").split("\t")
                
                if qc_metric == 'AlignmentSummaryMetrics':
                    if 'PAIR' in content:
                        row = content.strip("\n").split("\t")
                    elif 'UNPAIRED' in content:
                        row = content.strip("\n").split("\t")   
                        
                elif (qc_metric == 'InsertSizeMetrics') or (qc_metric == 'GcBiasSummaryMetrics'):
                    row = (contents[i+2]).strip("\n").split("\t")
                   
                else:
                    print('Not a valid picard tools output file, must be output from CollectAlignmentSummaryMetrics, CollectInsertSizeMetrics, or summary metrics from CollectGcBiasMetrics')        
                        
        data_dictionary = dict(zip(header,row)) #create dictionary of header and row
        json_table = json.dumps(data_dictionary) #create json from dictionary
        picard_dict = dict({'sample_id': self.sample_id, 'qc_program': qc_program, 'qc_metric': qc_metric, 'json': json_table})            
        return(picard_dict)


