#!/usr/bin/env python3

import ftplib
import netrc
from datetime import datetime
import os

import epygram
epygram.init_env()

#Conf
def recup(date,t):
	host = 'hendrix.meteo.fr'
	run = date
	term =  t #in hours

#get file
	user, _, password = netrc.netrc().authenticators(host)
	ftp = ftplib.FTP(host, user, password)
	ech=str(t).zfill(2)
	Y = str(date.year).zfill(2)
	M = str(date.month).zfill(2)
	D = str(date.day).zfill(2)
	filename = run.strftime("~mxpt001/vortex/arome/3dvarfr/OPER/%s/%s/%s/T%s00A/" %(Y,M,D,ech))
	filename += 'minim/'
	filename += "analysis.atm-arome.franmg-01km30.fa"
	print(filename)
	with open('arome.fa', 'wb') as f:
		ftp.retrbinary('RETR ' + filename, f.write)

	r = epygram.formats.resource('arome.fa', 'r')
#liste des champs dispos
#la liste est decrite ici: http://intra.cnrm.meteo.fr/aromerecherche/spip.php?article25
	return r


def recup_up(date,t):
	host = 'hendrix.meteo.fr'
	run = date
	term =  t #in hours

#get file
	user, _, password = netrc.netrc().authenticators(host)
	ftp = ftplib.FTP(host, user, password)
	ech=str(t).zfill(2)
	Y = str(date.year).zfill(2)
	M = str(date.month).zfill(2)
	D = str(date.day).zfill(2)
	filename = run.strftime("~mxpt001/vortex/arome/3dvarfr/OPER/%s/%s/%s/T%s00A/" %(Y,M,D,ech))
	filename += 'minim/'
	filename += "analysis.atm-arome.franmg-01km30.fa"
	print(filename)
	d0_dir = "/d0/Users/magnaldom/STOCKAGE_AROME_UP/"
	dossier = "%stemp/%s%s/" %(d0_dir,str(date.year).zfill(4), str(date.month).zfill(2))
	file_out = dossier + '%s%s%s%s.fa' %(str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2), str(t).zfill(2))
	with open(dossier + '%s%s%s%s.fa' %(str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2), str(t).zfill(2)), 'wb') as f:
		ftp.retrbinary('RETR ' + filename, f.write)

	r = epygram.formats.resource(file_out, 'r')
#liste des champs dispos
#la liste est decrite ici: http://intra.cnrm.meteo.fr/aromerecherche/spip.php?article25
	return r

def recup_without_return(date,t):
	host = 'hendrix.meteo.fr'
	run = date
	term =  t #in hours

#get file
	user, _, password = netrc.netrc().authenticators(host)
	ftp = ftplib.FTP(host, user, password)
	ech=str(t).zfill(2)
	Y = str(date.year).zfill(2)
	M = str(date.month).zfill(2)
	D = str(date.day).zfill(2)
	filename = run.strftime("~mxpt001/vortex/arome/3dvarfr/OPER/%s/%s/%s/T%s00A/" %(Y,M,D,ech))
	filename += 'minim/'
	filename += "analysis.atm-arome.franmg-01km30.fa"
	print(filename)
	d0_dir = "/d0/Users/magnaldom/STOCKAGE_AROME_UP/"
	#file_out = '%s%s%s%s_temp.fa' %(str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2), str(t).zfill(2))
	dossier = "%stemp/%s%s/" %(d0_dir,str(date.year).zfill(4), str(date.month).zfill(2))
	with open(dossier + '%s%s%s%s_temp.fa' %(str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2), str(t).zfill(2)), 'wb') as f:
		ftp.retrbinary('RETR ' + filename, f.write)
