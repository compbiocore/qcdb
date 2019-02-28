import pandas as pd


#The outputs from bioflows sra-tools will prepend the .fastq filenames with information about SRA experiments, etc.
#This information will also be parsed by qckitfastq (needs to be updated) so that it outputs files containing SRA experiments, etc. in the filenames.
#Once this is confirmed (bioflows) and implemented (qckitfastq), the parsing should be changed so that the filenames are parsed (not the directories). 

fastqckit_dir = ('../../SRX3544048/SAMN08331802/SRR6453154') #assign fastqckit_dir to the folder where the adapter content files are saved
fastqckit_dir.split('/') #split the directory string, dir names are informative -- they correspond to experiment/biosample/run
experiment=fastqckit_dir.split('/')[-3]
biosample=fastqckit_dir.split('/')[-2]
run=fastqckit_dir.split('/')[-1]

#adapters
adapter_content_file = ('/adapter_content.csv') #specify which is the adapter content file
adapter_content_file_path = fastqckit_dir+adapter_content_file #join the 2 strings to specify the full path name
adapter_content = pd.read_csv(adapter_content_file_path) #read in the adapter content as a df
adapter_content = adapter_content[['adapter','count']] #clean up superfluous column
adapter_content['sample_id']=experiment+'_'+biosample+'_'+run


#gc content
gc_content_file = ('/gc_content.csv') #specify which is the gc content file
gc_content_file_path = fastqckit_dir+gc_content_file #join the 2 strings to specify the full path name
gc_content = pd.read_csv(gc_content_file_path) #read in the gc content as a df
gc_content = gc_content[['read','mean_GC']] #clean up superfluous column
gc_content['sample_id']=experiment+'_'+biosample+'_'+run


#kmer counts
kmer_content_file = ('/kmer_count.csv') #specify which is the kmer content file
kmer_content_file_path = fastqckit_dir+kmer_content_file #join the 2 strings to specify the full path name
kmer_content = pd.read_csv(kmer_content_file_path) #read in the kmer content as a df
kmer_content.rename(columns={kmer_content.columns[0]:'kmer'}, inplace=True) #name the first 0-indexed column 'kmer'
kmer_content = pd.melt(kmer_content, id_vars=['kmer']) #melt the dataframe but specify that the id_vars is the 'kmer' column
kmer_content.columns=['kmer','position','count'] #give the columns the right names
kmer_content['sample_id']=experiment+'_'+biosample+'_'+run #add the sample_id column


#overrepresented kmers
overrep_kmer_file = ('/overrep_kmer.csv') #specify which is the overrepresented kmer file
overrep_kmer_file_path = fastqckit_dir+overrep_kmer_file #join the 2 strings to specify the full path name
overrep_kmer_content = pd.read_csv(overrep_kmer_file_path) #read in the overrepresented kmer file as a df
overrep_kmer_content = overrep_kmer_content[['row','position','obsexp_ratio','kmer']] #clean up superfluous column
overrep_kmer_content['sample_id']=experiment+'_'+biosample+'_'+run #add the sample_id column


#overrepresented reads
overrep_reads_file = ('/overrep_reads.csv') #specify which is the overrepresented reads file
overrep_reads_file_path = fastqckit_dir+overrep_reads_file #join the 2 strings to specify the full path name
overrep_reads = pd.read_csv(overrep_reads_file_path) #read in the overrepresented reads file as a df
overrep_reads = overrep_reads[['read_sequence','count']] #clean up superfluous column
overrep_reads['sample_id']=experiment+'_'+biosample+'_'+run #add the sample_id column


#per base quality
per_base_qual_file = ('/per_base_quality.csv') #specify which is the overrepresented reads file
per_base_qual_file_path = fastqckit_dir+per_base_qual_file #join the 2 strings to specify the full path name
per_base_qual = pd.read_csv(per_base_qual_file_path) #read in the overrepresented reads file as a df
per_base_qual=per_base_qual[['position', 'q10','q25','median','q75','q90']]
per_base_qual['sample_id']=experiment+'_'+biosample+'_'+run #add the sample_id column


#per read quality
per_read_qual_file = ('/per_read_quality.csv') #specify which is the overrepresented reads file
per_read_qual_file_path = fastqckit_dir+per_read_qual_file #join the 2 strings to specify the full path name
per_read_qual = pd.read_csv(per_read_qual_file_path) #read in the overrepresented reads file as a df
per_read_qual=per_read_qual[['read','sequence_mean']]
per_read_qual['sample_id']=experiment+'_'+biosample+'_'+run #add the sample_id column


#read content
read_content_file = ('/read_content.csv') #specify which is the overrepresented reads file
read_content_file_path = fastqckit_dir+read_content_file #join the 2 strings to specify the full path name
read_content = pd.read_csv(read_content_file_path) #read in the overrepresented reads file as a df
read_content=read_content[['position','a','c','t','g','n']]
read_content['sample_id']=experiment+'_'+biosample+'_'+run #add the sample_id column


#read length
read_length_file = ('/read_length.csv') #specify which is the overrepresented reads file
read_length_file_path = fastqckit_dir+read_length_file #join the 2 strings to specify the full path name
read_length = pd.read_csv(read_length_file_path) #read in the overrepresented reads file as a df
read_length=read_length[['read_length', 'num_reads']]
read_length['sample_id']=experiment+'_'+biosample+'_'+run #add the sample_id column
