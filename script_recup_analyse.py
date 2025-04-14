#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 15:24:53 2021

@author: magnaldom
"""

import ftplib
import netrc
from datetime import datetime
import os
import netCDF4 as nc
import numpy as np
import os
import time
import fonction_recup_analyse
from datetime import datetime, timedelta
import sys
from num_jour_between import num_jour_between
import epygram
epygram.init_env()

#Recup dates
date_temp1 = sys.argv[1]
date_temp2 = sys.argv[2]
y1 = int(date_temp1[:4])
m1 = int(date_temp1[4:6])
d1 = int(date_temp1[6:8])
y2 = int(date_temp2[:4])
m2 = int(date_temp2[4:6])
d2 = int(date_temp2[6:8])
date1 = datetime(y1,m1,d1,0,0,0)
date2 = datetime(y2,m2,d2,0,0,0)
stop = 0
num_jour = num_jour_between(date1,date2)
for d in range(0,num_jour):
	if stop > 5 :
		break
	date = date1 + timedelta(days = d)
	nb_heure = 1
	t_deb = 1

	t_fin = 23
	for t in range(t_deb,t_fin): #nb_heure+1):
			#====================
		# Attendre qu'il y ait moins de 5 fichiers
		#====================
		time_counter = 0
		time_to_wait = 60*60
		d0_dir = "/d0/Users/magnaldom/STOCKAGE_AROME_UP/"
		DIR = "%stemp/%s%s/" %(d0_dir,str(date.year).zfill(4), str(date.month).zfill(2))

		nb_file = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
		while not nb_file<5:
			time.sleep(1*30)
			time_counter += 1*30
			nb_file = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
			if time_counter > time_to_wait:
				stop = stop + 1
				break
		if nb_file < 5:
			fonction_recup_analyse.recup_without_return(date,t)

		if os.path.exists("%stemp/%s%s/%s%s%s%s_temp.fa" %(d0_dir,str(date.year), str(date.month).zfill(2),str(date.year), str(date.month).zfill(2), str(date.day).zfill(2), str(t).zfill(2))):
			os.system("mv %stemp/%s%s/%s%s%s%s_temp.fa %stemp/%s%s/%s%s%s%s.fa" %(d0_dir,str(date.year).zfill(4), str(date.month).zfill(2),str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2), str(t).zfill(2), d0_dir,str(date.year).zfill(4), str(date.month).zfill(2), str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2), str(t).zfill(2)))
		if os.path.exists("%stemp/%s%s/%s%s%s%s.fa" %(d0_dir,str(date.year), str(date.month).zfill(2),str(date.year), str(date.month).zfill(2), str(date.day).zfill(2), str(t).zfill(2))):
			print("Transfert de %s%s%s%s.fa réussi" %(str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2), str(t).zfill(2)))


