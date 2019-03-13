import pandas as pd
import glob2
import os

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

# data parse
def parse(directory, file_suffix, columns=False):
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
