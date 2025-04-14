#!/usr/bin/env python3

import ftplib
import netrc
from datetime import datetime
import os

import epygram
epygram.init_env()

#Conf
def recup(date,t,expe):
	host = 'hendrix.meteo.fr'
	run = date
	term =  t #in hours

#get file
	user, _, password = netrc.netrc().authenticators(host)
	ftp = ftplib.FTP(host, user, password)
	filename = run.strftime("/home/magnaldom/vortex/arome/3dvarfr/%s/%Y%m%dT%H%MP/" %(expe))
	filename += 'forecast/'
	filename += "historic.arome.franmg-01km30+" + str(term).zfill(4)  + ":00.fa"
	print(filename)
	with open('arome.fa', 'wb') as f:
		ftp.retrbinary('RETR ' + filename, f.write)

	r = epygram.formats.resource('arome.fa', 'r')
#liste des champs dispos
#la liste est decrite ici: http://intra.cnrm.meteo.fr/aromerecherche/spip.php?article25
	return r


def recup_up(date,t,expe):
	host = 'hendrix.meteo.fr'
	run = date
	term =  t #in hours

#get file
	user, _, password = netrc.netrc().authenticators(host)
	ftp = ftplib.FTP(host, user, password)
	filename = run.strftime("/home/magnaldom/vortex/arome/3dvarfr/"+expe+"/%Y%m%dT%H%MP/" )
	filename += 'forecast/'
	filename += "historic.arome.franmg-01km30+" + str(term).zfill(4)  + ":00.fa"
	print(filename)
	dossier = "/d0/Users/magnaldom/STOCKAGE_AROME_UP/%s/temp/%s%s/" %(expe,str(date.year).zfill(4), str(date.month).zfill(2))
	file_out = dossier + '%s%s%s%s.fa' %(str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2), str(t).zfill(2))
	with open(dossier + '%s%s%s%s.fa' %(str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2), str(t).zfill(2)), 'wb') as f:
		ftp.retrbinary('RETR ' + filename, f.write)

	r = epygram.formats.resource(file_out, 'r')
#liste des champs dispos
#la liste est decrite ici: http://intra.cnrm.meteo.fr/aromerecherche/spip.php?article25
	return r

def recup_without_return(date,t,expe):
	host = 'hendrix.meteo.fr'
	run = date
	term =  t #in hours

#get file
	user, _, password = netrc.netrc().authenticators(host)
	ftp = ftplib.FTP(host, user, password)
	filename = run.strftime("/home/magnaldom/vortex/arome/3dvarfr/"+expe+"/%Y%m%dT%H%MP/" )
	filename += 'forecast/'
	filename += "historic.arome.franmg-01km30+" + str(term).zfill(4)  + ":00.fa"
	print(filename)
	#file_out = '%s%s%s%s_temp.fa' %(str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2), str(t).zfill(2))
	dossier = "/d0/Users/magnaldom/STOCKAGE_AROME_UP/%s/temp/%s%s/" %(expe, str(date.year).zfill(4), str(date.month).zfill(2))
	with open(dossier + '%s%s%s%s_temp.fa' %(str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2), str(t).zfill(2)), 'wb') as f:
		ftp.retrbinary('RETR ' + filename, f.write)
