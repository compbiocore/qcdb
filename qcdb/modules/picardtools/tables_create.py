#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 09:13:27 2019

@author: jwalla12
"""

import sqlalchemy

def picardtools_create(metadata):
    picardtools_alignment_metrics = Table('picardtools_alignment_metrics', metadata,                                        
                                          Column('_id', Integer, primary_key=True),
                                          column('sample_id', String(50), ForeignKey('samplemeta.sample_id')).
                                          Column('CATEGORY',  String(50)),
                                          Column('TOTAL_READS', Float),
                                          Column('PF_READS', Float),
                                          Column('PCT_PF_READS', Float),
                                          Column('PF_NOISE_READS', Float),
                                          Column('PF_READS_ALIGNED', Float),
                                          Column('PCT_PF_READS_ALIGNED', Float),
                                          Column('PF_ALIGNED_BASES', Float),
                                          Column('PF_HQ_ALIGNED_READS', Float),
                                          Column('PF_HQ_ALIGNED_BASES', Float),
                                          Column('PF_HQ_ALIGNED_Q20_BASES', Float),
                                          Column('PF_HQ_MEDIAN_MISMATCHES', Float),
                                          Column('PF_MISMATCH_RATE', Float),
                                          Column('PF_HQ_ERROR_RATE', Float),
                                          Column('PF_INDEL_RATE', Float),
                                          Column('MEAN_READ_LENGTH', Float),
                                          Column('READS_ALIGNED_IN_PAIRS', Float),
                                          Column('PCT_READS_ALIGNED_IN_PAIRS', Float),
                                          Column('PF_READS_IMPROPER_PAIRS', Float),
                                          Column('PCT_PF_READS_IMPROPER_PAIRS', Float),
                                          Column('BAD_CYCLES', Float),
                                          Column('STRAND_BALANCE', Float),
                                          Column('STRAND_BALANCE', Float),
                                          Column('PCT_CHIMERAS', Float),
                                          Column('PCT_ADAPTER', Float),
                                          Column('SAMPLE', String(50)),
                                          Column('LIBRARY', String(50)),
                                          Column('READ_GROUP', String(50))
                                          )
    
    picardtools_insertsize_metrics = Table('picardtools_insertsize_metrics', metadata,                                        
                                          Column('_id', Integer, primary_key=True),
                                          column('sample_id', String(50), ForeignKey('samplemeta.sample_id')).
                                          Column('MEDIAN_INSERT_SIZE', String(50)),
                                          Column('MEDIAN_ABSOLUTE_DEVIATION', Float),
                                          Column('MIN_INSERT_SIZE', Float),
                                          Column('MAX_INSERT_SIZE', Float),
                                          Column('MEAN_INSERT_SIZE', Float),                                          
                                          Column('STANDARD_DEVIATION', Float),
                                          Column('READ_PAIRS', Float),
                                          Column('PAIR_ORIENTATION', String(50)),
                                          Column('WIDTH_OF_10_PERCENT', Float),
                                          Column('WIDTH_OF_20_PERCENT', Float),
                                          Column('WIDTH_OF_30_PERCENT', Float),
                                          Column('WIDTH_OF_40_PERCENT', Float),
                                          Column('WIDTH_OF_50_PERCENT', Float),
                                          Column('WIDTH_OF_60_PERCENT', Float),
                                          Column('WIDTH_OF_70_PERCENT', Float),
                                          Column('WIDTH_OF_80_PERCENT', Float),
                                          Column('WIDTH_OF_90_PERCENT', Float),
                                          Column('WIDTH_OF_99_PERCENT', Float),
                                          Column('SAMPLE', String(50)),
                                          Column('LIBRARY', String(50)),
                                          Column('READ_GROUP', String(50))
                                          )                                          

    picardtools_insertsize_metrics = Table('picardtools_gcbias_metrics', metadata,                                        
                                          Column('_id', Integer, primary_key=True),
                                          column('sample_id', String(50), ForeignKey('samplemeta.sample_id')).
                                          Column('ACCUMULATION_LEVEL', String(50)),
                                          Column('READS_USED', String(50)),
                                          Column('WINDOW_SIZE', Float),
                                          Column('TOTAL_CLUSTERS', Float),
                                          Column('ALIGNED_READS', Float),                                          
                                          Column('AT_DROPOUT', Float),
                                          Column('GC_DROPOUT', Float),
                                          Column('GC_NC_0_19', Float),
                                          Column('GC_NC_20_39', Float),
                                          Column('GC_NC_40_59', Float),
                                          Column('GC_NC_60_79', Float),
                                          Column('GC_NC_80_100', Float),
                                          Column('SAMPLE', String(50)),
                                          Column('LIBRARY', String(50)),
                                          Column('READ_GROUP', String(50))
                                          )      