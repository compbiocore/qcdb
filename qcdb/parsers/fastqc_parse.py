import pandas as pd
import glob2
import os
import zipfile as zf, re
import logging
from parsers.parse import BaseParser

class fastqcParser(BaseParser):
    def __init__(self, infile):
        super(FASTQCParser, self).__init__(name='FASTQC')

        self.parse(directory, name)

    # data parse
    # largely taken from: https://github.com/compbiocore/bioflows/blob/master/bioflows/bioutils/parse_fastqc/parsefastqc.py
    def parse(self, directory, file, columns=False):
        '''
        read in the results in zipfile and return parsed file
        :return: list of output and tuple with location of modules
        '''
        zp = zf.ZipFile(os.path.join(directory, file),'r')
        results_idx = next((i for i, item in enumerate(zp.namelist()) if re.search('fastqc_data.txt',item)), None)
        self.parsed_results = zp.open(zp.namelist()[results_idx]).readlines()

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

        files = glob2.glob(os.path.join(directory, '*{}.csv'.format(file_suffix)))
        df = pd.DataFrame()

        for file in files:
            base_file = os.path.basename(file)
            data = pd.read_table(file, sep=',')
            if columns:
                data = data[columns]

            data['sample_id'] = sample_id(base_file)

            df = df.append(data, ignore_index=True)

        return(df)