import glob2
import os
import csv
import logging
import pandas as pd
import oyaml as yaml
from qcdb.parsers.parse import BaseParser

log = logging.getLogger(__name__)
dirname = os.path.dirname(__file__)

class qckitfastqParser(BaseParser):

    def __init__(self, file_handle):
        log.info("Initializing qckitfastqParser...")
        BaseParser.__init__(self,file_handle)

        with open(os.path.join(os.path.dirname(dirname),'tables/qckitfastq.yaml'), 'r') as io:
            d = yaml.load(io)

        file_table_dict = {'qckitfastq_adaptcontent': 'adapter_content',
            'qckitfastq_gccontent': 'gc_content', 'qckitfastq_kmercount': 'kmer_count',
            'qckitfastq_overkmer': 'overrep_kmer', 'qckitfastq_overreads': 'overrep_reads',
            'qckitfastq_basequal': 'per_base_quality', 'qckitfastq_readqual': 'per_read_quality',
            'qckitfastq_readlength': 'read_length', 'qckitfastq_readcontent': 'read_content'}

        self.parse(file_table_dict, os.path.dirname(file_handle), d)
            #self.parse(table, os.path.dirname(file_handle), name, d)

    # data parse
    #def parse(self, table, directory, file_suffix, table_structure):
    def parse(self, ft_dict, directory, table_structure):
        for module in table_structure:
            table = module['table']
            name = ft_dict[table]
            log.info("Parsing {} into {}...".format(name, table))
            files = glob2.glob(os.path.join(directory,
                '{}_{}_*{}.csv'.format(self.sample_name,self.experiment,name)))
            for file in files:
                base_file = os.path.basename(file)
                columns = [m['name'] for m in module['columns']]
                types = [self.change_type(m['type']) for m in module['columns']]
                df = pd.read_csv(file, sep=',', names=columns,skiprows=1,dtype=dict(zip(columns,types)))
                df['sample_id'] = self.sample_id
                self.tables[module['table']] = df.to_dict(orient="records")
            #with open(file, 'r') as csv_file:
                #csv_reader = csv.DictReader(csv_file)

                #for row in csv_reader:
                #    row['sample_id'] = self.sample_id

                #    results.append(row)

        #self.qcdb_table[table].append(results)
