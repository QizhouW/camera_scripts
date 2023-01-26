Step1:
conda activate cv  / or conda acitvate tiscam

Step2:
source tiscamera-env.sh

Step3:
run tiscam-capture in commandline. Choose the camera serial number with v4l2 mode.
Adjust the parameters and export to file setup.json.

Step4:
tcam-ctrl -l : list available device with serial number
tcam-ctrl -c serial_number : make sure your selected output format is supported here.

Step5:
Run the recording script
python full30.py -fname test -delay 10 -len 10 -serial 1234567