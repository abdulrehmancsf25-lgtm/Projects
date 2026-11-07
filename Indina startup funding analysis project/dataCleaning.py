import pandas as pd
import numpy as np 
df = pd.read_csv('C:/Users/Lenovo/Desktop/Python/Pandas/PandasCaseStudy/startup_funding.csv')

                         # DATA CLEANING AND PROCESSING 
df['Investors Name'] = df['Investors Name'].fillna('Undisclosed')

df.set_index('Sr No', inplace=True) # SET INDEX COLUMN TO Sr No
df.drop(columns='Remarks' , inplace=True) # Dropping Remarks column 
df['Date dd/mm/yyyy'] = pd.to_datetime(df['Date dd/mm/yyyy'] , dayfirst=True , errors='coerce') # to date format
df.rename(columns={
       'Date dd/mm/yyyy' : 'date' ,
        'Startup Name' : 'startup' , 
        'Industry Vertical' : 'vertical' ,
          'SubVertical' : 'sub vertical' ,
            'City  Location' :  'city' ,
             'Investors Name' : 'investors' ,
             'InvestmentnType' : 'round' ,
             'Amount in USD' : 'amount(Cr)'
} , inplace=True)  # Changing column names for ease 

df['amount(Cr)'] =  df['amount(Cr)'].fillna('0')
def cleanAmount(text):
    text = text.strip() 
    text = "".join(text.split(',')) # join values to make one single
    if text.isalpha():
        text = '0'   # for undisclosed investments 
    if not text.isnumeric()  and not '.' in text:   # random text not valid amount 
        text = '0'    
    return text



df ['amount(Cr)']= df['amount(Cr)'].apply(cleanAmount)
df['amount(Cr)'] = df['amount(Cr)'].astype(float)

# now converting to crore 
df['amount(Cr)'] = (df['amount(Cr)'] * 95.12) / 10000000

df['investors'] = df['investors'].fillna('Unkown') # to avoid more removal of data
df = df.dropna(subset=['date'  ,'vertical' ,'city','round'])

df['city'] = df['city'].astype('category') # total cities in dataset -> 110

df.to_csv('cleaned_data.csv' , index=False)