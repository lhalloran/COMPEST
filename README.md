# COMPEST
A framework connecting COMSOL Multiphysics and PEST (coming soon...)

## Useful commands (in Windows cmd):
To compile COMPEST (run in the project directory):\
`javac -cp "C:\Program Files\COMSOL\COMSOL53\Multiphysics\plugins\*" -verbose COMPEST.java`

To execute COMPEST:\
`java -cp .;"C:\Program Files\COMSOL\COMSOL53\Multiphysics\plugins\*" COMPEST`

To launch COMSOL server so that it doesn't close upon disconnect:\
`"C:\Program Files\COMSOL\COMSOL53\Multiphysics\bin\win64\comsolmphserver.exe" -multi on`

_Replace the paths with the locations of your COMSOL java API files or server executable where necessary._
