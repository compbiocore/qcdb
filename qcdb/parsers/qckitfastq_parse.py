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

        file_table_dict = {'adaptcontent': 'adapter_content',
            'gccontent': 'gc_content', 'kmercount': 'kmer_count',
            'overkmer': 'overrep_kmer', 'overreads': 'overrep_reads',
            'basequal': 'per_base_quality', 'readqual': 'per_read_quality',
            'readlength': 'read_length', 'readcontent': 'read_content'}

        self.parse(file_table_dict, os.path.dirname(file_handle))
            #self.parse(table, os.path.dirname(file_handle), name, d)

    # data parse
    def parse(self, ft_dict, directory):
        for module, name in ft_dict.items():
            log.info("Parsing {} into {}...".format(name, module))
            files = glob2.glob(os.path.join(directory,
                '{}_{}_*{}.csv'.format(self.sample_name,self.experiment,name)))
            for file in files:

                with open(file, 'r') as csv_file:
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
                            raise Exception('Metric type does not have a mapped code')

                    new_csv_reader = csv.DictReader(csv_file, fieldnames=new_cols)

                    self.metrics.append({'sample_id': self.sample_id, 'qc_program': 'qckitfastq', 'qc_metric': module,
                    'data': json.loads(json.dumps([ row for row in new_csv_reader ]))})
