# GoMUSE vPSFex

This repository contains scripts to perform PSF photometry on MUSE slices.
Heavily based on Sextractor/PSFex.

Very unstable for the moment. All feedback on this project is valuable.

Felipe Gran (PUC/MAS/ESO internship)

fegran@uc.cl

## Intended usage 

The execution of the program occurs in a working folder, that 
at the beginning contains:

```
default files for Sextractor/PSFex
Raw datacube 
Field of View images (White,V,R,I)
GoMUSEvPSFex.py
```

The python programme (**GoMUSEvPSFex.py**) can be divided in two major branches: "User parameters" and "Main features".
The last branch also is divided into three major phases that the first two can be operated separately:

 - Phase 1: Perform PSF photometry on VRI FoV images and create the catalogs.
 - Phase 2: Separate slices using MissFITS to prepare to **Phase 3**.
 - Phase 3: **After Phase 2**, iterate over all the 3720 MUSE slices and perform PSF photometry creating individual catalogs.

## Version 1.0 (20.03.2019)

[x] Base code the perform PSF photometry over MUSE slices.

[x] Base code to create the CMDs of the field.

[x] Basic information to change scripts to the user preferences.

## Future ideas

[] Keep the default Sextractor/PSFex files on a separate unchanged folder

[] Comment and add the original python aperture photometry code (based on astropy.photutils) to compare results with GoMUSEvPSFex.

[] Add IPython Notebooks with examples.

## Collaborators

 - Elena Valenti
 - Giacomo Beccari