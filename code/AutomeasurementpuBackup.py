#Import needed packages for the script to run
import numpy as np
import pandas as pd
import easymodbus.modbusClient
import time
from easybus import Easybus
from datetime import datetime
import matplotlib.pyplot as plt
import serial

#Function(s)
def readmodbus(address):
    register_output = tribox.read_holdingregisters(address, 2)
    convert_output = np.array([register_output[1], register_output[0]], np.uint16)
    convert_output.dtype = np.float32
    return convert_output

plt.rcParams['figure.dpi'] = 60

#Constants wel aanpassen
MaterialAdded = 'Streesss test'                	                    #Material added to water
meas_amount = 30                                                    #Enter the amount of samples you want
                                                                    #120 measurements takes 2 hours

#niet aanpassen
dateN = datetime.now()                                              #Retrieving time and seconds
dateNow = dateN.strftime("%d%m%Y")
Date = str(np.datetime64(dateNow))                                  #Day of measurement

N_measurements = 0                                                  #Index of first measurement
Data_only = False                                                   #If true the spectrum wil not be measured

#Create path to Excelfile
excel_path = 'C:/Users/Reactorkunde/Desktop/Excel/' + str(Date) + '_' + str(dateN.strftime("%H")) + '-' + str(dateN.strftime("%M")) + '-' + str(dateN.strftime("%S")) + '_' + MaterialAdded + '.xlsx'

#Connections to sensors
tribox = easymodbus.modbusClient.ModbusClient('192.168.1.55', 127)  #Initialise to Modbus via ethernet

pH = Easybus('COM4')                                                #Connect to pH sensor via USB
print("connected ph")
conduct = Easybus('COM3')                                           #Connect to conduct sensor via USB
print("connected conduct")

#Connect with tribox
tribox.connect()                                                    #Connect with Tribox
print("connected with tribox") 
#Test measurement and initialisation
tribox.write_single_coil(1,1)   
     
#Get wavelength from tribox for labels and x-axis data
tribox.unitidentifier = 2                                           #Connect to OPUS via SlaveID = 2
 
#Create array full of zeros to fill in with the absorption unit retrieved from the Tribox
spectrum = pd.DataFrame(0,range(meas_amount+1), range(203))
#tribox.unitidentifier = 5
#fluorspectrum = pd.DataFrame(0,range(meas_amount+1), range(203))

#Fill in the first 3 values that won't have to be retrieved from the Tribox
spectrum.rename(columns = {0:'Date [dd-mm-yy]',1:'Time [hh-mm-ss]',2:'Measurement [-]'}, inplace=True)
#flourspectrum.rename(columns = {0:'Date [dd-mm-yy]',1:'Time [hh-mm-ss]',2:'Measurement [-]'}, inplace=True)

#Retrieve values from Tribox for wavelength at which is the measurement has taken place
index = 3                                                           #First index that has to be filled in after date, time and measurement
for nm in np.linspace(2100, 2896, num=200):
    read = readmodbus(int(nm))
    exec('spectrum.rename(columns = {' + str(int(index)) + ': ' + str(read[0]) + '}, inplace = True)')
    index += 1

#index = 3                                                           #First index that has to be filled in after date, time and measurement
# for nm in np.linspace(2100, 2896, num=200):
#     read = readmodbus(int(nm))
#     exec('fluorspectrum.rename(columns = {' + str(int(index)) + ': ' + str(read[0]) + '}, inplace = True)')
#     index += 1

