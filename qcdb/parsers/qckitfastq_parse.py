import glob2
import os
import csv
import json
import logging
import pandas as pd
import oyaml as yaml
from qcdb.parsers.parse import BaseParser

log = logging.getLogger(__name__)
dirname = os.path.dirname(__file__)

class qckitfastqParser(BaseParser):

    def __init__(self, file_handle, session, ref_table, build_ref):
        log.info("Initializing qckitfastqParser...")
        BaseParser.__init__(self,file_handle,'qckitfastq', session, ref_table, build_ref)

        file_table_dict = {'adapter_content': 'adaptcontent',
            'gc_content': 'gccontent', 'kmer_count': 'kmercount',
            'overrep_kmer': 'overkmer', 'overrep_reads': 'overreads',
            'per_base_quality': 'basequal', 'per_read_quality': 'readqual',
            'read_length': 'readlength', 'read_content': 'readcontent'}

        base_file = os.path.basename(file_handle)
        if self.library_read_type == 'single ended':
            file_type = base_file.split('{}_{}_'.format(self.sample_name,self.experiment))[1]
        else:
            file_type = base_file.split('{}_{}_?_'.format(self.sample_name,self.experiment))[1]
        metric = file_table_dict[file_type[:-4]]

        self.parse(metric, file_handle)

    # data parse
    def parse(self, module, file_handle):
        with open(file_handle, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            # update column names
            columns = csv_reader.fieldnames

            if self.build_ref and module not in self.ref_map:
                metric_map = {}
            else:
                metric_map = self.ref_map[module]

            new_cols = []
            for column in columns:
                if column in metric_map:
                    new_cols.append(metric_map[column])
                elif self.build_ref:
                    new_col = self.get_mapped_val(module, column)
                    metric_map[column] = new_col
                    new_cols.append(new_col)
                else:
                    log.error("Metric type does not have a mapped code (maybe you need to run with --buildref flag?)")
                    raise Exception('Metric type does not have a mapped code')

            new_csv_reader = csv.DictReader(csv_file, fieldnames=new_cols)

            self.metrics.append({'sample_id': self.sample_id, 'qc_program': 'qckitfastq', 'qc_metric': module,
            'data': json.loads(json.dumps([ row for row in new_csv_reader ]))})
