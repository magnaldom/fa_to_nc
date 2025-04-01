#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 12:07:02 2021

@author: magnaldom
"""
import netCDF4 as nc
import numpy as np
import os
import time
#import imp
#imp.reload(fonctions_fa_nc)
import fonction_recup
from datetime import datetime, timedelta
import sys
from num_jour_between import num_jour_between
import ftplib
import netrc
import epygram
epygram.init_env()

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


file_prestaging = "test_recup_AROME_%s%s" %(str(date1.year),str(date1.month).zfill(2))
fichier = open(file_prestaging, "w")
fichier.write("#MAIL=marie-adele.magnaldo@meteo.fr" + "\n")

num_jour = num_jour_between(date1,date2)
for d in range(0,num_jour):
	date = date1 + timedelta(days = d)
	t_deb = 1
	t_fin = 23
	for t in range(t_deb, t_fin):
		ech=str(t).zfill(2)
		Y = str(date.year).zfill(2)
		M = str(date.month).zfill(2)
		D = str(date.day).zfill(2)
		filename = "~mxpt001/vortex/arome/3dvarfr/OPER/%s/%s/%s/T%s00A/" %(Y,M,D,ech)
		filename += 'minim/'
		filename += "analysis.atm-arome.franmg-01km30.fa"
		fichier.write("~mxpt001/vortex/arome/3dvarfr/OPER/%s/%s/%s/T%s00A/minim/analysis.atm-arome.franmg-01km30.fa"  %(Y, M,D,ech) + "\n")

fichier.close()
fichier = open(file_prestaging, "rb")
#Le déposer
host = 'hendrix.meteo.fr'
user, _, password = netrc.netrc().authenticators(host)
ftp = ftplib.FTP(host, user, password)
file = open(file_prestaging, 'rb')
ftpCommand = "STOR /DemandeMig/ChargeEnEspaceRapide/test_recup_AROME_%s%s" %(str(date1.year),str(date1.month).zfill(2))
ftp.storbinary(ftpCommand, fichier)
#/DemandeMig/ChargeEnEspaceRapide
fichier.close()

rename = ftp.rename("/DemandeMig/ChargeEnEspaceRapide/test_recup_AROME_%s%s" %(str(date1.year),str(date1.month).zfill(2)), "/DemandeMig/ChargeEnEspaceRapide/test_recup_AROME_%s%s.MIG" %(str(date1.year),str(date1.month).zfill(2))) # maintenant, on effectue vraiment l'action

rep = ftp.dir() # on récupère le listing
print(rep)




