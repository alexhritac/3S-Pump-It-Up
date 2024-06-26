#Import needed packages for the script to run
import numpy as np
import pandas as pd
import easymodbus.modbusClient
import time
from easybus import Easybus
from datetime import datetime
import matplotlib.pyplot as plt
import serial
import warnings
import mysql.connector
import datetime
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine
pd.options.mode.chained_assignment = None  # default='warn' ---don't care about writes making it back to the original frame ---line spectrum_row.loc['Time [hh-mm-ss]'] = now.strftime('%Y-%m-%d %H:%M:%S')
warnings.simplefilter(action='ignore', category=FutureWarning)


#Constants wel aanpassen
MaterialAdded = '26_May'                	                   #Material added to water
meas_amount = 1000                                                #Enter the amount of samples you want 120 measurements takes aprox. 2 hours

#file location  !BE SURE! to use the / (backslash) and not the (\) frontslash
File_location_excel = 'C:/Users/Reactorkunde/Desktop/Excel/'        #The excel file will be saved in this folder       
File_Location_plots = 'C:/Users/Reactorkunde/Desktop/Plots/'        #the picture of the graph will be saved in this folder                                                            
        


#Function(s)
def readmodbus(address):
    register_output = tribox.read_holdingregisters(address, 2)
    convert_output = np.array([register_output[1], register_output[0]], np.uint16)
    convert_output.dtype = np.float32
    return convert_output

plt.rcParams['figure.dpi'] = 60



#niet aanpassen
dateN = datetime.now()                                              #Retrieving time and seconds
dateNow = dateN.strftime("%d%m%Y")
Date = str(np.datetime64(dateNow))                                  #Day of measurement
N_measurements = 0                                                  #Index of first measurement
Data_only = False                                                   #If true the spectrum wil not be measured

#Create path to Excelfile
excel_path = File_location_excel + str(Date) + '_' + str(dateN.strftime("%H")) + '-' + str(dateN.strftime("%M")) + '-' + str(dateN.strftime("%S")) + '_' + MaterialAdded + '.xlsx'

#Create path to Plots
plot_path = File_Location_plots + str(Date) + '_' + str(dateN.strftime("%H")) + '-' + str(dateN.strftime("%M")) + '-' + str(dateN.strftime("%S")) + '_' + MaterialAdded + '.png'

#Connections to sensors
tribox = easymodbus.modbusClient.ModbusClient('192.168.1.54', 127)  #Initialise to Modbus via ethernet

#COM porten (pH en conductivity)
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
#UV spec
spectrum = pd.DataFrame(0,range(meas_amount+1), range(203))
#Fill in the first 3 values that won't have to be retrieved from the Tribox
spectrum.rename(columns = {0:'Date [dd-mm-yy]',1:'Time [hh-mm-ss]',2:'Measurement [-]'}, inplace=True)






#Retrieve values from Tribox for wavelength at which is the measurement has taken place
#uv Read
tribox.unitidentifier = 2
uvindex = 3                                                           #First index that has to be filled in after date, time and measurement
for nm in np.linspace(2100, 2896, num=200):
    read = readmodbus(int(nm))
    
    exec('spectrum.rename(columns = {' + str(int(uvindex)) + ': ' + str(read[0]) + '}, inplace = True)')
    uvindex += 1

#Table titles for the Data sheet
table = pd.DataFrame(0,range(meas_amount+1), range(16))
table = table.astype('float32')
table.rename(columns = {0:'Date [dd-mm-yy]', 1:'Time [hh-mm-ss]', 2:'Measurement [-]', 3:'ABS210 [AU]', 4:'ABS254 [AU]', 5:'SAC254 [AU]', 6:'UVT254 [AU]', 7:'ABS360 [AU]', 8:'Turbidity [FNU]', 9:'Acidity [pH]', 10:'Conductivity [uS/cm]', 11:'TRP[ug/l]', 12:'BODeq', 13:'CODeq', 14:'NO2', 15:'NO3'}, inplace = True)

