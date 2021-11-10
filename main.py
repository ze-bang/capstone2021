# File: main.py
# Author: Andrija Paurevic
# Student Number: 1003995297
# Date: October 8, 2021
# Description:

# Import Modules
import dataAcquisitionHelperFunctions as run
from tqdm import tqdm

# Get parameters that the oscilloscope requires to run and collect data
trigParams, chanParams, timeParams, chanNumbers = run.setupOscilloscopeInput()

# Number of data points
numOfIterations = 1000

# Execute Functions
dataAcq = run.dataAcquisition()
dataAcq.prepareOscilloscope(triggerParameters=trigParams,channelParameters=chanParams,timeParameters=timeParams)
for i in tqdm(range(numOfIterations)):
    dataAcq.collectData(channels=chanNumbers)

# Plot data
dataAcq.plotData(plotParameters=None)