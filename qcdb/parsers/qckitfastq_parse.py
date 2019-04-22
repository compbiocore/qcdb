import glob2
import os
import csv
import logging
from qcdb.parsers.parse import BaseParser

log = logging.getLogger(__name__)

class qckitfastqParser(BaseParser):

    def __init__(self, directory):
        log.info("Initializing qckitfastqParser...")
        BaseParser.__init__(self,directory)

        file_table_dict = {'adapter_content': 'qckitfastq_adaptcontent',
            'gc_content': 'qckitfastq_gccontent', 'kmer_count': 'qckitfastq_kmercount',
            'overrep_kmer': 'qckitfastq_overrep_kmer', 'overrep_reads': 'qckitfastq_overreads',
            'per_base_quality': 'qckitfastq_basequal', 'per_read_quality': 'qckitfastq_readqual',
            'read_length': 'qckitfastq_readlength'}

        sample_id = self.sample_id(base_file)

        for name, table in file_table_dict.items():
            log.info("Parsing {} into {}...".format(name, table))
            self.parse(table, directory, name)

    # data parse
    def parse(self, table, directory, file_suffix):
        files = glob2.glob(os.path.join(directory, '*{}.csv'.format(file_suffix)))
        results = []
        for file in files:
            base_file = os.path.basename(file)
            with open(file, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)

            for row in reader:
                row['sample_id'] = sample_id
                results.append(row)

        self.qcdb_table[table].append(results)
