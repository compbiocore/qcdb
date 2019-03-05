import pandas as pd
import glob2
import argparse
import os

parser=argparse.ArgumentParser()
parser.add_argument('-d', nargs=1, required=True, dest='directory', help='path to qckitfastq output directory')
args=parser.parse_args()

#adapters
adapter_content_files = glob2.glob(args.directory[0]+'*_adapter_content.csv') 
adapter_content_table=pd.DataFrame()
for adapter_file in adapter_content_files:
    base_file=os.path.basename(adapter_file)
    sample=base_file.split('_')[0]
    experiment=base_file.split('_')[1]
    library_read_type=base_file.split('_')[2]
    adapter_content=pd.read_table(adapter_file, sep=',')
    adapter_content['sample_id']=sample+'_'+experiment   
    if library_read_type == '1':
        adapter_content['library_read_type'] = 'pe_1'
    if library_read_type == '2':
        adapter_content['library_read_type'] = 'pe_2'
    if library_read_type.isalpha():
        adapter_content['library_read_type'] = 'se'
    adapter_content_table=adapter_content_table.append(adapter_content, ignore_index=True)
    

#GC content
gc_content_files = glob2.glob(args.directory[0]+'*_gc_content.csv') 
gc_content_table=pd.DataFrame()
for gc_file in gc_content_files:
    base_file=os.path.basename(gc_file)
    sample=base_file.split('_')[0]
    experiment=base_file.split('_')[1]
    library_read_type=base_file.split('_')[2]
    gc_content=pd.read_table(gc_file, sep=',')
    gc_content = gc_content[['read','mean_GC']]
    gc_content['sample_id']=sample+'_'+experiment 
    if library_read_type == '1':
        gc_content['library_read_type'] = 'pe_1'
    if library_read_type == '2':
        gc_content['library_read_type'] = 'pe_2'
    if library_read_type.isalpha():
        gc_content['library_read_type'] = 'se'
    gc_content_table=gc_content_table.append(gc_content, ignore_index=True)


#overrep kmer
overrep_kmer_files = glob2.glob(args.directory[0]+'*_overrep_kmer.csv') 
overrep_kmer_table=pd.DataFrame()
for overrep_kmer_file in overrep_kmer_files:
    base_file=os.path.basename(overrep_kmer_file)
    sample=base_file.split('_')[0]
    experiment=base_file.split('_')[1]
    library_read_type=base_file.split('_')[2]
    overrep_kmer=pd.read_table(overrep_kmer_file, sep=',')
    overrep_kmer = overrep_kmer[['row','position','obsexp_ratio','kmer']]
    overrep_kmer['sample_id']=sample+'_'+experiment
    if library_read_type == '1':
        overrep_kmer['library_read_type'] = 'pe_1'
    if library_read_type == '2':
        overrep_kmer['library_read_type'] = 'pe_2'
    if library_read_type.isalpha():
        overrep_kmer['library_read_type'] = 'se'         
    overrep_kmer_table=overrep_kmer_table.append(overrep_kmer, ignore_index=True)

#kmer counts 
kmer_counts_files = glob2.glob(args.directory[0]+'*kmer_count.csv') 
kmer_counts_table=pd.DataFrame()
for kmer_counts_file in kmer_counts_files:
    base_file=os.path.basename(kmer_counts_file)
    sample=base_file.split('_')[0]
    experiment=base_file.split('_')[1]
    library_read_type=base_file.split('_')[2]
    kmer_counts=pd.read_table(kmer_counts_file, sep=',')
    kmer_counts.rename(columns={kmer_counts.columns[0]:'kmer'}, inplace=True) #name the first 0-indexed column 'kmer'
    kmer_counts = pd.melt(kmer_counts, id_vars=['kmer']) #melt the dataframe but specify that the id_vars is the 'kmer' column
    kmer_counts['sample_id']=sample+'_'+experiment
    if library_read_type == '1':
        kmer_counts['library_read_type'] = 'pe_1'
    if library_read_type == '2':
        kmer_counts['library_read_type'] = 'pe_2'
    if library_read_type.isalpha():
        kmer_counts['library_read_type'] = 'se'         
    kmer_counts_table=kmer_counts_table.append(kmer_counts, ignore_index=True)    
    

