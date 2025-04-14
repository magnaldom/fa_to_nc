#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### ============================================================================
### Transformation des fichiers FA de sortie de modèle en un fichier unique en
### format NetCDF.
###

### ============================================================================

### PACKAGES
import netCDF4 as nc
import numpy as np
import os
import fonctions_fa_nc
import time
import imp
imp.reload(fonctions_fa_nc)
import fonction_recup
from datetime import datetime, timedelta
import sys
from num_jour_between import num_jour_between
import epygram
epygram.init_env()
import subprocess
### ============================================================================
### DONNEES ENTREES

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

####==============
### On lance le scrip recup
###=================

os.system("rm -f temp/%s%s/*" %(str(date1.year), str(date1.month).zfill(2)))

os.system("python3 prestaging.py %s %s &" %(date_temp1, date_temp2))
os.system("python3 script_recup.py %s %s &" %(date_temp1, date_temp2))
#subprocess.run(["python3 script_recup.py %s %s" %(date_temp1, date_temp2)])
print("Script_recup lancé")
### ============================================================================
### INITIALISATION GEOMETRIE
try:
	FILE = fonction_recup.recup_up(date1,0)
	#fa = "historic.arome.fog"+res+"-"+res+"m000+0000:00.fa"
	#FILE = epygram.formats.resource(fa, 'r')
except:
	print("Fichiers non disponibles " )
	sys.exit()

HU = FILE.readfield('S001HUMI.SPECIFI')
lons, lats = HU.geometry.get_lonlat_grid(subzone = "CI")
HU = fonctions_fa_nc.getdata3D(FILE.readfields('S*HUMI.SPECIFI'))
FILE.close()

## Constantes de géométrie
nlons = np.shape(lons)[0]
nlats = np.shape(lons)[1]
nalts = np.shape(HU)[2]

