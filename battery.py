'''
@namespace battery
Class libarary to communicate with the Inspired Engergies Lithium-Ion
batteries with smbus.

Library written using this document 
http://inspiredenergy.com/Standard_Products/NH2054/NH2054HD24%20spec%20v3.1.pdf

@author miannucci
April 214
'''
import smbus

class Battery:

    def __init__(self, address, nBus):
        '''Defualt class constructor

        @param address The i2c address of the batteries
        @param nBus The i2c bus number to operate on

        @return new Battery object

        '''
        self.bus = smbus.SMBus(nBus)  # Create the smbus interface
        self.busAddr = address  # Cast the device adress into class scope

    def WriteWord(self, comm, word):
        '''Writes a word to the smbus port according to the battery 
        protocol.

        @param word The word to write to the port

        '''
        self.bus.write_byte_data(self.busAddr, comm, word)

    def ReadWord(self, comm):
        '''Reads a word from the smbus port according to the battery
        protocol.

        @param comm The command to send to init the read

        @return The word written from the interface

        '''
        data = self.bus.read_byte_data(self.busAddr, comm)
        msb = data[1]
        lsb = data[0]
        return ((msb << 8) | (lsb >> 4))


    def BlockRead(self, comm, nBytes):
        '''Reads a maximum of 32 bytes from the battery interface

        @param comm The command to send to the slave (battery)
        @param nbytes The number of bytes to read in the BlockRead

        @return the data that has been read. 

        '''
        data = self.bus.read_block_data(self.busAddr, comm, nBytes)
        msb = data[1]
        lsb = data[0]
        return ((msb << 8) | (lsb >> 4))

    def AtRateTimeToFull(self):
        '''Returns the predicted remaining time to fully charge the 
        battery at the AtRate() value. 

        @return Time remaining to finish charging in minutes

        '''
        return self.ReadWord(0x05)

    def AtRateTimeToEmpty(self):
        '''Returns the predicted remaining operating time if the battery 
        is discharged at the AtRate() value.

        @return Predicted remaining operating time in minutes

        '''
        return self.ReadWord(0x06)

    def Temperature(self):
        '''Returns the pack's internal Temperature

        @return Temperature of the battery pack in 0.1 degrees K

        '''
        return self.ReadWord(0x08)

    def Voltage(self):
        '''Returns the battery's voltage (measured at the cell stack)

        @return Volatge of the battery in mV

        '''
        return self.ReadWord(0x09)

    def Current(self):
        '''Returns the current being supplied (or accepted) through the 
        battery’s terminals.

        @return The current through the terminals in mA 

        '''
        return self.ReadWord(0x0a)

    def AverageCurrent(self):
        '''Returns a rolling average based upon the last 64 samples of 
        current. 

        @return The average current in mA 

        '''
        return self.ReadWord(0x0b)

    def MaxError(self):
        '''Returns the expected margin of error 

        @return The expected error in percentage

        '''
        return self.ReadWord(0x0c)

    def RelativeStateOfCharge(self):
        '''Returns the predicted remaining battery capacity expressed 
        as a percentage of FullChargeCapacity(). 

        @return Predicted remaining battery capacity in percentage

        '''
        return self.ReadWord(0x0d)

    def AbsoluteStateOfCharge(self):
        '''Returns the predicted remaining battery capacity expressed 
        as a percentage of DesignCapacity().

        @return The predicted remaining battery capacity in percentage

        '''
        return self.ReadWord(0x0e)

    def RemainingCapacity(self):
        '''Returns the predicted remaining battery capacity.

        @return The predicted remaining battery capacity in mAh

        '''
        return self.ReadWord(0x0f)

    def FullChargeCapacity(self):
        '''Returns the predicted battery capacity when fully charged

        @return The predicted battery capacity at full charge in mAh

        '''
        self.ReadWord()(0x10)

    def RunTimeToEmpty(self):
        '''Returns the predicted remaining battery life at the present
        discharge rate.

        @return The predicted remaining battery life at the 
        present dicharge rate in minutes

        '''
        self.ReadWord()(0x11)

    def AverageTimeToEmpty(self):
        '''Returns the rolling average of the predicted remaining battery 
        life. 

        @return The average remaining battery life in minutes

        '''
        self.ReadWord(0x12)

    def AverageTimeToFull(self):
        '''Returns the rolling average of the predicted remaining time 
        until the battery reaches full charge. 

        @return The average predicted time until the battery reaches full 
        charge in minutes

        '''
        self.ReadWord()(0x13)

    def ChargingCurrent(self):
        '''Returns the battery's desired charging rate 

        @return The battery's desired charging rate in mA

        '''
        self.ReadWord(0x14)

    def ChargingVoltage(self):
        '''Returns the battery's desired charging voltage

        @return The battery's desired charging voltage in mV

        '''
        self.ReadWord(0x15)

    def BatteryStatus(self):
        '''Returns the battery's status word 

        @return Bit Flags with the battery's status word.

        '''
        self.ReadWord(0x16)

    def CycleCount(self):
        '''Returns the number of charge/discharge cycles the battery 
        has experienced. A charge/discharge cycle is defined as: an 
        amount of discharge approximately equal to the value of 
        DesignCapacity.

        @return The number of charge/discharge cycles the battery has 
        experienced 

        '''
        self.ReadWord(0x17)

    def DesignCapacity(self):
        '''The theoretical capacity of a new battery 

        @return The theoretical capacity of the new battery in mAh

        '''
        self.ReadWord(0x18)

    def DesignVoltage(self):
        '''Returns the theoretical voltage of a new battery 

        @return The theoretical voltage of a new battery in mV

        '''
        self.ReadWord(0x19)

    def SerialNumber(self):
        '''Returns the battery's serial number

        @return The serial number of the battery 

        '''
        self.ReadWord(0x1c)