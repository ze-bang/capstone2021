# File: dataAcquisitionHelperFunctions.py
# Author: Andrija Paurevic
# Student Number: 1003995297
# Date: October 8, 2021
# Description:

# Import modules
import pyvisa as visa
import sys, os, platform


def setupOscilloscopeInput():
    """"""

    # Channel numbers you wish to interact/collect data on
    channelNumbers = [3, 4]

    # Trigger inputs
    trigMode = "EGDE"
    trigSource = "WGEN2"
    if "WGEN" in trigSource:
        trigLevel = ""
    else:
        trigLevel = ""

    # Time inputs
    timeMode = "MAIN"
    timeScale = 1
    timeOffset = 0

    # Channel inputs
    chan3BWLimit = "ON"
    chan3Scale = 1
    chan3Offset = 1

    chan4BWLimit = "ON"
    chan4Scale = 1
    chan4Offset = 1

    chan3Params = [3, chan3Scale, chan3Offset, chan3BWLimit]
    chan4Params = [4, chan4Scale, chan4Offset, chan4BWLimit]

    # Set-up arrays needed for functions
    trigParams = [trigMode, trigSource, trigLevel]
    chanParams = [chan3Params, chan4Params]
    timeParams = [timeMode, timeScale, timeOffset]

    return trigParams, chanParams, timeParams

class dataAcquisition:

    def __init__(self):
        """"""
        if platform.system() == "Windows":
            os.add_dll_directory("C:\\Program Files\\Keysight\\IO Libraries Suite\\bin")
            self.rm = visa.ResourceManager("ktvisa32")
            self.infiniiVision = self.rm.open_resource("USB0::2391::6076::MY60101365::0::INSTR")
            self.infiniiVision.timeout = 50000
            self.debug = 0

        if platform.system() == "Darwin":
            self.rm = visa.ResourceManager("@py")
            self.infiniiVision = self.rm.open_resource("USB0::2391::6076::MY60101365::0::INSTR")
            self.infiniiVision.timeout = 50000
            self.debug = 0
        else:
            try:
                self.rm = visa.ResourceManager("@py")
                self.infiniiVision = self.rm.open_resource("USB0::2391::6076::MY60101365::0::INSTR")
                self.infiniiVision.timeout = 50000
                self.debug = 0
            except:
                print("Using an unfamiliar system, please figure out how to connect to the oscilloscope!")

        # Set-up results array to store data
        self.results = []

        # Set-up delay result
        self.delay = 0

    def doCommand(self, command, hideParams=False):
        """"""
        if hideParams:
            (header, data) = command.split(" ", 1)
            if self.debug:
                print("\nCmd = '%s'" % header)
        else:
            if self.debug:
                print("\nCmd = '%s'" % command)
        self.infiniiVision.write("%s" % command)
        if hideParams:
            self.checkInstrumentErrors(header)
        else:
            self.checkInstrumentErrors(command)

    def getQueryResult(self, query):
        if self.debug:
            print("Qys = '%s'" % query)
        result = self.infiniiVision.query("%s" % query)
        self.checkInstrumentErrors(query)
        return result

    def checkInstrumentErrors(self, command):
        """"""
        while True:
            errorString = self.infiniiVision.query(":SYSTem:ERRor?")
            if errorString:  # If there is an error string value.
                if errorString.find("+0,", 0, 3) == -1:  # Not "No error".
                    print("ERROR: %s, command: '%s'" % (errorString, command))
                    print("Exited because of error.")
                    sys.exit(1)
                else:  # "No error"
                    break
            else:  # :SYSTem:ERRor? should always return string.
                print("ERROR: :SYSTem:ERRor? returned nothing, command: '%s'" % command)
                print("Exited because of error.")
                sys.exit(1)

    def setTriggerParameters(self, triggerParameters=None):
        """
        Adjusts the trigger parameters remotely on the oscilloscope.

        :param triggerParameters: [type, source, trigger level (V)]
                                  e.g. ["EDGE", "WGEN2", ""] or ["EDGE","CHANnel 1", "1"]
        """

        try:
            self.doCommand(":TRIGger:MODE {}".format(triggerParameters[0]))

            if "WGEN" in triggerParameters[1]:
                self.doCommand(":TRIGger:EDGE:SOURce {}".format(triggerParameters[1]))
            else:
                self.doCommand(":TRIGger:EDGE:SOURce {}".format(triggerParameters[1]))
                self.doCommand(":TRIGger:EDGE:LEVel {}".format(triggerParameters[2]))
        except:
            print("Error adjusting the trigger parameters on the Oscilloscope.")

    def setChannelParameters(self, channelParameters):
        """
        Adjusts the channel parameters remotely on the oscilloscope.

        :param channelParameters: [[Channel Number (1,2,3,4), Vertical Scale (V), Offset (V), BWLimit (ON/OFF)], [], ...]
        """

        for channel in channelParameters:
            try:
                self.doCommand(":CHANnel{0}:SCALe {1}".format(channel[0],channel[1]))
                self.doCommand(":CHANnel{0}:OFFSet {1}".format(channel[0],channel[2]))
                self.doCommand(":CHANnel{0}:BWLimit {1}".format(channel[0],channel[3]))
            except:
                print("Error in setting channels for channel {}".format(channel[0]))

    def setTimeParameters(self, timeParameters):
        """
        Adjust the time parameters remotely on the oscilloscope

        :param timeParameters: [Mode, Horizontal Scale (ns), Position (ns)]
        """

        try:
            self.doCommand(":TIMebase:MODE {}".format(timeParameters[0]))
            self.doCommand(":TIMebase:SCALe {}E-9".format(timeParameters[1]))
            self.doCommand(":TIMebase:POSition {}E-9".format(timeParameters[2]))
        except:
            print("Error in adjusting the time parameters on the oscilloscope.")

    def digitizeChannels(self, channels):
        """
        Digitizes channels provided in order to prep them for signal measurement and data
        acquisition.

        :param channels: Array of channels that need digitizing
        """

        try:
            self.doCommand(":ACQuire:TYPE NORMal")

            for channel in channels:
                self.doCommand(":DIGitize CHANnel{}".format(channel))

        except:
            print("Error digitizing signals, please double check your code.")

    def measureSignals(self, channels):
        """"""
        try:
            query = ":MEASure:DELay CHANnel{0},CHANnel{1}".format(channels[0],channels[1])
            delay = self.getQueryResult(query)
            return delay
        except:
            print("Error in measuring the delay between the two channel signals.")

    def prepareOscilloscope(self, triggerParameters, channelParameters, timeParameters):
        """"""

        self.setTriggerParameters(triggerParameters)

        self.setChannelParameters(channelParameters)

        self.setTimeParameters(timeParameters)

    def collectData(self, channels):
        """"""

        self.digitizeChannels(channels)
        self.delay = self.measureSignals(channels)
        self.storeData(delay)

    def storeData(self, data):
        """"""
        self.results += [data]

    def plotData(self, plotParameters):
        """"""
