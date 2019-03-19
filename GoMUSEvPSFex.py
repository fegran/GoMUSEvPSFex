from joblib import Parallel, delayed
from astropy.io import fits
import pandas as pd
import numpy as np
import warnings
import glob
import os

warnings.filterwarnings('ignore')


########## USER PARAMETERS ######################

path = '/Users/felipegran/Desktop/Doctorado/ESO/m0.7m1.4pt1/'
datacube_name = 'm0.7m1.4pt1.fits' 
v_image = 'IMAGE_FOV_0002.fits'
r_image = 'IMAGE_FOV_0003.fits'
i_image = 'IMAGE_FOV_0004.fits'
reference_image = i_image

#################################################

#Create Folders 
os.system('mkdir fits cmds_psfex_output cmds_output slice_catalogs slice_psfex_output')
os.chdir('%s' %path) #move to path


##### Phase 1: Commands to execute the CMDs #####

os.system('sex -PARAMETERS_NAME default.param.ape -CATALOG_TYPE FITS_LDAC -CATALOG_NAME v.ldac %s,%s' %(reference_image,v_image))
os.system('sex -PARAMETERS_NAME default.param.ape -CATALOG_TYPE FITS_LDAC -CATALOG_NAME r.ldac %s,%s' %(reference_image,r_image))
os.system('sex -PARAMETERS_NAME default.param.ape -CATALOG_TYPE FITS_LDAC -CATALOG_NAME i.ldac %s,%s' %(reference_image,i_image))

os.system('psfex v.ldac')
os.system('psfex r.ldac')
os.system('psfex i.ldac')

os.system('sex -PARAMETERS_NAME default.param.psf.vri.psf -CATALOG_TYPE ASCII_HEAD -CATALOG_NAME v.psf.cat -PSF_NAME v.psf %s,%s' %(reference_image,v_image))
os.system('sex -PARAMETERS_NAME default.param.psf.vri.psf -CATALOG_TYPE ASCII_HEAD -CATALOG_NAME r.psf.cat -PSF_NAME r.psf %s,%s' %(reference_image,r_image))
os.system('sex -PARAMETERS_NAME default.param.psf.vri.psf -CATALOG_TYPE ASCII_HEAD -CATALOG_NAME i.psf.cat -PSF_NAME i.psf %s,%s' %(reference_image,i_image))

#Move output to cmds_psfex_output (PSF diagnostics) ...
os.system('mv chi_* proto_* resi_* samp_* nap_* cmds_psfex_output/')
os.system('mv *.ldac cmds_psfex_output/')
os.system('mv v.psf r.psf i.psf cmds_psfex_output/')
#... and cmds_output (catalogs)
os.system('mv v.psf.cat r.psf.cat i.psf.cat cmds_output/')

#############################################################



####### Phase 2: Slicing the DATACUBE ########################

os.system('mv %s %sfits/' %(datacube_name, path))
os.system('missfits -c ../default.missfits %' %datacube_name)

##############################################################



######### Phase 3: Sextractor/PSFex photometry on slices #########

data = glob.glob('fits/*.s*.fits') #select sliced fits

#Function to perform the parallel calls 
def sextractor(img):
    
    img_name = img[5:22]
    #
    cmd1 = 'sex -PARAMETERS_NAME default.param.ape -CATALOG_TYPE FITS_LDAC -CATALOG_NAME %s.ldac %s,%s' %(img_name,reference_image,img)
    os.system('%s' %cmd1)
    cmd2 = 'psfex %s.ldac' %(img_name)
    os.system('%s' %cmd2)
    cmd3 = 'sex -PARAMETERS_NAME default.param.psf -CATALOG_TYPE ASCII_HEAD -CATALOG_NAME %s.psf.cat -PSF_NAME %s.psf %s,%s' %(img_name,img_name,reference_image,img)
    os.system('%s' %cmd3)    
    
    os.system('mv samp_%s.fits slice_psfex_output/' %img_name)
    os.system('mv snap_%s.fits slice_psfex_output/' %img_name)
    os.system('mv resi_%s.fits slice_psfex_output/' %img_name)
    os.system('mv chi_%s.fits slice_psfex_output/' %img_name)
    os.system('mv proto_%s.fits slice_psfex_output/' %img_name)
    os.system('mv %s.psf slice_psfex_output/' %img_name)
    os.system('mv %s.ldac slice_psfex_output/' %img_name)
    
    os.system('mv %s.psf.cat slice_catalogs/' %img_name)

    pass

#Delete old failures :(
os.system('rm slice_catalogs/*.psf.cat')
#Explanation: Parallel for doing multiple slices at a time 
#n_jobs=-1 to select all the available cores 
#verbose=1 very little output, normally only to check if the system is doing well (Total slices: 3720)
#Then iterate over images in data (which contains all the slices)
Parallel(n_jobs=-1, verbose=1)(delayed(sextractor)(img) for img in data)
#At the end of the iteration the folder slice_catalogs/ will contains all the photometry catalogs

##############################################################