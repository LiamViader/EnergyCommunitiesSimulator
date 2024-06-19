import pandas as pd
StartPath="DataOutputs/residential"
HourEndPath="HourStats.xlsx"
MinuteEndPath="MinuteStats.xlsx"
dfsHour=[pd.read_excel(StartPath+str(i)+HourEndPath) for i in range(1,7)] #llegeixo els arxius de consum horari dels 6 residencials
dfsMinute=[pd.read_excel(StartPath+str(i)+MinuteEndPath) for i in range(1,7)] #llegeixo els arxius de consum minut dels 6 residencials

#take only the base load mean and rename it
for i, df in enumerate(dfsHour):
    df=df[['local_hour','residential'+str(i+1)+'_baseProfileLoad_mean']].rename(columns={'residential'+str(i+1)+'_baseProfileLoad_mean': 'residential'+str(i+1)})
    dfsHour[i]=df

for i, df in enumerate(dfsMinute):
    df=df[['local_time','residential'+str(i+1)+'_baseProfileLoad_mean']].rename(columns={'residential'+str(i+1)+'_baseProfileLoad_mean': 'residential'+str(i+1)})
    dfsMinute[i]=df

#concat in the final df
dfBaseProfileLoadHour=pd.concat(dfsHour, axis=1)
dfBaseProfileLoadMinute=pd.concat(dfsMinute, axis=1)

#delete duplicate columns
dfBaseProfileLoadHour = dfBaseProfileLoadHour.loc[:, ~dfBaseProfileLoadHour.columns.duplicated()]
dfBaseProfileLoadMinute = dfBaseProfileLoadMinute.loc[:, ~dfBaseProfileLoadMinute.columns.duplicated()]

dfBaseProfileLoadHour.to_excel('Profiles/BaseProfilesHour.xlsx')
dfBaseProfileLoadMinute.to_excel('Profiles/BaseProfilesMinute.xlsx')