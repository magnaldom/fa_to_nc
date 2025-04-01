#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Performances:
# ne pas charger tous les tableaux en mémoire en même temps
# ne pas écrire dans le fichier netcdf en faisant une boucle sur les niveaux
#Performances pour le traitement d'une échéance:
# NETCDF4-HDF5, zlib=True, complevel=1:
#   temps: lecture 50s, écriture 150s, réarrangement mémoire 25s, total 230s
#   taille: 
# NETCDF4-HDF5, zlib=False:
#   temps: lecture 52s, écriture 38s, réarrangement mémoire 25s, total 120s 
#   taille:

### ============================================================================
### Transformation des fichiers FA de sortie de modèle en un fichier unique en
### format NetCDF.
###

### ============================================================================

### PACKAGES
import sys; sys.path.insert(0,'/cnrm/phynh/data1/magnaldom/Outils')
import netCDF4 as nc
import numpy as np
import os
import time
#SR pourquoi faire le reload?
#SR import imp
#SR imp.reload(fonctions_fa_nc)
import fonction_recup_analyse
from datetime import datetime, timedelta
import sys
from masse_lwp_iwp import water_path
from calcul_pression import calcul_pression_up
from num_jour_between import num_jour_between
import epygram
epygram.init_env()
import netCDF4 as nc
from netCDF4 import Dataset
#import subprocess
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

fichier = "/d0/Users/magnaldom/STOCKAGE_AROME_UP/A_B_AROME.nc"
A_B = Dataset(fichier, "r", format="NETCDF4")
A = A_B.variables["A"][:]
B = A_B.variables["B"][:]
A_B.close()

os.system("rm -f /d0/Users/magnaldom/STOCKAGE_AROME_UP/DATA/temp/%s%s/*" %(str(date1.year),str(date1.month).zfill(2)))

os.system("python3 prestaging_analyse.py %s %s &" %(date_temp1, date_temp2))

os.system("python3 script_recup.py %s %s &" %(date_temp1, date_temp2))
#subprocess.run(["python3 script_recup.py %s %s" %(date_temp1, date_temp2)])
print("Script_recup lancé")
### ============================================================================
#SR Si je comprends bien ça va rechercher à nouveau le fichier sur hendrix
#   est-ce qu'il ne suffirait pas de l'attendre?
try:
  FILE = fonction_recup_analyse.recup_up(date1,0)
  #fa = "historic.arome.fog"+res+"-"+res+"m000+0000:00.fa"
  #FILE = epygram.formats.resource(fa, 'r')
except:
  print("Fichiers non disponibles " )
  sys.exit()
FILE.close()

### Variables
# Rayonnement
vars_2D = ['SURFRAYT SOLA DE', 'SURFRAYT THER DE', 'SURFFLU.RAY.SOLA', 'SURFFLU.RAY.THER', 'SOMMFLU.RAY.SOLA',
          'SOMMFLU.RAY.THER', 'SURFRAYT.SOLAIRE', 'SURFRAYT.TERREST', 'SOMMRAYT.SOLAIRE', 'SOMMRAYT.TERREST',
          'S001RAYT SOL CL', 'S001RAYT THER CL', 'S090RAYT SOL CL', 'S090RAYT THER CL', 'SURFRAYT DIR SUR',
          'TOPRAYT DIR SOM', 'SURFDIR NORM IRR']


# Nébulosté
vars_2D.extend(['ATMONEBUL.TOTALE', 'ATMONEBUL.HAUTE', 'ATMONEBUL.MOYENN', 'ATMONEBUL.BASSE', 'SURFNEBUL.TOTALE',
                'SURFNEBUL.HAUTE', 'SURFNEBUL.MOYENN', 'SURFNEBUL.BASSE'])
# Autres
vars_2D.extend(['SURFPRESSION', 'SURFTEMPERATURE','SURFFLU.LAT.MEVA','SURFFLU.LAT.MSUB','SURFFLU.MEVAP.EA','SURFFLU.MSUBL.NE','SURFFLU.CHA.SENS'])

vars_2D.extend(['HUMI_SPECIFI_2D',
            'CLOUD_WATER_2D','ICE_CRYSTAL_2D',
            'SNOW_2D','RAIN_2D','GRAUPEL_2D'])

