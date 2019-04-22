#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 13:36:11 2019

@author: jwalla12
"""
import os, glob2

#make a function that takes the trailing filename as an arg
#then it will get the sample_id
#call that function in my other functions to parse

def alignmentmetrics_parse(directory):
    dictionary_list = []
    directory_list = glob2.glob(os.path.join(directory, '*_alignment_metrics_picard.txt'))

    for fname in directory_list: 
        base_file = os.path.basename(fname)
        
        sample=base_file.split('_')[0]
        experiment=base_file.split('_')[1]
        library_read_type=base_file.split('_')[2]
        if library_read_type[0].isalpha(): # single-end
            library_read_type = 'se'
        
        sample_id = sample+'_'+experiment+'_'+library_read_type
        
        f = open(fname, 'r', encoding = "ISO-8859-1")
        
        contents = f.readlines()

        for content in contents:
            if 'PAIR' in content:
                value = content.strip("\n").split("\t")
        for content in contents:
            if 'UNPAIRED' in content:
                value = content.strip("\n").split("\t")    
                
        dictionary = {sample_id:value}
            
        dictionary_list.append(dictionary)
    return(dictionary_list)

def insertmetrics_parse(directory):
    dictionary_list = []
    directory_list = glob2.glob(os.path.join(directory, '*_insertsize_metrics_picard.txt'))
    
    for fname in directory_list:
        base_file = os.path.basename(fname)
        
        sample=base_file.split('_')[0]
        experiment=base_file.split('_')[1]
        library_read_type=base_file.split('_')[2]
        if library_read_type[0].isalpha(): # single-end
            library_read_type = 'se'
        
        sample_id = sample+'_'+experiment+'_'+library_read_type
        
        f = open(fname, 'r', encoding = "ISO-8859-1")
        
        contents = f.readlines()
        
        for content in contents:
            if 'FR' in content:
                value = content.strip("\n").split("\t")
        for content in contents:
            if 'RF' in content:
                value = content.strip("\n").split("\t")
        for content in contents:
            if 'TANDEM' in content:
                value = content.strip("\n").split("\t") 
                
        dictionary = {sample_id:value}
   
        dictionary_list.append(dictionary)
    return(dictionary_list)
            
def parse_picard_GCBias_metrics(directory):
    dictionary_list = []
    directory_list = glob2.glob(os.path.join(directory, '*_gcbias_metrics_picard.txt'))
    
    for fname in directory_list:
        base_file = os.path.basename(fname)
        
        sample=base_file.split('_')[0]
        experiment=base_file.split('_')[1]
        library_read_type=base_file.split('_')[2]
        if library_read_type[0].isalpha(): # single-end
            library_read_type = 'se'
        
        sample_id = sample+'_'+experiment+'_'+library_read_type
        
        f = open(fname, 'r', encoding = "ISO-8859-1")
        
        contents = f.readlines()

        for content in contents:    
            if 'All' in content:
                value = content.strip("\n").split("\t")
                        
        dictionary = {sample_id:value}
   
        dictionary_list.append(dictionary)
    return(dictionary_list)

