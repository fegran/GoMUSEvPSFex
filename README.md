# GoMUSE vPSFex

Repository containing scripts to perform PSF photometry on MUSE slices.
Heavily based on Sextractor/PSFex.

Very unstable for the moment. All feedback on this project is valuable.

Felipe Gran (PUC/MAS/ESO internship)

fegran@uc.cl

## Intended usage 

The exection of the program occurs in a working folder, that 
at the begining contains:

```
default files for Sextractor/PSFex
Raw datacube 
Field of View images (White,V,R,I)
GoMUSEvPSFex.py
```

The python programme (**GoMUSEvPSFex.py**) can be divided in two mayor branches: "User parameters" and "Main features".
The last branch also is divided in three mayor phases that the first two can be operate separatelly:

 - Phase 1: Perform PSF photometry on VRI FoV images and create the catalogs.
 - Phase 2: Separate slices using MissFITS to prepare to ~~Phase 3~~.
 - Phase 3: Iterate over all the 3720 MUSE slices and perform PSF photometry creating individual catalogs.

## Version 1.0 (20.03.2019)

[x] Base code the perform PSF photometry over MUSE slices.
[x] Base code to create the CMDs of the field.