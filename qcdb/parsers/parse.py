import pandas as pd
import glob2
import os
import re
import logging
from collections import defaultdict
from sqlalchemy import *
from sqlalchemy.orm import Session

log = logging.getLogger(__name__)

class BaseParser(object):
# structure of insert statements is a list of dictionaries
# so we will have a dictionary of a list of dictionaries
# i.e. fastqc_adaptcontent: [{_id: 1, position: 1}, {_id: 1, position: 2}]

    def __init__(self, file_handle, qc_program, session, ref_table, build_ref):
        self.metrics = []
        self.qc_program = qc_program
        base_file = os.path.basename(file_handle)
        sample, experiment, library_read_type = self.get_metadata(base_file)
        self.sample_id = self.sample_id(sample, experiment, library_read_type)
        self.sample_name = sample
        self.experiment = experiment
        self.library_read_type = self.get_library_read_type(library_read_type)
        self.session = session
        self.ref_table = ref_table
        self.build_ref = build_ref
        self.ref_map = self.get_reference_map()

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

    # get the reference map for this qc_program (e.g. {kmercount: {long_name: l}})
    def get_reference_map(self):
        map = {}
        s = select([self.ref_table.c.qc_metric, self.ref_table.c.field_name, self.ref_table.c.field_code].where(self.ref_table.c.qc_program == self.qc_program))
        for row in self.session.execute(s):
            # add metric to map if it doesn't yet exist
            if row['qc_metric'] not in map:
                map[row['qc_metric']] = {}

            map[row['qc_metric']][row['field_name']] = row['field_code']

        return map

    # utility function to create field code
    def get_new_mapping(field_name, codes):
        s = field_name.lower()
        s = re.sub('[^0-9a-zA-Z]+', ' ', s)
        xl = s.split()
        s = re.sub('[^0-9a-zA-Z]+', '', s)
        first_char = 'x'
        for c in s:
            if c.isalpha():
                first_char = c
                break

        # return first alpha if not used
        if first_char not in codes:
            return first_char

        candidate = first_char
        i = 1
        while i < len(xl):
            candidate += xl[i][0]

        # return acronym if not used
        if candidate not in codes:
            return candidate

        # add counter to acronym until not used
        cnt = 1
        while True:
            if candidate + str(cnt) not in codes:
                return candidate + str(cnt)
            cnt += 1

    # create new mapping value from field name to code
    def get_mapped_val(self, metric_type, field_name):
        if not build_ref:
            raise Exception('Can only update reference mappings when buildref set to true')

        if metric_type not in self.ref_map:
            self.ref_map[metric_type] = {}

        # section of the map we need to guaranee uniqueness over
        mmap = self.ref_map[metric_type]

        if field_name in mmap:
            return mmap[field_name]
        else:
            new_val = get_new_mapping(field_name, mmap.values())
            self.ref_map[metric_type][field_name] = new_val
            self.session.execute(self.ref_table.insert(), qc_program=self.qc_program, qc_metric=self.qc_metric, field_name=field_name, field_code=new_val, display_name=field_name)
            return new_val


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
