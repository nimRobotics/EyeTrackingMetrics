'''
author: @nimrobotics
description: calculates the SGE and GTE for SAI data
'''

import numpy as np
import pandas as pd
import glob
import os
from eyesmetriccalculator import EyesMetricCalculator
from transition_matrix import *
import csv

def getGazeValues(file):
	'''
	Extracts gaze values for all trials from the file using Event markers
	file: tsv file name
	returns: participant ID, list of lists of gaze values for normal and attack trials
	'''
	df = pd.read_csv(file,sep='\t')
	
	# handle empty files
	try:
		participantID=df['Participant name'][0]
	except IndexError as e:
		print("Error Processing file: ",file)
		participantID=str(file)

	# df=df[["Event","Gaze point X", "Gaze point Y","Gaze event duration","Fixation point X","Fixation point Y"]]  # select columns
	df=df[["Event","Gaze point X [MCS px]", "Gaze point Y [MCS px]","Gaze event duration [ms]","Fixation point X [MCS px]","Fixation point Y [MCS px]"]]  # select columns

	normal_start_idx=df[df['Event'] == 'Normal Trial Start'].index.to_numpy() 
	normal_stop_idx=df[df['Event'] == 'Normal Trail End'].index.to_numpy() 
	# correction for misspelled event (Trial vs Trail)
	if len(normal_stop_idx)==0:
			normal_stop_idx=df[df['Event'] == 'Normal Trial End'].index.to_numpy() 
	attack_start_idx=df[df['Event'] == 'Attack Trial Start'].index.to_numpy() 
	attack_stop_idx=df[df['Event'] == 'Attack Trial End'].index.to_numpy() 
	
	# check if length of start and stop indices are equal, else make them equal using minimum length
	if len(normal_start_idx)!=len(normal_stop_idx):
		print(len(normal_start_idx),len(normal_stop_idx),len(attack_start_idx),len(attack_stop_idx))
		print("Error: Length of Normal Start and Stop indices are not equal")
		normal_start_idx=normal_start_idx[:np.min([len(normal_start_idx),len(normal_stop_idx)])]
		normal_stop_idx=normal_stop_idx[:np.min([len(normal_start_idx),len(normal_stop_idx)])]
	if len(attack_start_idx)!=len(attack_stop_idx):
		print("Error: Length of Attack Start and Stop indices are not equal")
		attack_start_idx=attack_start_idx[:np.min([len(attack_start_idx),len(attack_stop_idx)])]
		attack_stop_idx=attack_stop_idx[:np.min([len(attack_start_idx),len(attack_stop_idx)])]

	# remove irrelevant data
	df=df[["Gaze point X [MCS px]", "Gaze point Y [MCS px]","Gaze event duration [ms]","Fixation point X [MCS px]","Fixation point Y [MCS px]"]]  # select columns

	normalData=[]
	for i in range(normal_start_idx.shape[0]):
		normalData.append(df.loc[normal_start_idx[i]:normal_stop_idx[i]].dropna(subset = ["Gaze point X [MCS px]", "Gaze point Y [MCS px]"]).to_numpy())
		# CAUTION: dropping NA values for "Gaze point X", "Gaze point Y" only. To drop all NA values use .dropna()

	attackData=[]
	for i in range(attack_start_idx.shape[0]):
		attackData.append(df.loc[attack_start_idx[i]:attack_stop_idx[i]].dropna(subset = ["Gaze point X [MCS px]", "Gaze point Y [MCS px]"]).to_numpy())
		# CAUTION: dropping NA values for "Gaze point X", "Gaze point Y" only. To drop all NA values use .dropna()

	return(participantID, normalData, attackData)

def getAOI(nx, ny, screen_dimension):
	'''
	nx: gaze point x coordinate
	ny: gaze point y coordinate
	screen_dimension: screen dimension in pixels
	returns: AOI
	'''
	x = np.linspace(0, screen_dimension[0], nx)
	y = np.linspace(0, screen_dimension[1], ny)
	xv, yv = np.meshgrid(x, y)
	aoiDict = {}
	vertices=np.zeros((4,2))
	for i in range(xv.shape[0]-1):
		for j in range(xv.shape[1]-1):
			aoiName='aoi_'+str(i)+'_'+str(j)
			vertices[0,:]=np.array([xv[i,j],yv[i,i]])
			vertices[1,:]=np.array([xv[i,j+1],yv[i,j+1]])
			vertices[2,:]=np.array([xv[i+1,j+1],yv[i+1,j]])
			vertices[3,:]=np.array([xv[i+1,j],yv[i+1,j+1]])
			aoiDict[aoiName]=PolyAOI(screen_dimension,vertices)
	return(aoiDict)

def getSGE_GTE(trials):
	"""
	trials: list of lists of gaze data
	returns: list of lists of SGE and GTE
	"""
	SGEdata=[]
	GTEdata=[]
	for trial in trials:
		gaze=np.zeros((trial.shape[0],3))
		gaze[:,:2]=trial[:,:2]
		fixation=trial[:,2:]
		fixation=fixation[:,[1,2,0]]	
		ec = EyesMetricCalculator(fixation,gaze,TEST_SCREENDIM)
		SGE=ec.GEntropy(TEST_AOI_DICT,'stationary').compute()
		GTE=ec.GEntropy(TEST_AOI_DICT,'transition').compute()		
		SGEdata.append(SGE)
		GTEdata.append(GTE)
	return(SGEdata,GTEdata)

def writeToCSV(data,filename):
	'''
	data: entropy data
	filename: name of the file to be written
	'''
	with open(filename, 'w') as csvfile: 
	    # creating a csv writer object 
	    csvwriter = csv.writer(csvfile) 
	    # writing the fields 
	    csvwriter.writerow(["ID", "Trial 1", "Trial 2", "Trial 3", "Trial 4", "Trial 5", "Trial 6", "Trial 7", "Trial 8", "Trial 9", "Trial 10"]) 
	    # writing the data rows 
	    csvwriter.writerows(data)

if __name__ == '__main__':
	TEST_SCREENDIM = [1920,1080]
	TEST_AOI_DICT=getAOI(11,11,TEST_SCREENDIM)
	# folder_name = 'data_'
	folder_name = 'testdata'

	allNormalSGE=[]
	allNormalGTE=[]
	allAttackSGE=[]
	allAttackGTE=[]
	for file in sorted(glob.glob(folder_name + "/*.tsv")):
		print("\nProcessing file: ",file)

		# "Gaze point X", "Gaze point Y","Gaze event duration","Fixation point X","Fixation point Y"
		participantID, normalData, attackData=getGazeValues(file) 

		print('Number of normal trials: ',len(normalData))
		print('Number of attack trials: ',len(attackData))	

		normalSGE, normalGTE=getSGE_GTE(normalData) # normal SGE and GTE
		attackSGE, attackGTE=getSGE_GTE(attackData) # attack SGE and GTE

		allNormalSGE.append([participantID]+normalSGE)
		allNormalGTE.append([participantID]+normalGTE)
		allAttackSGE.append([participantID]+attackSGE)
		allAttackGTE.append([participantID]+attackGTE)
	
	writeToCSV(allNormalSGE,'allNormalSGE.csv')
	writeToCSV(allNormalGTE,'allNormalGTE.csv')
	writeToCSV(allAttackSGE,'allAttackSGE.csv')
	writeToCSV(allAttackGTE,'allAttackGTE.csv')



	