##overrepresented reads
overrep_reads_files = glob2.glob(args.directory[0]+'*overrep_reads.csv') 
overrep_reads_table=pd.DataFrame()
for overrep_reads_file in overrep_reads_files:
    base_file=os.path.basename(overrep_reads_file)
    sample=base_file.split('_')[0]
    experiment=base_file.split('_')[1]
    library_read_type=base_file.split('_')[2]
    overrep_reads=pd.read_table(overrep_reads_file, sep=',')
    overrep_reads['sample_id']=sample+'_'+experiment
    if library_read_type == '1':
        overrep_reads['library_read_type'] = 'pe_1'
    if library_read_type == '2':
        overrep_reads['library_read_type'] = 'pe_2'
    if library_read_type.isalpha():
        overrep_reads['library_read_type'] = 'se'         
    overrep_reads_table=overrep_reads_table.append(overrep_reads, ignore_index=True)  
    
    
#per base quality
per_base_quality_files = glob2.glob(args.directory[0]+'*per_base_quality.csv') 
per_base_quality_table=pd.DataFrame()
for per_base_quality_file in per_base_quality_files:
    base_file=os.path.basename(per_base_quality_file)
    sample=base_file.split('_')[0]
    experiment=base_file.split('_')[1]
    library_read_type=base_file.split('_')[2]
    per_base_quality=pd.read_table(per_base_quality_file, sep=',')
    per_base_quality=per_base_quality[['position', 'q10','q25','median','q75','q90']]
    per_base_quality['sample_id']=sample+'_'+experiment
    if library_read_type == '1':
        per_base_quality['library_read_type'] = 'pe_1'
    if library_read_type == '2':
        per_base_quality['library_read_type'] = 'pe_2'
    if library_read_type.isalpha():
        per_base_quality['library_read_type'] = 'se'         
    per_base_quality_table=per_base_quality_table.append(per_base_quality, ignore_index=True)      
    

#per read quality
per_read_quality_files = glob2.glob(args.directory[0]+'*per_read_quality.csv') 
per_read_quality_table=pd.DataFrame()
for per_read_quality_file in per_read_quality_files:
    base_file=os.path.basename(per_read_quality_file)
    sample=base_file.split('_')[0]
    experiment=base_file.split('_')[1]
    library_read_type=base_file.split('_')[2]
    per_read_quality=pd.read_table(per_read_quality_file, sep=',')
    per_read_quality=per_read_quality[['read','sequence_mean']]
    per_read_quality['sample_id']=sample+'_'+experiment
    if library_read_type == '1':
        per_read_quality['library_read_type'] = 'pe_1'
    if library_read_type == '2':
        per_read_quality['library_read_type'] = 'pe_2'
    if library_read_type.isalpha():
        per_read_quality['library_read_type'] = 'se'         
    per_read_quality_table=per_read_quality_table.append(per_read_quality, ignore_index=True)  
    
#read content
read_content_files = glob2.glob(args.directory[0]+'*read_content.csv') 
read_content_table=pd.DataFrame()
for read_content_file in read_content_files:
    base_file=os.path.basename(read_content_file)
    sample=base_file.split('_')[0]
    experiment=base_file.split('_')[1]
    library_read_type=base_file.split('_')[2]
    read_content=pd.read_table(read_content_file, sep=',')
    read_content=read_content[['position','a','c','t','g','n']]
    read_content['sample_id']=sample+'_'+experiment
    if library_read_type == '1':
        read_content['library_read_type'] = 'pe_1'
    if library_read_type == '2':
        read_content['library_read_type'] = 'pe_2'
    if library_read_type.isalpha():
        read_content['library_read_type'] = 'se'         
    read_content_table=read_content_table.append(read_content, ignore_index=True)  

#read length
read_length_files = glob2.glob(args.directory[0]+'*read_length.csv') 
read_length_table=pd.DataFrame()
for read_length_file in read_length_files:
    base_file=os.path.basename(read_length_file)
    sample=base_file.split('_')[0]
    experiment=base_file.split('_')[1]
    library_read_type=base_file.split('_')[2]
    read_length=pd.read_table(read_length_file, sep=',')
    read_length=read_length[['read_length', 'num_reads']]
    read_length['sample_id']=sample+'_'+experiment
    if library_read_type == '1':
        read_length['library_read_type'] = 'pe_1'
    if library_read_type == '2':
        read_length['library_read_type'] = 'pe_2'
    if library_read_type.isalpha():
        read_length['library_read_type'] = 'se'         
    read_length_table=read_length_table.append(read_length, ignore_index=True)  
   
