#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import epygram
epygram.init_env()
import numpy as np
from bronx.meteo.conversion import q2R


def get_pressure_level(data_arome):
    # En entree le data sortie d'epygram
   
    #Niveaux hybride
    A = [level[1]['Ai'] for level in data_arome.geometry.vcoordinate.grid['gridlevels']][1:]
    B = [level[1]['Bi'] for level in data_arome.geometry.vcoordinate.grid['gridlevels']][1:]
    surfpression = data_arome.readfield('SURFPRESSION')
    surfpression.sp2gp()
    
    #Niveaux Pression
    surfpression_data= np.float32(np.exp(surfpression.getdata()[:][:]))#[i0:i1,j0:j1]))

    #P_mass = epygram.profiles.hybridP2masspressure(A,B,Psurf=surfpression_data,vertical_mean = 'geometric')
    P = epygram.profiles.hybridP2fluxpressure(A,B,Psurf=surfpression_data)
    #print(np.shape(P_mass), np.shape(P))
    P=P.T
    i0, j0, z0 = np.shape(P)
    P_out = np.zeros((j0,i0,z0))

    for i in range(i0):
        for j in range(j0):
            P_out[j,i,:] = P[i,j,:]

    return P_out    #tableau 3D de la pression en Pa

def get_pressure_sans_epygram(data_arome):
   # En entree le data sortie d'epygram
   
    #Niveaux hybride
    A = [level[1]['Ai'] for level in data_arome.geometry.vcoordinate.grid['gridlevels']][1:]
    B = [level[1]['Bi'] for level in data_arome.geometry.vcoordinate.grid['gridlevels']][1:]
    surfpression = data_arome.readfield('SURFPRESSION')
    surfpression.sp2gp()
    
    #Niveaux Pression
    surfpression_data= np.float32(np.exp(surfpression.getdata()[:][:]))#[i0:i1,j0:j1]))

    P_mass = epygram.profiles.hybridP2masspressure(A,B,Psurf=surfpression_data,vertical_mean = 'geometric')
    P = epygram.profiles.hybridP2fluxpressure(A,B,Psurf=surfpression_data)
    print(np.shape(P_mass), np.shape(P))
    #press_ref_half_level[it1,it2,:] = hybrid_coef_A_ref[:] + hybrid_coef_B_ref[:] * ground_pressure[it1,it2]
    P=P.T
    i0, j0, z0 = np.shape(P)
    P_out = np.zeros((j0,i0,z0))
    print(A)
    for i in range(i0):
        for j in range(j0):
            P_out[j,i,:] = P[i,j,:]
            #z in range(z0):
                #P_out[j,i,z] =  

    return P_out    #tableau 3D de la pression en Pa 

def get_z(fa_arome,i_lat,i_lon):
    #Lecture fu fichier FA
    FILE = epygram.formats.resource(fa_arome,"r")

    #Coefficients A et B, coordonnees hybrides pression
    A = [level[1]['Ai'] for level in FILE.geometry.vcoordinate.grid['gridlevels']][1:]
    B = [level[1]['Bi'] for level in FILE.geometry.vcoordinate.grid['gridlevels']][1:]

    #Lecture du profil vertical de temperature au point lat/lon
    t = FILE.extractprofile('S*TEMPERATURE', i_lon, i_lat)
    t_profile = t.data

    #Lecture du profil vertical d humidite specifique au point lat/lon
    q = FILE.extractprofile('S*HUMI.SPECIFI', i_lon, i_lat)
    #Conversion en profil de R specific gas constant (J/kg/K)
    r = q2R(q)
    R_profile = r.data

    #Lecture de la pression de surface (qui est en perturbation de pression autour de pression de reference) + conversion en Pa
    surfpression = FILE.readfield('SURFPRESSION')
    surfpression.sp2gp()
    psurface=(surfpression.getvalue_ll(i_lon, i_lat) + 1013.25) *100.0

    #Conversion de la coordonnee hybride pression en altitude
    # Les [6:] sont la pour eviter de manier des coefficients A=B=0, specificites de la fonction hybridP2altitude 
    Z = epygram.profiles.hybridP2altitude(A[6:],B[6:],R_profile[6:], t_profile[6:], Psurf=psurface, vertical_mean='geometric')
    return Z
    
def getdata3D(FIELD_SET):
   
    #FIELD_SET en entree
    #Sors un numpy 3D
   
    nx= FIELD_SET[0].geometry.dimensions['X']
    ny = FIELD_SET[0].geometry.dimensions['Y']
    nz= len(FIELD_SET)

    DATA3D = np.zeros((ny,nx,len(FIELD_SET)))

    for z in range(0,nz) :
       
        try :
            DATA3D[:,:,z] = FIELD_SET[z].getdata()
        except:
            FIELD_SET[z].sp2gp()
            DATA3D[:,:,z] = FIELD_SET[z].getdata()
       
    return DATA3D

def getdata2D(FIELD_SET):
   
    #FIELD_SET en entree
    #Sors un numpy 2D
   
    nx= FIELD_SET.geometry.dimensions['X']
    ny = FIELD_SET.geometry.dimensions['Y']

    DATA2D = np.zeros((ny,nx))

    try :
        DATA2D[:,:] = FIELD_SET.getdata()
    except:
        FIELD_SET.sp2gp()
        DATA2D[:,:] = FIELD_SET.getdata()
       
    return DATA2D

    
def water_path(MICRO3D_data,Pressure_levels):
    # P en Pa <-> kg.m-1.s-2
    # MICRO3D_data en kg.kg-1
    g=9.80665 #constant gravite m.s-2

    ny,nx,nz = np.shape(MICRO3D_data)
    MICRO_WP_data = np.zeros((ny,nx))
    for z in range(1,nz):
        MICRO_WP_data[:,:] = MICRO_WP_data[:,:]+(Pressure_levels[:,:,z]-Pressure_levels[:,:,z-1])*(MICRO3D_data[:,:,z])#+MICRO3D_data[:,:,z-1])/2 #MICRO_WP_data[:,:]+(Pressure_levels[z+1]-Pressure_levels[z])*100*(MICRO3D_data[:,:,z+1]-MICRO3D_data[:,:,z]) #*100 pour passer de hPa en Pa #Systeme International
    MICRO_WP_data = MICRO_WP_data/g

    return MICRO_WP_data #en kg/m-2 numpy 2D


def water_path1D(MICRO3D_data,Pressure_levels):
    # P en Pa <-> kg.m-1.s-2
    # MICRO3D_data en kg.kg-1
    g=9.80665 #constant gravite m.s-2

    nz = len(MICRO3D_data)
    MICRO_WP_data = 0
    for z in range(1,nz):
        MICRO_WP_data = MICRO_WP_data+(Pressure_levels[z]-Pressure_levels[z-1])*(MICRO3D_data[z])#+MICRO3D_data[:,:,z-1])/2 #MICRO_WP_data[:,:]+(Pressure_levels[z+1]-Pressure_levels[z])*100*(MICRO3D_data[:,:,z+1]-MICRO3D_data[:,:,z]) #*100 pour passer de hPa en Pa #Systeme International
    MICRO_WP_data = MICRO_WP_data/g

    return MICRO_WP_data #en kg/m-2 numpy 1D

