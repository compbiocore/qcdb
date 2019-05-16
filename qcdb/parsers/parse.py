import pandas as pd
import glob2
import os
import logging
from collections import defaultdict

log = logging.getLogger(__name__)

class BaseParser(object):
# structure of insert statements is a list of dictionaries
# so we will have a dictionary of a list of dictionaries
# i.e. fastqc_adaptcontent: [{_id: 1, position: 1}, {_id: 1, position: 2}]

    def __init__(self, file_handle):#, table_yaml):
        self.metrics = []
        #self.yaml = table_yaml
        base_file = os.path.basename(file_handle)
        sample, experiment, library_read_type = self.get_metadata(base_file)
        self.sample_id = self.sample_id(sample, experiment, library_read_type)
        self.sample_name = sample
        self.experiment = experiment
        self.library_read_type = self.get_library_read_type(library_read_type)

    def change_type(self, type_):
        if type_ == 'Integer':
            return int
        if type_ == 'Float':
            return float
        else:
            return str

    def get_metadata(self, base_file):
        sample=base_file.split('_')[0]
        experiment=base_file.split('_')[1]
        library_read_type=base_file.split('_')[2]
        if library_read_type[0].isalpha(): # single-end
            library_read_type = 'se'

        return (sample,
                experiment,
                library_read_type)

    def sample_id(self, sample, experiment, library_read_type):
        return(sample+'_'+experiment+'_'+library_read_type)


    def get_library_read_type(self, library_read_type):
        if library_read_type == '1':
            return 'paired-end forward'
        if library_read_type == '2':
            return 'paired-end reverse'
        if library_read_type.isalpha():
            return 'single ended' 
        else:
            raise KeyError("Library read type not recognized.")

    # create metadata table
    def metadata(self, directory):
        files = glob2.glob(os.path.join(directory, '*'))
        log.info("files: {}".format(files))
        metadata_df = pd.DataFrame()
        for f in files:
            base_file = os.path.basename(f)

            sample, experiment, library_read_type = self.get_metadata(base_file)
            _id = self.sample_id(sample, experiment, library_read_type)

            row = pd.DataFrame({'sample_id': _id,
                                 'sample_name': sample,
                                 'library_read_type': self.get_library_read_type(base_file),
                                 'experiment': experiment}, index=[0])

            metadata_df = metadata_df.append(row)

        return metadata_df.drop_duplicates()
