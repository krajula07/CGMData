import pandas as pd
import numpy as np

def secondsPerDay(tme):
    hours, minutes, seconds = tme.split(':')
    return (int(hours)*60*60)+(int(minutes)*60)+int(seconds)

def checkTime(tme, tmeRange):
    return secondsPerDay(tmeRange[0]) < secondsPerDay(tme) <= secondsPerDay(tmeRange[1])
print(checkTime('06:00:00',('00:00:00', '6:00:00') ))
print(checkTime('23:59:59',('06:00:00', '23:59:59')))
CGM_data_file='CGMData.csv'
CGM_data = pd.read_csv(CGM_data_file,low_memory=False)
print(CGM_data['Time'].count())
#CGM_Date_data = pd.read_csv(CGM_data_file,low_memory=False,parse_dates=[['Date', 'Time']])
CGM_data['Sensor Glucose (mg/dL)'].interpolate(method='linear', inplace=True, direction = 'both')
#print(CGM_data.head(10))


CGM_data['Count']=CGM_data.groupby('Date')['Time'].transform('count')
drop_count=CGM_data[( CGM_data['Count']>288)|( CGM_data['Count']<270)]
print(drop_count['Time'].count())
rows=CGM_data[( CGM_data['Count']>288)|( CGM_data['Count']<270)].index
CGM_data.drop(rows,inplace=True)


Insulin_Data_File='InsulinData.csv'
Insulin_data = pd.read_csv(Insulin_Data_File,low_memory=False)
rows =Insulin_data[(Insulin_data['Alarm']=='AUTO MODE ACTIVE PLGM OFF')]
AutoModeOn=rows.tail(1)
#print(AutoModeOn['Date'],AutoModeOn['Time'])
#print((AutoModeOn['Time'].values)>'8:06:13')
Compared_rows=CGM_data[((CGM_data['Date'].values)==(AutoModeOn['Date'].values)) & ((CGM_data['Time'].values)>=(AutoModeOn['Time'].values))  ]
Compared_row=Compared_rows.tail(1)
AutoMode_Rows=CGM_data[(CGM_data['Index'].values)<(Compared_row['Index'].values)]
ManualMode_Rows=CGM_data[(CGM_data['Index'].values)>(Compared_row['Index'].values)]
print(AutoMode_Rows['Time'].count())
print(ManualMode_Rows['Time'].count())
Days_data = AutoMode_Rows.groupby('Date')

count=0
count1=0
metrics=[0]*18
for day_grp in Days_data:
    df_temp = AutoMode_Rows.loc[AutoMode_Rows['Date'] == day_grp[0]]
#    print(df_temp['Time'].values,df_temp['Sensor Glucose (mg/dL)'].values)
    #print(df_temp['Time']<'6:00:00')
    m=[0]*18
    for index, day in df_temp.iterrows():

        if(checkTime(day['Time'], ('00:00:00', '6:00:00'))):
            print(f"overnight= {day['Time']}")
            if(day['Sensor Glucose (mg/dL)']>180):
                m[0]+=1
            if(day['Sensor Glucose (mg/dL)']>250):
                m[1]+=1
            if((day['Sensor Glucose (mg/dL)']>=70) & (day['Sensor Glucose (mg/dL)']<=180)):
                m[2]+=1
            if((day['Sensor Glucose (mg/dL)']>=70) & (day['Sensor Glucose (mg/dL)']<=150)):
                m[3]+=1
            if(day['Sensor Glucose (mg/dL)']<70):
                m[4]+=1
            if(day['Sensor Glucose (mg/dL)']<54):
                m[5]+=1
        if(checkTime(day['Time'], ('05:59:59', '23:59:59'))):
            print(f"daytime= {day['Time']}")
            if(day['Sensor Glucose (mg/dL)']>180):
                m[6]+=1
            if(day['Sensor Glucose (mg/dL)']>250):
                m[7]+=1
            if((day['Sensor Glucose (mg/dL)']>=70) & (day['Sensor Glucose (mg/dL)']<=180)):
                m[8]+=1
            if((day['Sensor Glucose (mg/dL)']>=70) & (day['Sensor Glucose (mg/dL)']<=150)):
                m[9]+=1
            if(day['Sensor Glucose (mg/dL)']<70):
                m[10]+=1
            if(day['Sensor Glucose (mg/dL)']<54):
                m[11]+=1
        if(checkTime(day['Time'], ('00:00:00', '23:59:59'))):
            print(f"wholeday = {day['Time']}")
            if(day['Sensor Glucose (mg/dL)']>180):
                m[12]+=1
            if(day['Sensor Glucose (mg/dL)']>250):
                m[13]+=1
            if((day['Sensor Glucose (mg/dL)']>=70) & (day['Sensor Glucose (mg/dL)']<=180)):
                m[14]+=1
            if((day['Sensor Glucose (mg/dL)']>=70) & (day['Sensor Glucose (mg/dL)']<=150)):
                m[15]+=1
            if(day['Sensor Glucose (mg/dL)']<70):
                m[16]+=1
            if(day['Sensor Glucose (mg/dL)']<54):
                m[17]+=1
    metrics[0]+=m[0]
    metrics[1]+=m[1]
    metrics[2]+=m[2]
    metrics[3]+=m[3]
    metrics[4]+=m[4]
    metrics[5]+=m[5]
    metrics[6]+=m[6]
    metrics[7]+=m[7]
    metrics[8]+=m[8]
    metrics[9]+=m[9]
    metrics[10]+=m[10]
    metrics[11]+=m[11]
    metrics[12]+=m[12]
    metrics[13]+=m[13]
    metrics[14]+=m[14]
    metrics[15]+=m[15]
    metrics[16]+=m[16]
    metrics[17]+=m[17]
