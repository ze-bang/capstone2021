# File: main.py
# Author: Andrija Paurevic
# Student Number: 1003995297
# Date: October 8, 2021
# Description:

import dataAcquisitionHelperFunctions as run

run.dataAcquisition.__init__()
run.dataAcquisition.prepareOscilloscope()
run.dataAcquisition.analyze()
results = run.dataAcquisition.returnResults()