### Grille du modèle
LONGITUDE = lons[:nlons, :nlats]
LATITUDE = lats[:nlons, :nlats]
###============================================================================
stop = 0
num_jour = num_jour_between(date1,date2)
for d in range(0,num_jour):
	if stop > 5 :
		break
	date = date1 + timedelta(days = d)
	print(date)


	tmps1=time.time()
	file_nc = nc.Dataset("DATA/%s%s/AROME_%s%s%s.nc" %(str(date.year).zfill(4),str(date.month).zfill(2), str(date.year).zfill(4),str(date.month).zfill(2),str(date.day).zfill(2)),"w",format="NETCDF4")
	#file_nc = nc.Dataset("test.nc","w",format="NETCDF4")

	### ---------------------------------------------------------------------------
	### Dimensions
	file_nc.createDimension('time', None)
	file_nc.createDimension('alt', nalts)
	file_nc.createDimension('lon', nlons)
	file_nc.createDimension('lat', nlats)

	### ---------------------------------------------------------------------------
	### Variables dimentions
	longitude	   = file_nc.createVariable('Longitude', 'f4', dimensions=('lat','lon',))
	latitude		= file_nc.createVariable('Latitude', 'f4', dimensions=('lat','lon',))
	niveau_altitude = file_nc.createVariable('Niveau_alt', 'i4', 'alt')
	echeance		= file_nc.createVariable('Echeance', 'i4', 'time')

	#--------Rayonnement-------#
	SURFRAYT_SOLA_DE = file_nc.createVariable('SURFRAYT_SOLA_DE', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SURFRAYT_THER_DE = file_nc.createVariable('SURFRAYT_THER_DE', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SURFFLU_RAY_SOLA = file_nc.createVariable('SURFFLU_RAY_SOLA', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SURFFLU_RAY_THER = file_nc.createVariable('SURFFLU_RAY_THER', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SOMMFLU_RAY_SOLA = file_nc.createVariable('SOMMFLU_RAY_SOLA', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SOMMFLU_RAY_THER = file_nc.createVariable('SOMMFLU_RAY_THER', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SURFRAYT_SOLAIRE = file_nc.createVariable('SURFRAYT_SOLAIRE', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SURFRAYT_TERREST = file_nc.createVariable('SURFRAYT_TERREST', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SOMMRAYT_SOLAIRE = file_nc.createVariable('SOMMRAYT_SOLAIRE', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SOMMRAYT_TERREST = file_nc.createVariable('SOMMRAYT_TERREST', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	S001RAYT_SOL_CL = file_nc.createVariable('S001RAYT_SOL_CL', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	S001RAYT_THER_CL = file_nc.createVariable('S001RAYT_THER_CL', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	S090RAYT_SOL_CL = file_nc.createVariable('S090RAYT_SOL_CL', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	S090RAYT_THER_CL = file_nc.createVariable('S090RAYT_THER_CL', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	TOPRAYT_DIR_SOM = file_nc.createVariable('TOPRAYT_DIR_SOM', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SURFDIR_NORM_IRR = file_nc.createVariable('SURFDIR_NORM_IRR', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SURFRAYT_DIR_SUR = file_nc.createVariable('SURFRAYT_DIR_SUR', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)

	#-------Nébulosité--------#
	ATMONEBUL_TOTALE = file_nc.createVariable('ATMONEBUL_TOTALE', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	ATMONEBUL_HAUTE = file_nc.createVariable('ATMONEBUL_HAUTE', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	ATMONEBUL_MOYENN = file_nc.createVariable('ATMONEBUL_MOYENN', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	ATMONEBUL_BASSE = file_nc.createVariable('ATMONEBUL_BASSE', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SURFNEBUL_TOTALE = file_nc.createVariable('SURFNEBUL_TOTALE', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SURFNEBUL_HAUTE = file_nc.createVariable('SURFNEBUL_HAUTE', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SURFNEBUL_MOYENN = file_nc.createVariable('SURFNEBUL_MOYENN', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SURFNEBUL_BASSE = file_nc.createVariable('SURFNEBUL_BASSE', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)

	#-------Autres--------------#
	SURFPRESSION = file_nc.createVariable('SURFPRESSION', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)
	SURFTEMPERATURE = file_nc.createVariable('SURFTEMPERATURE', 'f4', dimensions=('time','lat', 'lon'), zlib=True, complevel=1)


	TEMPERATURE  = file_nc.createVariable('TEMPERATURE', 'f4', dimensions=('time','lat', 'lon', 'alt'), zlib=True, complevel=1)
	HUMI_SPECIFI = file_nc.createVariable('HUMI_SPECIFI', 'f4', dimensions=('time','lat', 'lon', 'alt'), zlib=True, complevel=1)
	CLOUD_WATER  = file_nc.createVariable('CLOUD_WATER', 'f4', dimensions=('time','lat', 'lon', 'alt'), zlib=True, complevel=1)
	ICE_CRYSTAL  = file_nc.createVariable('ICE_CRYSTAL', 'f4', dimensions=('time','lat', 'lon', 'alt'), zlib=True, complevel=1)
	CLOUD_FRACTI = file_nc.createVariable('CLOUD_FRACTI', 'f4', dimensions=('time','lat', 'lon', 'alt'), zlib=True, complevel=1)
	SNOW = file_nc.createVariable('SNOW', 'f4', dimensions=('time','lat', 'lon', 'alt'), zlib=True, complevel=1)
	RAIN = file_nc.createVariable('RAIN', 'f4', dimensions=('time','lat', 'lon', 'alt'), zlib=True, complevel=1)
	GRAUPEL = file_nc.createVariable('GRAUPEL', 'f4', dimensions=('time','lat', 'lon', 'alt'), zlib=True, complevel=1)

	CHECK = file_nc.createVariable('CHECK', 'S8', dimensions=('time'), zlib=True, complevel=1)


	tmps2=time.time()
	print("Temps préparation des variables:", tmps2-tmps1)

	### ---------------------------------------------------------------------------
	### Ecritude des variables de dimension
	longitude[::]	  = LONGITUDE.T
	latitude[::]	   = LATITUDE.T
	#echeance[:]		= np.arange(nechs)
	niveau_altitude[:] = np.arange(nalts)


	### ============================================================================
	### ============================================================================
	### Boucles sur les échéances
	nb_heure = 18
	tmps2p=time.time()

	t_deb = 1
	t_fin = 24
	for t in range(t_deb,t_fin): #nb_heure+1):

		#====================
		# Attendre que le fichier.fa soit recup
		#====================
		time_counter = 0
		time_to_wait = 1*60*60
		fa = "temp/%s%s/%s%s%s%s.fa" %(str(date.year).zfill(4),str(date.month).zfill(2), str(date.year).zfill(4),str(date.month).zfill(2),str(date.day).zfill(2),str(t).zfill(2))
		while not os.path.exists(fa):
			time.sleep(1*30)
			time_counter += 1*30
			if time_counter > time_to_wait:
				stop = stop + 1
				break

		if os.path.exists(fa):
			tmps5=time.time()
		### ---------------------------------------------------------------------------
		### Fichier fa
			#fa = "arome500m.FC.20200307.00."+ech+".fa"
			FILE = epygram.formats.resource(fa, 'r')
			#FILE = fonction_recup.recup(date,t)

		### ---------------------------------------------------------------------------
		#-------------------Rayonnement---------------
			tmp_SURFRAYT_SOLA_DE = FILE.readfield('SURFRAYT SOLA DE')
			tmp_SURFRAYT_THER_DE = FILE.readfield('SURFRAYT THER DE')
			tmp_SURFFLU_RAY_SOLA = FILE.readfield('SURFFLU.RAY.SOLA')
			tmp_SURFFLU_RAY_THER = FILE.readfield('SURFFLU.RAY.THER')
			tmp_SOMMFLU_RAY_SOLA = FILE.readfield('SOMMFLU.RAY.SOLA')
			tmp_SOMMFLU_RAY_THER = FILE.readfield('SOMMFLU.RAY.THER')
			tmp_SURFRAYT_SOLAIRE = FILE.readfield('SURFRAYT.SOLAIRE')
			tmp_SURFRAYT_TERREST = FILE.readfield('SURFRAYT.TERREST')
			tmp_SOMMRAYT_SOLAIRE = FILE.readfield('SOMMRAYT.SOLAIRE')
			tmp_SOMMRAYT_TERREST = FILE.readfield('SOMMRAYT.TERREST')
			tmp_S001RAYT_SOL_CL = FILE.readfield('S001RAYT SOL CL')
			tmp_S001RAYT_THER_CL = FILE.readfield('S001RAYT THER CL')
			tmp_S090RAYT_SOL_CL = FILE.readfield('S090RAYT SOL CL')
			tmp_S090RAYT_THER_CL = FILE.readfield('S090RAYT THER CL')
			tmp_SURFRAYT_DIR_SUR = FILE.readfield('SURFRAYT DIR SUR')
			tmp_TOPRAYT_DIR_SOM = FILE.readfield('TOPRAYT DIR SOM')
			tmp_SURFDIR_NORM_IRR = FILE.readfield('SURFDIR NORM IRR')

		#------------------Nebulosité----------------
			tmp_ATMONEBUL_TOTALE = FILE.readfield('ATMONEBUL.TOTALE')
			tmp_ATMONEBUL_HAUTE = FILE.readfield('ATMONEBUL.HAUTE')
			tmp_ATMONEBUL_MOYENN = FILE.readfield('ATMONEBUL.MOYENN')
			tmp_ATMONEBUL_BASSE = FILE.readfield('ATMONEBUL.BASSE')
			tmp_SURFNEBUL_TOTALE = FILE.readfield('SURFNEBUL.TOTALE')
			tmp_SURFNEBUL_HAUTE = FILE.readfield('SURFNEBUL.HAUTE')
			tmp_SURFNEBUL_MOYENN = FILE.readfield('SURFNEBUL.MOYENN')
			tmp_SURFNEBUL_BASSE = FILE.readfield('SURFNEBUL.BASSE')

			tmp_SURFPRESSION = FILE.readfield('SURFPRESSION')
			tmp_SURFTEMPERATURE = FILE.readfield('SURFTEMPERATURE')

		#------------------Variable 3D---------------
			tmp_HUMI_SPECIFI = FILE.readfields('S*HUMI.SPECIFI')
			tmp_CLOUD_WATER  = FILE.readfields('S*CLOUD_WATER')
			tmp_CLOUD_FRACTI = FILE.readfields('S*CLOUD_FRACTI')
			tmp_TEMPERATURE = FILE.readfields('S*TEMPERATURE')
			tmp_ICE_CRYSTAL = FILE.readfields('S*ICE_CRYSTAL')
			tmp_SNOW = FILE.readfields('S*SNOW')
			tmp_GRAUPEL = FILE.readfields('S*GRAUPEL')
			tmp_RAIN = FILE.readfields('S*RAIN')


			FILE.close()
			tmps6=time.time()
			print("Temps pour la lecture des données", tmps6-tmps5)
		### ============================================================================
		### Transformation en numpy et suppression de la zone E - VARIABLES 2D
			tmp_ATMONEBUL_TOTALE = fonctions_fa_nc.getdata2D(tmp_ATMONEBUL_TOTALE)[:nlons, :nlats]
			tmp_ATMONEBUL_HAUTE = fonctions_fa_nc.getdata2D(tmp_ATMONEBUL_HAUTE)[:nlons, :nlats]
			tmp_ATMONEBUL_MOYENN = fonctions_fa_nc.getdata2D(tmp_ATMONEBUL_MOYENN)[:nlons, :nlats]
			tmp_ATMONEBUL_BASSE = fonctions_fa_nc.getdata2D(tmp_ATMONEBUL_BASSE)[:nlons, :nlats]
			tmp_SURFNEBUL_TOTALE = fonctions_fa_nc.getdata2D(tmp_SURFNEBUL_TOTALE)[:nlons, :nlats]
			tmp_SURFNEBUL_HAUTE = fonctions_fa_nc.getdata2D(tmp_SURFNEBUL_HAUTE)[:nlons, :nlats]
			tmp_SURFNEBUL_MOYENN = fonctions_fa_nc.getdata2D(tmp_SURFNEBUL_MOYENN)[:nlons, :nlats]
			tmp_SURFNEBUL_BASSE = fonctions_fa_nc.getdata2D(tmp_SURFNEBUL_BASSE)[:nlons, :nlats]
			tmp_SURFRAYT_SOLA_DE = fonctions_fa_nc.getdata2D(tmp_SURFRAYT_SOLA_DE)[:nlons, :nlats]
			tmp_SURFRAYT_THER_DE = fonctions_fa_nc.getdata2D(tmp_SURFRAYT_THER_DE)[:nlons, :nlats]
			tmp_SURFFLU_RAY_SOLA = fonctions_fa_nc.getdata2D(tmp_SURFFLU_RAY_SOLA)[:nlons, :nlats]
			tmp_SURFFLU_RAY_THER = fonctions_fa_nc.getdata2D(tmp_SURFFLU_RAY_THER)[:nlons, :nlats]
			tmp_SOMMFLU_RAY_SOLA = fonctions_fa_nc.getdata2D(tmp_SOMMFLU_RAY_SOLA)[:nlons, :nlats]
			tmp_SOMMFLU_RAY_THER = fonctions_fa_nc.getdata2D(tmp_SOMMFLU_RAY_THER)[:nlons, :nlats]
			tmp_SURFRAYT_SOLAIRE = fonctions_fa_nc.getdata2D(tmp_SURFRAYT_SOLAIRE)[:nlons, :nlats]
			tmp_SURFRAYT_TERREST = fonctions_fa_nc.getdata2D(tmp_SURFRAYT_TERREST)[:nlons, :nlats]
			tmp_S001RAYT_SOL_CL = fonctions_fa_nc.getdata2D(tmp_S001RAYT_SOL_CL)[:nlons, :nlats]
			tmp_S001RAYT_THER_CL = fonctions_fa_nc.getdata2D(tmp_S001RAYT_THER_CL)[:nlons, :nlats]
			tmp_S090RAYT_SOL_CL = fonctions_fa_nc.getdata2D(tmp_S090RAYT_SOL_CL)[:nlons, :nlats]
			tmp_S090RAYT_THER_CL = fonctions_fa_nc.getdata2D(tmp_S090RAYT_THER_CL)[:nlons, :nlats]
			tmp_SURFRAYT_DIR_SUR = fonctions_fa_nc.getdata2D(tmp_SURFRAYT_DIR_SUR)[:nlons, :nlats]
			tmp_TOPRAYT_DIR_SOM = fonctions_fa_nc.getdata2D(tmp_TOPRAYT_DIR_SOM)[:nlons, :nlats]
			tmp_SURFDIR_NORM_IRR = fonctions_fa_nc.getdata2D(tmp_SURFDIR_NORM_IRR)[:nlons, :nlats]

			tmp_SURFPRESSION = fonctions_fa_nc.getdata2D(tmp_SURFPRESSION)[:nlons, :nlats]
			tmp_SURFTEMPERATURE = fonctions_fa_nc.getdata2D(tmp_SURFTEMPERATURE)[:nlons, :nlats]


			tmp_HUMI_SPECIFI = fonctions_fa_nc.getdata3D(tmp_HUMI_SPECIFI)[:nlons, :nlats, :]
			tmp_CLOUD_WATER  = fonctions_fa_nc.getdata3D(tmp_CLOUD_WATER)[:nlons, :nlats, :]
			tmp_CLOUD_FRACTI = fonctions_fa_nc.getdata3D(tmp_CLOUD_FRACTI)[:nlons, :nlats, :]
			tmp_TEMPERATURE = fonctions_fa_nc.getdata3D(tmp_TEMPERATURE)[:nlons, :nlats, :]
			tmp_ICE_CRYSTAL = fonctions_fa_nc.getdata3D(tmp_ICE_CRYSTAL)[:nlons, :nlats, :]
			tmp_SNOW = fonctions_fa_nc.getdata3D(tmp_SNOW)[:nlons, :nlats, :]
			tmp_RAIN = fonctions_fa_nc.getdata3D(tmp_RAIN)[:nlons, :nlats, :]
			tmp_GRAUPEL = fonctions_fa_nc.getdata3D(tmp_GRAUPEL)[:nlons, :nlats, :]

			tmps7=time.time()
			print("Temps pour la transformation en numpy", tmps7-tmps6)
		### ============================================================================
		### Ecritude des variables dans le fichier NetCDF - Variables 2D
			ATMONEBUL_TOTALE[t,::]   = tmp_ATMONEBUL_TOTALE.T
			ATMONEBUL_HAUTE[t,::]   = tmp_ATMONEBUL_HAUTE.T
			ATMONEBUL_MOYENN[t,::]   = tmp_ATMONEBUL_MOYENN.T
			ATMONEBUL_BASSE[t,::]   = tmp_ATMONEBUL_BASSE.T
			SURFNEBUL_TOTALE[t,::]   = tmp_SURFNEBUL_TOTALE.T
			SURFNEBUL_HAUTE[t,::]   = tmp_SURFNEBUL_HAUTE.T
			SURFNEBUL_MOYENN[t,::]   = tmp_SURFNEBUL_MOYENN.T
			SURFNEBUL_BASSE[t,::]   = tmp_SURFNEBUL_BASSE.T
			SURFRAYT_SOLA_DE[t,::]   = tmp_SURFRAYT_SOLA_DE.T
			SURFRAYT_THER_DE[t,::]   = tmp_SURFRAYT_THER_DE.T
			SURFFLU_RAY_SOLA[t,::]   = tmp_SURFFLU_RAY_SOLA.T
			SURFFLU_RAY_THER[t,::]   = tmp_SURFFLU_RAY_THER.T
			SOMMFLU_RAY_SOLA[t,::]   = tmp_SOMMFLU_RAY_SOLA.T
			SOMMFLU_RAY_THER[t,::]   = tmp_SOMMFLU_RAY_THER.T
			SURFRAYT_SOLAIRE[t,::]   = tmp_SURFRAYT_SOLAIRE.T
			SURFRAYT_TERREST[t,::]   = tmp_SURFRAYT_TERREST.T
			S001RAYT_SOL_CL[t,::]   = tmp_S001RAYT_SOL_CL.T
			S001RAYT_THER_CL[t,::]   = tmp_S001RAYT_THER_CL.T
			S090RAYT_SOL_CL[t,::]   = tmp_S090RAYT_SOL_CL.T
			S090RAYT_THER_CL[t,::]   = tmp_S090RAYT_THER_CL.T

			SURFRAYT_DIR_SUR[t,::]   = tmp_SURFRAYT_DIR_SUR.T
			TOPRAYT_DIR_SOM[t,::]   = tmp_TOPRAYT_DIR_SOM.T
			SURFDIR_NORM_IRR[t,::]   = tmp_SURFDIR_NORM_IRR.T

			SURFPRESSION[t,::]   = tmp_SURFPRESSION.T
			SURFTEMPERATURE[t,::]   = tmp_SURFTEMPERATURE.T



			for z in range(nalts):
				HUMI_SPECIFI[t,:,:,z] = tmp_HUMI_SPECIFI[:,:,z].T
				CLOUD_WATER[t,:,:,z]  = tmp_CLOUD_WATER[:,:,z].T
				CLOUD_FRACTI[t,:,:,z] = tmp_CLOUD_FRACTI[:,:,z].T
				TEMPERATURE[t,:,:,z] = tmp_TEMPERATURE[:,:,z].T
				ICE_CRYSTAL[t,:,:,z] = tmp_ICE_CRYSTAL[:,:,z].T
				SNOW[t,:,:,z] = tmp_SNOW[:,:,z].T
				RAIN[t,:,:,z] = tmp_RAIN[:,:,z].T
				GRAUPEL[t,:,:,z] = tmp_GRAUPEL[:,:,z].T

			CHECK[t] = 'OK'

			#======================
			#====== Suppresion du fichier .fa
			#======================
			os.remove(fa)
			print("%s remove" %(fa))
			tmps3=time.time()
			print("Temps pour lecriture", tmps3-tmps7)
			print("Temps pour une boucle:", tmps3-tmps5)

		else:
			CHECK[t] = 'NOT OK'
			print("%s n'a pas eu le temps d'être transféré" %(fa))

	tmps4=time.time()
	print("Temps un jour sans préparation:", tmps4-tmps2p)



	file_nc.close()

