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
    def __init__(self, file_handle, session, ref_table, build_ref):
        log.info("Initializing fastqcParser for {}...".format(file_handle))
        BaseParser.__init__(self,file_handle,'fastqc', session, ref_table, build_ref)

        metrics = ['basequal', 'tilequal', 'seqqual', 'perbaseseqcontent',
            'gccontent', 'perbaseNcontent', 'seqlength', 'seqdup', 'overseqs',
            'adaptcontent', 'kmercount']

        self.parse(file_handle, metrics)

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
            # pre-mapped column names
            columns = lines[start].decode('utf-8').lstrip('#').strip('\n').split('\t')

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

            rows = lines[start+1:end-1]

            # if no data right now JSON will be empty. OK solution?

            # now want dictionary of sample_id, qc_program (fastqc), qc_metric (each metric), json
            self.metrics.append({'sample_id': self.sample_id, 'qc_program': 'fastqc', 'qc_metric': module,
                'data': json_dump(new_cols, rows)})
