from DeepWhiskerCuts.lib.ProgressManager import ExperimentManager
import os 
import pdb
path = r'\\dk-server.dk.ucsd.edu\afassihizakeri\Topviewmovies\ar37\2023_03_23_182302'
manager = ExperimentManager(path,'top')
manager.print_progress()