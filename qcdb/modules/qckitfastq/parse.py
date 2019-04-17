import glob2
import os
import csv

class qckitfastqParser(BaseParser):

    def __init__(self, infile)
        self.infile = file_handle

    file_table_dict = {'adapter_content': qckitfastq_adaptcontent,
        'gc_content': qckitfastq_gccontent, kmer_count: qckitfastq_kmercount,
        overrep_kmer: qckitfastq_overrep_kmer, overrep_reads: qckitfastq_overreads,
        per_base_quality: qckitfastq_basequal, per_read_quality: qckitfastq_readqual,
        read_length: qckitfastq_readlength}

    for name, table in file_table_dict.values():
        self.parse(self, table, directory, name)

    # data parse
    def parse(self, table, directory, file_suffix):
        files = glob2.glob(os.path.join(directory, '*{}.csv'.format(file_suffix)))

        sample_id = sample_id(base_file)
        results = []
        for file in files:
            base_file = os.path.basename(file)
            with open(file, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)

            for row in reader:
                row['sample_id'] = sample_id
                results.append(row)

        self.qcdb_table[table].append(results)

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
