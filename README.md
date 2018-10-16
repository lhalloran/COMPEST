# COMPEST
A framework connecting COMSOL Multiphysics and PEST *(coming soon...)*

## Overview
COMPEST is a program written in _java_ that enables advanced parameter estimation, sensitivity analysis, uncertainty analysis, and data-worth analysis to investigate ad solve inverse problems using forward finite-element models. The software functions as a link between [PEST](http://www.pesthomepage.org/) and [COMSOL Multiphysics](http://www.comsol.com). Although the software's functionality has been demonstarted with application to isotopic fractionation in the diffusion and degradation of chlorinated contaminants in the subsurface, any problem that can be modelled in COMSOL Multiphysics can be handled with some modification of the code.

## Requirements
* _(proprietary)_ COMSOL Multiphysics Server (tested with ver. 5.3) and COMSOL Java API
* _(free)_ Java IDE (tested with ver. 1.8), 
* _(free)_ PEST (ver. 12.1.0 executable included here)

## How-to:
* Firstly, it is recommended you read the article: **INSERT DOI HERE**
* Secondly, it is recommended to have some familiarity with PEST (see Doherty 2016).

1. **Define:**
   1. Define problem for which observations (measurements) exist and for which a finite-element model can be created.
   1. Choose which parameters to vary (e.g., to be estimated, to investigate uncertainty, etc.)
1. **Prepare COMSOL Model:**
   1. Set up time-dependent model in COMSOL. (Note: stationary models may work too, but this will require some creativity on your part).
   1. Ensure all parameters to be varied are defined as "
   1. Set model output times to the times of the observations.
   1. Delete the values of parameters to be varied (having them present can result in a duplicate definition error).
   1. Launch the COMSOL Server in a separate command prompt using `"C:\XXXXXX\COMSOL53\Multiphysics\bin\win64\comsolmphserver.exe" -multi on` where `XXXXXX` is the location of your COMSOL installation.
1. **Prepare PEST:**
   1. **to do**
1. **Prepare COMPEST:**
    1. If needed (e.g., COMSOL Java API plugins not in same location as mentioned in **Useful Commands** below), compile the java _class_ file using `javac -cp "C:\XXXXXX\COMSOL53\Multiphysics\plugins\*" COMPEST.java` where `XXXXXX` is the location of your COMSOL installation.
   1. Define all parametes in the define.properties file (an explanation of all parameters is contained in the file header).
   1. Ensure batch file is referring to correct location of COMSOL Java API files (see **Useful Commands** below). 
1. **Make it happen:**
   1. Execute the PEST-COMPEST-COMSOL by typing `PEST PCFFILENAME` in the command prompt, where `PCFFILENAME` is the name of the `.pst` "PEST Control File".
  

## Useful commands (in Windows cmd):
To compile COMPEST (run in the project directory):\
`javac -cp "C:\Program Files\COMSOL\COMSOL53\Multiphysics\plugins\*" -verbose COMPEST.java`

To execute COMPEST:\
`java -cp .;"C:\Program Files\COMSOL\COMSOL53\Multiphysics\plugins\*" COMPEST`

To launch COMSOL server so that it doesn't close upon disconnect:\
`"C:\Program Files\COMSOL\COMSOL53\Multiphysics\bin\win64\comsolmphserver.exe" -multi on`

_Replace the paths with the locations of your COMSOL java API files or server executable where necessary._

## References:
* Doherty, J. (2016). PEST Model-Independent Parameter Estimation User Manual Part I: PEST, SENSAN and Global Optimisers (6th ed.). Brisbane: Watermark Numerical Computing.
