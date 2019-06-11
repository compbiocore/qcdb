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

            #     columns = [m['name'] for m in module['columns']]
            #     types = [self.change_type(m['type']) for m in module['columns']]
            #     df = pd.read_csv(file, sep=',', names=columns,skiprows=1,dtype=dict(zip(columns,types)))
            #     df['sample_id'] = self.sample_id
            #     self.tables[module['table']] = df.to_dict(orient="records")
                with open(file, 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    self.metrics.append({'sample_id': self.sample_id, 'qc_program': 'qckitfastq', 'qc_metric': module,
                    'data': json.loads(json.dumps([ row for row in csv_reader ]))})
