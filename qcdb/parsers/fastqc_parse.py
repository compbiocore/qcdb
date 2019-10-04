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

        self.parse(file_handle)

    # data parse
    def parse(self, file):
        '''
        read in the results in zipfile and return parsed file
        :return: list of output and tuple with location of modules
        '''
        zp = zf.ZipFile(file,'r')
        results_idx = next((i for i, item in enumerate(zp.namelist()) if re.search('fastqc_data.txt',item)), None)
        lines = zp.open(zp.namelist()[results_idx]).readlines()

        module_end_idx = [i for i, item in enumerate(lines) if re.search('^>>END_MODULE', item.decode('utf-8'))]
        module_start_idx = [i+1 for i in module_end_idx]
        metrics = modules(module_start_idx[:-1],lines)

        for start, end, module in zip(module_start_idx[:-1], module_end_idx[1:], metrics):
            start = start+1 # column names are line after start

            # some edge cases
            if module=='seqdup': # sequence duplicaiton levels come with two comment lines
                start = start+1 # so we just keep the last one for column names

            if start==end: # if module is empty, like overrep sequences
                continue

            columns = lines[start].decode('utf-8').lstrip('#').strip('\n').split('\t')

            if self.build_ref and module not in self.ref_map:
                metric_map = {}
            else:
                try:
                    metric_map = self.ref_map[module]
                except:
                    log.error("No reference map (maybe you need to run with --buildref flag)")
                    raise Exception('No reference map')

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

            # now want dictionary of db_id, qc_program (fastqc), qc_metric (each metric), json
            self.metrics.append({'db_id': self.db_id, 'qc_program': 'fastqc', 'qc_metric': module,
                'data': json_dump(new_cols, rows)})

def modules(start, lines):
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
    modules = []
    for i in start:
        if lines[i].decode('utf-8').startswith(">>Per base sequence quality"):
            modules.append('basequal')
        elif lines[i].decode('utf-8').startswith(">>Per tile"):
            modules.append('tilequal')
        elif lines[i].decode('utf-8').startswith(">>Per sequence quality scores"):
            modules.append('seqqual')
        elif lines[i].decode('utf-8').startswith(">>Per base sequence content"):
            modules.append('perbaseseqcontent')
        elif lines[i].decode('utf-8').startswith(">>Per sequence GC content"):
            modules.append('gccontent')
        elif lines[i].decode('utf-8').startswith(">>Per base N content"):
            modules.append('perbaseNcontent')
        elif lines[i].decode('utf-8').startswith(">>Sequence Length Distribution"):
            modules.append('seqlength')
        elif lines[i].decode('utf-8').startswith(">>Sequence Duplication"):
            modules.append('seqdup')
        elif lines[i].decode('utf-8').startswith(">>Overrepresented sequences"):
            modules.append('overseqs')
        elif lines[i].decode('utf-8').startswith(">>Adapter"):
            modules.append('adaptcontent')
        elif lines[i].decode('utf-8').startswith(">>Kmer Content"):
            modules.append('kmercount')
        else:
            raise Exception("No modules known to be fastqc found")
            log.error("No modules known to be fastqc found")
    return modules