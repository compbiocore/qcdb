import pandas as pd
import glob2
import os
import json
import zipfile as zf, re
import logging
import oyaml as yaml
from io import BytesIO
from qcdb.parsers.parse import BaseParser

log = logging.getLogger(__name__)
dirname = os.path.dirname(__file__)

def json_dump(columns, rows):
    json_list = []
    for r in rows:
        json_list.append({ columns[i]: r.decode('utf-8').strip('\n').split('\t')[i] for i in range(len(columns))})
    return(json_list)

class fastqcParser(BaseParser):
    def __init__(self, file_handle):
        log.info("Initializing fastqcParser...")
        BaseParser.__init__(self,file_handle,'fastqc')

        metrics = ['basequal', 'tilequal', 'seqqual', 'perbaseseqcontent',
            'gccontent', 'perbaseNcontent', 'seqlength', 'seqdup', 'overseqs',
            'adaptcontent', 'kmercount']
        self.parse(file_handle, metrics)

        #with open(os.path.join(os.path.dirname(dirname),'tables/fastqc.yaml'), 'r') as io:
        #    d = yaml.load(io)
        #self.parse(file_handle, d)

    # data parse
    # largely taken from: https://github.com/compbiocore/bioflows/blob/master/bioflows/bioutils/parse_fastqc/parsefastqc.py
    def parse(self, file, metrics):
        '''
        read in the results in zipfile and return parsed file
        :return: list of output and tuple with location of modules
        '''
        zp = zf.ZipFile(file,'r')
        results_idx = next((i for i, item in enumerate(zp.namelist()) if re.search('fastqc_data.txt',item)), None)
        lines = zp.open(zp.namelist()[results_idx]).readlines()

        # Generate a tuple for the start and end locs of the modules 12 in total
            # ['>>Basic Statistics\tpass\n',
            #  '>>Per base sequence quality\tpass\n',
            #  '>>Per tile sequence quality\twarn\n',
            #  '>>Per sequence quality scores\tpass\n',
            #  '>>Per base sequence content\twarn\n',
            #  '>>Per sequence GC content\tpass\n',
            #  '>>Per base N content\tpass\n',
            #  '>>Sequence Length Distribution\tpass\n',
            #  '>>Sequence Duplication Levels\tfail\n',
            #  '>>Overrepresented sequences\twarn\n',
            #  '>>Adapter Content\tpass\n',
            #  '>>Kmer Content\tfail\n']

        module_start_idx = [i for i, item in enumerate(lines) if re.search('#', item.decode('utf-8'))]
        del(module_start_idx[9]) # sequence duplication levels has two comment lines so we wonly want the last one
        module_end_idx = [i for i, item in enumerate(lines) if re.search('^>>END_MODULE', item.decode('utf-8'))]

        for start, end, module in zip(module_start_idx[2:], module_end_idx[1:], metrics):
            columns = lines[start].decode('utf-8').lstrip('#').strip('\n').split('\t')
            rows = lines[start+1:end-1]

            # if no data right now JSON will be empty. OK solution?
            
            # now want dictionary of sample_id, qc_program (fastqc), qc_metric (each metric), json
            self.metrics.append({'sample_id': self.sample_id, 'qc_program': 'fastqc', 'qc_metric': module,
                'data': json_dump(columns, rows)})