for i in range(len(metrics)):

    metrics[i]=((metrics[i])/(288*len(Days_data)))*100
    count+=metrics[i]


ManualDays_data = ManualMode_Rows.groupby('Date')

Manualmetrics=[0]*18
#print(len(ManualDays_data))
for day_grp in ManualDays_data:
    df_temp = ManualMode_Rows.loc[ManualMode_Rows['Date'] == day_grp[0]]
    m=[0]*18
#    print(df_temp['Time'].values,df_temp['Sensor Glucose (mg/dL)'].values)
    #print(df_temp['Time']<'6:00:00')

    for index, day in df_temp.iterrows():

        if(checkTime(day['Time'], ('00:00:00', '6:00:00'))):
            if(day['Sensor Glucose (mg/dL)']>180):
                m[0]+=1
            if(day['Sensor Glucose (mg/dL)']>250):
                m[1]+=1
            if((day['Sensor Glucose (mg/dL)']>=70) & (day['Sensor Glucose (mg/dL)']<=180)):
                m[2]+=1
            if((day['Sensor Glucose (mg/dL)']>=70) & (day['Sensor Glucose (mg/dL)']<=150)):
                m[3]+=1
            if(day['Sensor Glucose (mg/dL)']<70):
                m[4]+=1
            if(day['Sensor Glucose (mg/dL)']<54):
                m[5]+=1
        if(checkTime(day['Time'], ('05:59:59', '23:59:59'))):
            if(day['Sensor Glucose (mg/dL)']>180):
                m[6]+=1
            if(day['Sensor Glucose (mg/dL)']>250):
                m[7]+=1
            if((day['Sensor Glucose (mg/dL)']>=70) & (day['Sensor Glucose (mg/dL)']<=180)):
                m[8]+=1
            if((day['Sensor Glucose (mg/dL)']>=70) & (day['Sensor Glucose (mg/dL)']<=150)):
                m[9]+=1
            if(day['Sensor Glucose (mg/dL)']<70):
                m[10]+=1
            if(day['Sensor Glucose (mg/dL)']<54):
                m[11]+=1
        if(checkTime(day['Time'], ('00:00:00', '23:59:59'))):
            if(day['Sensor Glucose (mg/dL)']>180):
                m[12]+=1
            if(day['Sensor Glucose (mg/dL)']>250):
                m[13]+=1
            if((day['Sensor Glucose (mg/dL)']>=70) & (day['Sensor Glucose (mg/dL)']<=180)):
                m[14]+=1
            if((day['Sensor Glucose (mg/dL)']>=70) & (day['Sensor Glucose (mg/dL)']<=150)):
                m[15]+=1
            if(day['Sensor Glucose (mg/dL)']<70):
                m[16]+=1
            if(day['Sensor Glucose (mg/dL)']<54):
                m[17]+=1
        #print(day['Time'],m[0],m[1],m[2],m[3],m[4],m[5],m[6],m[7],m[8],m[9],m[10],m[11],m[12],m[13],m[14],m[15],m[16],m[17])
    Manualmetrics[0]+=m[0]
    Manualmetrics[1]+=m[1]
    Manualmetrics[2]+=m[2]
    Manualmetrics[3]+=m[3]
    Manualmetrics[4]+=m[4]
    Manualmetrics[5]+=m[5]
    Manualmetrics[6]+=m[6]
    Manualmetrics[7]+=m[7]
    Manualmetrics[8]+=m[8]
    Manualmetrics[9]+=m[9]
    Manualmetrics[10]+=m[10]
    Manualmetrics[11]+=m[11]
    Manualmetrics[12]+=m[12]
    Manualmetrics[13]+=m[13]
    Manualmetrics[14]+=m[14]
    Manualmetrics[15]+=m[15]
    Manualmetrics[16]+=m[16]
    Manualmetrics[17]+=m[17]
    #print(Manualmetrics[0],Manualmetrics[6],Manualmetrics[11])

for i in range(len(Manualmetrics)):
    Manualmetrics[i]=((Manualmetrics[i])/(288*len(ManualDays_data)))*100
metrics_df=pd.DataFrame(metrics)
metrics_df1=metrics_df.transpose()
Manualmetrics_df=pd.DataFrame(Manualmetrics)
Manualmetrics_df1=Manualmetrics_df.transpose()
final=pd.concat([Manualmetrics_df1,metrics_df1])
#print(final)
final.to_csv('Results1.csv',mode='a', header=None,index=False)
#Manualmetrics_df1.to_csv('metrics1.csv')
print(metrics)
print(Manualmetrics)