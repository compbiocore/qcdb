import pandas as pd
import glob2
import os
import zipfile as zf, re
import logging

from qcdb.parse import get_metadata

class fastqcParser(BaseParser):
    super(FASTQCParser, self).__init__(name='FASTQC')

    self.parse()

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

    def get_metadata(base_file):
        sample=base_file.split('_')[0]
        experiment=base_file.split('_')[1]
        library_read_type=base_file.split('_')[2]

        return (sample,
                experiment,
                library_read_type)

def sample_id(base_file):
    sample, experiment, library_read_type = get_metadata(base_file)
    if library_read_type.isalpha():
        library_read_type =  'se'
    return(sample+'_'+experiment+'_'+library_read_type)


def get_library_read_type(base_file):

    sample, experiment, library_read_type = get_metadata(base_file)

    if library_read_type == '1':
        return 'paired-end forward'
    if library_read_type == '2':
        return 'paired-end reverse'
    if library_read_type.isalpha():
        return 'single ended'

# create metadata table
def metadata(directory):
    files = glob2.glob(os.path.join(directory, '*'))
    metadata_df = pd.DataFrame()
    for f in files:
        base_file = os.path.basename(f)

        sample, experiment, library_read_type = get_metadata(base_file)
        _id = sample_id(base_file)

        row = pd.DataFrame({'sample_id': _id,
                             'sample_name': sample,
                             'library_read_type': get_library_read_type(base_file),
                             'experiment': experiment}, index=[0])

        metadata_df = metadata_df.append(row)

    return metadata_df.drop_duplicates()
