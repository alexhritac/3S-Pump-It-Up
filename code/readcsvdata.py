#Import libraries needed for running the code
import pandas as pd
import numpy as np

#Names of the files that need EventLab data added to them
paths = ['2022-10-14_14-13-00_NaCl']

#Loop to add the EventLab data to all files in paths
for path in paths:
    
    #Path to Excel-file and csv-file
    EventData = pd.read_csv(path + '.csv')
    excel_path = path + '.xlsx'
    
    #Import data from Excelsheets
    excel_data = pd.read_excel(excel_path, sheet_name = 'Data')
    excel_spectrum = pd.read_excel(excel_path, sheet_name = 'Spectrum')
    
    #Initialise columns for the response and temperature values from the csv-file
    response = pd.DataFrame(0, index=range(121), columns = range(1))
    temp = pd.DataFrame(0, index=range(121), columns = range(1))
    
    #Retrieve the minute of the first measurement
    time_data = EventData.iloc[0,1]
    minutes = int(time_data[14:16])
    
    response.iloc[0,0] = EventData.iloc[1,10]
    temp.iloc[0,0] = EventData.iloc[1,13]
    
    index = 1
    
    #Fill recently initialised columns with data from the csv-file
    for n in range(len(EventData)):
        time_data = EventData.iloc[n,1]
        
        time_data = int(time_data[14:16])
        
        if minutes == 60:
            minutes = 0
        
        if time_data == minutes:
            response.iloc[index,0] = EventData.iloc[n,10]
            temp.iloc[index,0] = EventData.iloc[n,13]
            minutes += 1
            index += 1
        
        if index == 121:
            break
    
    #Drop the Chloor[ppm] column
    response.drop(index = 0, inplace = True)
    response.reset_index(inplace = True,drop = True)
    excel_data['Chloor [ppm]'] = response[0]
    excel_data = excel_data.rename(columns = {'Chloor [ppm]':'Response'})
    #Drop the Temperature[C]] column
    temp.drop(index = 0, inplace = True)
    temp.reset_index(inplace = True, drop = True)
    excel_data['Temperature [C]'] = temp[0]
    
    #Scan all spectrumdata for NaNs or Infs. When there is one of both, the script will fill it automatically so a graph can be made later.
    for k in np.linspace(3,202,202,dtype=int):
        for n in np.linspace(1,119,119,dtype=int):
            if np.isnan(excel_spectrum.iloc[n,k]) == False and np.isinf(excel_spectrum.iloc[n,k]) == False:
                save_value = excel_spectrum.iloc[n,k]
            
            if np.isnan(excel_spectrum.iloc[n,k]) == True or np.isinf(excel_spectrum.iloc[n,k]) == True:
                if n != 119:
                    excel_spectrum.iloc[n,k] = (excel_spectrum.iloc[n-1,k] + excel_spectrum.iloc[n+1,k])*0.5
                else:
                    excel_spectrum.iloc[n,k] = excel_spectrum.iloc[n-1,k]
            
            if np.isnan(excel_spectrum.iloc[n,k]) == True or np.isinf(excel_spectrum.iloc[n,k]) == True:
                excel_spectrum.iloc[n,k] = save_value
    
    for k in range(len(excel_data)):
        if np.isnan(excel_data.iloc[k,3]) == True or np.isinf(excel_data.iloc[k,3]):
            excel_data.iloc[k,3] = excel_spectrum.iloc[k,17]
    
    #Export the Excelfile to the same file it was in before
    with pd.ExcelWriter(excel_path) as writer:
        excel_data.to_excel(writer, sheet_name = 'Data', index = False)
        excel_spectrum.to_excel(writer, sheet_name = 'Spectrum', index = False)
