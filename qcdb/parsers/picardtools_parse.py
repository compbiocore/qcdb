#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 13:36:11 2019

@author: jwalla12
"""
import os, re, glob2
import logging
from parsers.parse import BaseParser

log = logging.getLogger(__name__)

class picardParser(BaseParser):# specifying a picardparser class
    def __init__(self, directory): # initializing a picardparser object
        log.info("Initializing picardParser...")
        BaseParser.__init__(self, directory) #runs the BaseParser initializer which will fill in some fields
        
        
    def alignmentmetrics_parse(self, directory):
        dictionary_list = ()
        #directory_list = os.listdir(directory)
        directory_list = glob2.glob(os.path.join(directory, '*_alignment_metrics_picard.txt'))
        for fname in directory_list: 
            sample_id = self.sample_id(base_file)
            f = open(directory + os.sep + fname, 'r', encoding = "ISO-8859-1")
            contents = f.readlines()
            
            for content in contents:
                if 'CATEGORY' in content:
                    header_value = content.strip("\n").split("\t")
            for content in contents:
                if 'UNPAIRED' in content:
                    value = content.strip("\n").split("\t")    
            for content in contents:
                if 'PAIR' in content:
                    value = content.strip("\n").split("\t")

                dictionary = {sample_id:{header_value, value}}
                dictionary_list.append(dictionary)
        return(dictionary_list)

    def insertmetrics_parse(self, directory):
        dictionary_list = ()
        #directory_list = os.listdir(directory)
        directory_list = glob2.glob(os.path.join(directory, '*_insertsize_metrics_picard.txt'))
        for fname in directory_list: 
            sample_id = self.sample_id(base_file)
            f = open(directory + os.sep + fname, 'r', encoding = "ISO-8859-1")
            contents = f.readlines()
            
            for content in contents:
                if 'MEDIAN_INSERT_SIZE' in content:
                    header_value = content.strip("\n").split("\t")
            for content in contents:
                if 'FR' in content:
                    value = content.strip("\n").split("\t")
            for content in contents:
                if 'RF' in content:
                    value = content.strip("\n").split("\t")
            for content in contents:
                if 'TANDEM' in content:
                    value = content.strip("\n").split("\t") 
                            
                dictionary = {sample_id:{header_value, value}}
                dictionary_list.append(dictionary)
        return(dictionary_list)
                
    def parse_picard_GCBias_metrics(self, directory):
        dictionary_list = ()
        #directory_list = os.listdir(directory)
        directory_list = glob2.glob(os.path.join(directory, '*_gcbias_metrics_picard.txt'))
        for fname in directory_list: 
            sample_id = self.sample_id(base_file)
            f = open(directory + os.sep + fname, 'r', encoding = "ISO-8859-1")
            contents = f.readlines()

            for content in contents:
                if 'AT_DROPOUT' in content:
                    header_value = content.strip("\n").split("\t")
            for content in contents:    
                if 'All' in content:
                    value = content.strip("\n").split("\t")
                            
                dictionary = {sample_id:{header_value, value}}
                dictionary_list.append(dictionary)
        return(dictionary_list)
    
    