vars_3D = ['HUMI.SPECIFI', 'CLOUD_WATER',  'ICE_CRYSTAL',
          'SNOW', 'GRAUPEL', 'RAIN']

vars_3D.extend(['CLOUD_FRACTI', 'TEMPERATURE'])


fa_0 =  "/d0/Users/magnaldom/STOCKAGE_AROME_UP/temp/%s%s/%s%s%s%s.fa" %( str(date1.year).zfill(4), str(date1.month).zfill(2),
                                                                                    str(date1.year).zfill(4),
                                                                                    str(date1.month).zfill(2), str(date1.day).zfill(2), str(0).zfill(2))
tmps = time.time()
FILE = epygram.formats.resource(fa_0, 'r')
LONGITUDE, LATITUDE = FILE.geometry.get_lonlat_grid(subzone = "CI")
nlons, nlats = LONGITUDE.shape
nalts = len(FILE.geometry.vcoordinate.levels)
FILE.close()
print("Temps de lecture de la géométrie", time.time() - tmps)

#SR il vaudrait mieux ne pas récupérer ce fichier et utiliser celui à H+1
os.remove(fa_0)
###============================================================================
stop = 0
num_jour = num_jour_between(date1,date2)
for d in range(0, num_jour):
  if stop > 5 :
    break
  date = date1 + timedelta(days = d)
  print(date)

  tmps = time.time()
  file_nc = nc.Dataset("/d0/Users/magnaldom/STOCKAGE_AROME_UP/DATA/%s%s/AROME_%s%s%s.nc" %(str(date.year).zfill(4), str(date.month).zfill(2),
                                                                                                str(date.year).zfill(4), str(date.month).zfill(2),
                                                                                                str(date.day).zfill(2)), "w", format="NETCDF4")
  #file_nc = nc.Dataset("test.nc","w",format="NETCDF4")

  ### ---------------------------------------------------------------------------
  ### Dimensions
  file_nc.createDimension('time', None)
  file_nc.createDimension('alt', nalts)
  file_nc.createDimension('lon', nlons)
  file_nc.createDimension('lat', nlats)

  ### ---------------------------------------------------------------------------
  ### Variables dimentions
  longitude     = file_nc.createVariable('Longitude', 'f4', dimensions=('lat','lon',))
  latitude    = file_nc.createVariable('Latitude', 'f4', dimensions=('lat','lon',))
  niveau_altitude = file_nc.createVariable('Niveau_alt', 'i4', 'alt')
  echeance    = file_nc.createVariable('Echeance', 'i4', 'time')

  ### ---------------------------------------------------------------------------
  ### Variables
  kwargs_vars = dict(zlib=True, complevel=1)
  varsnc = {}
  for fid in vars_2D:
    name = fid.replace(' ', '_').replace('.', '_')
    varsnc[name] = file_nc.createVariable(name, 'f4', dimensions=('time','lat', 'lon'), **kwargs_vars)

  for fid in vars_3D:
    name = fid.replace(' ', '_').replace('.', '_')
    varsnc[name] = file_nc.createVariable(name, 'f4', dimensions=('time','lat', 'lon', 'alt'), **kwargs_vars)

  varsnc['CHECK'] = file_nc.createVariable('CHECK', 'S8', dimensions=('time'), **kwargs_vars)

  print("Temps préparation des variables:", time.time() - tmps)

  ### ---------------------------------------------------------------------------
  ### Ecritude des variables de dimension
  longitude[::]    = LONGITUDE.T
  latitude[::]     = LATITUDE.T
  #echeance[:]    = np.arange(nechs)
  niveau_altitude[:] = np.arange(nalts)


  ### ============================================================================
  ### ============================================================================
  ### Boucles sur les échéances
  tmps2p=time.time()

  t_deb = 1
  t_fin = 23
  for t in range(t_deb, t_fin):
    #====================
    # Attendre que le fichier.fa soit recup
    #====================
    time_counter = 0
    time_to_wait = 1*60*60
    fa = "/d0/Users/magnaldom/STOCKAGE_AROME_UP/temp/%s%s/%s%s%s%s.fa" %(str(date.year).zfill(4), str(date.month).zfill(2),
                                                                                     str(date.year).zfill(4),
                                                                                     str(date.month).zfill(2), str(date.day).zfill(2), str(t).zfill(2))
    while not os.path.exists(fa):
      time.sleep(1*30)
      time_counter += 1*30
      if time_counter > time_to_wait:
        stop = stop + 1
        break
    if os.path.exists(fa):
      tmps5 = time.time()
      temps_lecture = 0.
      temps_ecriture = 0.
      temps_arrangement_memoire = 0.
      ### ---------------------------------------------------------------------------
      ### Fichier fa
      #fa = "arome500m.FC.20200307.00."+ech+".fa"
      FILE = epygram.formats.resource(fa, 'r')
      #FILE = fonction_recup.recup(date,t)

      for fid in vars_2D[:-6]:
        sys.stdout.flush()
        name = fid.replace(' ', '_').replace('.', '_')
        #Lecture
        tmps = time.time()
        field = FILE.readfield(fid)
        temps_lecture += time.time() - tmps
        #Suppression de la zone E et écriture
        tmps = time.time()
        if field.spectral:
          field.sp2gp()
        varsnc[name][t,::] = field.getdata()[:nlons, :nlats].T
        temps_ecriture += time.time() - tmps
      
      tmp_SURFPRESSION = varsnc['SURFPRESSION'][t,::]
      PRESSION = calcul_pression_up(A, B, tmp_SURFPRESSION)

      for fid in vars_3D[:-2]:
        sys.stdout.flush()
        name = fid.replace(' ', '_').replace('.', '_')
        #Lecture
        tmps = time.time()
        fields = FILE.readfields('S*' + fid)
        temps_lecture += time.time() - tmps
        #Suppression de la zone E et écriture
        tmps = time.time()
        for field in fields:
          if field.spectral:
            field.sp2gp()
        #ATTENTION, readfields remonte SURFTEMPERATURE, S001TEMPERATURE, ... Il faut filtrer
        values = np.array([field.getdata()[:nlons, :nlats].T for field in fields if not field.fid['FA'].startswith('SURF')])
        values = np.moveaxis(values, 0, -1)
        temps_arrangement_memoire += time.time() - tmps
        tmps = time.time()
        varsnc[name][t,:,:,:] = values
        varsnc[name+'_2D'][t,:,:] = water_path(values, PRESSION)
        temps_ecriture += time.time() - tmps

      for fid in vars_3D[-2:]:
        sys.stdout.flush()
        name = fid.replace(' ', '_').replace('.', '_')
        #Lecture
        tmps = time.time()
        fields = FILE.readfields('S*' + fid)
        temps_lecture += time.time() - tmps
        #Suppression de la zone E et écriture
        tmps = time.time()
        for field in fields:
          if field.spectral:
            field.sp2gp()
        #ATTENTION, readfields remonte SURFTEMPERATURE, S001TEMPERATURE, ... Il faut filtrer
        values = np.array([field.getdata()[:nlons, :nlats].T for field in fields if not field.fid['FA'].startswith('SURF')])
        values = np.moveaxis(values, 0, -1)
        temps_arrangement_memoire += time.time() - tmps
        tmps = time.time()
        varsnc[name][t,:,:,:] = values
        temps_ecriture += time.time() - tmps

      FILE.close()
       
      varsnc['CHECK'][t] = 'OK'
      
      #======================
      #====== Suppresion du fichier .fa
      #======================
      os.remove(fa)
      print("%s remove" %(fa))
      print("Temps pour la lecture", temps_lecture)
      print("Temps pour l'ecriture", temps_ecriture)
      print("Temps pour le réarrangement en mémoire", temps_arrangement_memoire)
      print("Temps pour une boucle:", time.time() - tmps5)

    else:
      varsnc['CHECK'][t] = 'NOT OK'
      print("%s n'a pas eu le temps d'être transféré" %(fa))

  print("Temps un jour sans préparation:", time.time() - tmps2p)
  file_nc.close()
  
#os.system("python3 DATA_light/script_traitement_light_expe.py %s %s %s &" %(date_temp1, date_temp2, expe))