#While loop retrieves data every minute from tribox and handheld sensors for meas_amount of times
while N_measurements <= meas_amount:
    timeN = datetime.now()                                          #Retrieving time and seconds
    timeNow = timeN.strftime("%H:%M:%S")
    timeSeconds = int(timeN.strftime("%S"))
    if timeSeconds == 0:                                            #Checks if seconds are equal to zero
        #Keep track of amount of measurements done
        print(timeNow, "Meassure round: ", N_measurements)

        #SlaveID tribox = 1, OPUS = 2, Turbidity = 3, Free Chlorine = 4, Microflu = 5
        tribox.unitidentifier = 1
        
        #Trigger measurement for all of the sensors connected to the Tribox
        tribox.write_single_coil(1,1)
        
        #Read values from OPUS sensor
        tribox.unitidentifier = 2
        ABS210 = readmodbus(1036)
        if np.isnan(ABS210[0]) : ABS210[0] = 0

        ABS254 = readmodbus(1042)
        if np.isnan(ABS254[0]) : ABS254[0] = 0

        SAC254 = readmodbus(1032)
        if np.isnan(SAC254[0]) : SAC254[0] = 0

        UVT254 = readmodbus(1062)
        if np.isnan(UVT254[0]) : UVT254[0] = 0

        ABS360 = readmodbus(1034)
        if np.isnan(ABS360[0]) : ABS360[0] = 0

        BODeq = readmodbus(1006)
        if np.isnan(BODeq[0]) : BODeq[0] = 0

        CODeq = readmodbus(1004)
        if np.isnan(CODeq[0]) : CODeq[0] = 0

        NO2 = readmodbus(1048)
        if np.isnan(NO2[0]) : NO2[0] = 0

        NO3 = readmodbus(1046)
        if np.isnan(NO3[0]) : NO3[0] = 0
        
        #Read values from turbidity sensor
        tribox.unitidentifier = 3
        FNU = readmodbus(1000)
        if np.isnan(FNU[0]) : FNU[0] = 0
        #Read values from free chlorine sensor
        #tribox.unitidentifier = 4
        #cl = readmodbus(1000)
        #temp = readmodbus(1004)

        #Read values from microflu
        tribox.unitidentifier = 5
        TRP = readmodbus(1000)          #aanpassen naar microflu spectrum
        if np.isnan(TRP[0]) : TRP[0] = 0
        
        #new sensor can be added here
            #tribox.unitidentifier is modbus address found in the settings menu of each sensor
            # the adress the number in between brackets of readmodbus() can be found in the chatbox of the sensor in the tribox
        #tribox.unitidentifier = number
        #nieuweSensorafkoring = readmodbus(adress)



        #Read values from pH and Conductivity sensor. If the value can't be retrieved a zero will be added to the array instead
        pHval = pH.value()
        print("pH Value: ", pHval)

        conductval = conduct.value()
        print("conductval: ", conductval)
        
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
        table.iloc[N_measurements,9] = pHval
        table.iloc[N_measurements,10] = conductval
        table.iloc[N_measurements,11] = TRP[0]
        table.iloc[N_measurements,12] = BODeq[0]
        table.iloc[N_measurements,13] = CODeq[0]
        table.iloc[N_measurements,14] = NO2[0]
        table.iloc[N_measurements,15] = NO3[0]
        #table.iloc[N_measurements,9] = cl[0]
        #table.iloc[N_measurements,10] = temp[0]
        #new sensor can be added here
        #table.iloc[N_measurements,(nextnumber)] = nieuweSensorAfkoring[0]
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="PumpItUp3S",
        database="pumpitup"
        ) 
        mycursor = mydb.cursor()
        now = datetime.now()
        #print(float(ABS210[0]),float(ABS254[0]),float(SAC254[0]),float(UVT254[0]),float(ABS360[0]),float(FNU[0]),pHval,conductval,float(TRP[0]),float(BODeq[0]),float(CODeq[0]),float(NO2[0]),float(NO3[0]))
        sql = "INSERT INTO sensors (date,abs210,abs254,sac254,uvt254,abs360,turbidity,acidity,conductivity,trp,bod,cod,no2,no3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (now.strftime('%Y-%m-%d %H:%M:%S'),float(ABS210[0]),float(ABS254[0]),float(SAC254[0]),float(UVT254[0]),float(ABS360[0]),float(FNU[0]),pHval,conductval,float(TRP[0]),float(BODeq[0]),float(CODeq[0]),float(NO2[0]),float(NO3[0]))
        mycursor.execute(sql, val) 

        mydb.commit()
        mycursor.close()
        
        print(mycursor.rowcount, "record inserted.")

        if Data_only == False:
            #Fill in date, time and measurement number
            spectrum.iloc[N_measurements,0] = Date
            spectrum.iloc[N_measurements,1] = timeNow
            spectrum.iloc[N_measurements,2] = N_measurements
                
            #Retrieve uv spectrum from OPUS
            tribox.unitidentifier = 2    
            
            #Retrieve absorption units for every wavelength and put in array
            index = 3
            for nm in np.linspace(2102, 2898, num=200):
                read = readmodbus(int(nm))
                spectrum.iloc[N_measurements,index] = float(read[0])
                index += 1

        
        sql_engine = create_engine('mysql+mysqlconnector://root:PumpItUp3S@localhost:3306/pumpitup')
        conn = sql_engine
        spectrum_row = spectrum.loc[N_measurements]
        spectrum_row.loc['Time [hh-mm-ss]'] = now.strftime('%Y-%m-%d %H:%M:%S')
        spectrum_row_df = pd.DataFrame(spectrum_row).transpose()
        spectrum_row_df.infer_objects().to_sql(name='spectrum', con=conn, if_exists='append', index=False)
        mydb.close()
        print("record inserted.")
        

        #Here will a simple figure be made
        plist = ['p1','p2','p3','p4','p5','p6','p7','p8','p9','p10','p11','p12','p13']  #'p11', 'p12' 'p13' ]     
        #een figuur aanmaken
        if N_measurements > 0:
            #Export table to sheet 1 and spectrum to sheet 2
            with pd.ExcelWriter(excel_path) as writer:
                table.to_excel(writer, sheet_name = 'Data', index = False, header = True)
                spectrum.to_excel(writer, sheet_name = 'Spectrum', index = False, header = True)
                #fluorspectrum.to_excel(writer, sheet_name = 'Fluorspectrum', index = False, header = True)
          
                
        #Increase N_measurements with 1
        N_measurements += 1
        
    #end of measurement loop
    
#Remove first measurement from the matrices
table = table.drop(table.index[0])
spectrum = spectrum.drop(spectrum.index[0])
print("Out of loop")


#Close all ports
pH.close()
conduct.close()
tribox.close()
print("Creating plots")

fig = plt.figure(figsize=(8,15))
    
for p in plist:
    index = plist.index(p)
    exec(p + "= fig.add_subplot(7,2, index+1)")
    exec(p + ".plot(table.iloc[:N_measurements+1,2],table.iloc[:N_measurements+1,index+3])")
    exec(p + ".set_title(table.columns[index+3])")
plt.tight_layout()
plt.savefig(plot_path)

print("Program is done")
