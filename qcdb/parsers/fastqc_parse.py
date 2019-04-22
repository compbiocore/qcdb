import pandas as pd
import glob2
import os
import zipfile as zf, re
import logging
import oyaml as yaml
from io import BytesIO
from parsers.parse import BaseParser

log = logging.getLogger(__name__)

class fastqcParser(BaseParser):
    def __init__(self, file_handle):
        log.info("Initializing fastqcParser...")
        BaseParser.__init__(self,file_handle)#, 'tables/fastqc.yaml')
        print(self.sample_id)

        with open('tables/fastqc.yaml', 'r') as io:
            d = yaml.load(io)

        self.parse(file_handle, d)

    # data parse
    # largely taken from: https://github.com/compbiocore/bioflows/blob/master/bioflows/bioutils/parse_fastqc/parsefastqc.py
    def parse(self, file, table_structure):
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
        del(module_start_idx[9])
        print(module_start_idx)
        module_end_idx = [i for i, item in enumerate(lines) if re.search('^>>END_MODULE', item.decode('utf-8'))]
#        module_start_idx = 
        #module_start_idx = sorted(list(set(module_start_idx) - set(module_end_idx)))

        for start, end, module in zip(module_start_idx[2:], module_end_idx[1:], table_structure):
            rows = lines[start+1:end-1]
            print(start)
            table = module['table']
            columns = [m['name'] for m in module['columns']]
            types = [self.change_type(m['type']) for m in module['columns']]
            b = BytesIO()
            for r in rows:
                b.write(r)
            log.info("did this work")
            print(columns)
            print(types)
#            print(b.getvalue())
            b.seek(0)
            df = pd.read_csv(b, sep='\t', names=columns, dtype=dict(zip(columns,types)))
            df['sample_id'] = self.sample_id
            self.tables[module['table']] = df.to_dict(orient="records")
#            self.tables[module['table']] = [dict(zip(columns, r.decode('utf-8').split('\t').strip('\n'))) for r in rows]