# File: main.py
# Author: Andrija Paurevic
# Student Number: 1003995297
# Date: October 8, 2021
# Description:

# Import Modules
import dataAcquisitionHelperFunctions as run
import tqdm

# Get parameters that the oscilloscope requires to run and collect data
trigParams, chanParams, timeParams = run.setupOscilloscopeInput()

# Number of data points
numOfIterations = 1000

# Execute Functions
run.dataAcquisition.__init__()
run.dataAcquisition.prepareOscilloscope(triggerParameters=trigParams,channelParameters=chanParams,timeParameters=timeParams)
for i in tqdm(range(numOfIterations)):
    run.dataAcquisition.collectData(channels=channelNumbers)

# Plot data
run.dataAcquisition.plotData(plotParameters=None)