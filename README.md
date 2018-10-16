# COMPEST
A framework connecting COMSOL Multiphysics and PEST (coming soon...)

## Overview
COMPEST is a program written in _java_ that enables advanced parameter estimation, sensitivity analysis, uncertainty analysis, and data-worth analysis to investigate ad solve inverse problems using forward finite-element models. The software functions as a link between [PEST](http://www.pesthomepage.org/) and [COMSOL Multiphysics](http://www.comsol.com). Although the software's functionality has been demonstarted with application to isotopic fractionation in the diffusion and degradation of chlorinated contaminants in the subsurface, any problem that can be modelled in COMSOL Multiphysics can be handled with some modification of the code.

## Requirements
* _(proprietary)_ COMSOL Multiphysics Server (tested with ver. 5.3) and COMSOL Java API _(proprietary)_
* _(free)_ Java IDE (tested with ver. 1.8), 
* _(free)_ PEST (ver. 12.1.0 executable included here)

## How-to:
* First, it is recommended you read the article: +INSERT DOI HERE+
* _to do_

## Useful commands (in Windows cmd):
To compile COMPEST (run in the project directory):\
`javac -cp "C:\Program Files\COMSOL\COMSOL53\Multiphysics\plugins\*" -verbose COMPEST.java`

To execute COMPEST:\
`java -cp .;"C:\Program Files\COMSOL\COMSOL53\Multiphysics\plugins\*" COMPEST`

To launch COMSOL server so that it doesn't close upon disconnect:\
`"C:\Program Files\COMSOL\COMSOL53\Multiphysics\bin\win64\comsolmphserver.exe" -multi on`

_Replace the paths with the locations of your COMSOL java API files or server executable where necessary._