#Table titles for the Data sheet
table = pd.DataFrame(0,range(meas_amount+1), range(13))
table = table.astype('float32')
table.rename(columns = {0:'Date [dd-mm-yy]', 1:'Time [hh-mm-ss]', 2:'Measurement [-]', 3:'ABS210 [AU]', 4:'ABS254 [AU]', 5:'SAC254 [AU]', 6:'UVT254 [AU]', 7:'ABS360 [AU]', 8:'Turbidity [FNU]', 9:'Chloor [ppm]', 10:'Temperature [C]', 11:'Acidity [pH]', 12:'Conductivity [uS/cm]'}, inplace = True)
print("Wait time over")
#While loop retrieves data every minute from tribox and handheld sensors for meas_amount of times
while N_measurements <= meas_amount:
    timeN = datetime.now()                                          #Retrieving time and seconds
    timeNow = timeN.strftime("%H:%M:%S")
    timeSeconds = int(timeN.strftime("%S"))
    
    time.sleep(0.5)
    
    print("time is ", timeSeconds)
    
    if timeSeconds == 0:                                            #Checks if seconds are equal to zero
        #SlaveID tribox = 1, OPUS = 2, Turbidity = 3, Free Chlorine = 4, Microflu = 5
        tribox.unitidentifier = 1
        
        #Trigger measurement for all of the sensors connected to the Tribox
        tribox.write_single_coil(1,1)
        
        #Read values from OPUS sensor
        tribox.unitidentifier = 2
        ABS210 = readmodbus(1036)
        ABS254 = readmodbus(1042)
        SAC254 = readmodbus(1032)
        UVT254 = readmodbus(1062)
        ABS360 = readmodbus(1034)
        

        #Read values from turbidity sensor
        tribox.unitidentifier = 3
        FNU = readmodbus(1000)
        
        #Read values from free chlorine sensor
        tribox.unitidentifier = 4
        cl = readmodbus(1000)
        temp = readmodbus(1004)

        #Read values from microflu
        #tribox.unitidentifier = 5
        #  ABS210 = readmodbus(1036)        #aanpassen naar microflu spectrum
        # ABS254 = readmodbus(1042)
        # SAC254 = readmodbus(1032)
        # UVT254 = readmodbus(1062)
        # ABS360 = readmodbus(1034)

        #Read values from pH and Conductivity sensor. If the value can't be retrieved a zero will be added to the array instead
        print("read pH value")
        pHval = pH.value()
        print(pHval, "\n")

        print("read conduct value")
        conductval = conduct.value()
        print(conductval, "\n")
        
        #Fill array with data and stack with last loops data
        table.iloc[N_measurements,0] = Date
        table.iloc[N_measurements,1] = timeNow
        table.iloc[N_measurements,2] = N_measurements
        table.iloc[N_measurements,3] = ABS210[0]
        table.iloc[N_measurements,4] = ABS254[0]
        table.iloc[N_measurements,5] = SAC254[0]
        table.iloc[N_measurements,6] = UVT254[0]
        table.iloc[N_measurements,7] = ABS360[0]
        table.iloc[N_measurements,8] = FNU[0]
        table.iloc[N_measurements,9] = cl[0]
        table.iloc[N_measurements,10] = temp[0]
        table.iloc[N_measurements,11] = pHval
        table.iloc[N_measurements,12] = conductval
        #table.iloc[N_measurements,13] = #fluor afkortingen
        
        if Data_only == False:
            #Fill in date, time and measurement number
            spectrum.iloc[N_measurements,0] = Date
            spectrum.iloc[N_measurements,1] = timeNow
            spectrum.iloc[N_measurements,2] = N_measurements
                
            #Retrieve spectrum from OPUS
            tribox.unitidentifier = 2    
            
            #Retrieve absorption units for every wavelength and put in array
            index = 3
            for nm in np.linspace(2102, 2898, num=200):
                read = readmodbus(int(nm))
                spectrum.iloc[N_measurements,index] = float(read[0])
                index += 1
                 
            # index = 3
            # for nm in np.linspace(2102, 2898, num=200):
            #     read = readmodbus(int(nm))
            #     fluorspectrum.iloc[N_measurements,index] = float(read[0])
            #     index += 1     
        
        plist = ['p1','p2','p3','p4','p5','p6','p7','p8','p9','p10']  #'p11', 'p12' 'p13' ]     
        #een figuur aanmaken
        if N_measurements > 0:
            #Export table to sheet 1 and spectrum to sheet 2
            with pd.ExcelWriter(excel_path) as writer:
                table.to_excel(writer, sheet_name = 'Data', index = False, header = True)
                spectrum.to_excel(writer, sheet_name = 'Spectrum', index = False, header = True)
                #fluorspectrum.to_excel(writer, sheet_name = 'Fluorspectrum', index = False, header = True)
          
                

        #Keep track of amount of measurements done
        print("Meassure round: ", N_measurements)
        N_measurements += 1
        

#Remove first measurement from the matrices
table = table.drop(table.index[0])
spectrum = spectrum.drop(spectrum.index[0])
print("Out of loop")


#Close all ports
pH.close()
conduct.close()
tribox.close()
print("Program is done")
print("Creating plots")

fig = plt.figure(figsize=(6,10))
    
for p in plist:
    index = plist.index(p)
    exec(p + "= fig.add_subplot(5,2, index+1)")
    exec(p + ".plot(table.iloc[:N_measurements+1,2],table.iloc[:N_measurements+1,index+3])")
    exec(p + ".set_title(table.columns[index+3])")
plt.tight_layout()
plt.show()