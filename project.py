#!/usr/bin/env python
# coding: utf-8

# In[209]:


# Description: Project
from sys import displayhook
import pandas as pd


# In[210]:


#read the data
df = pd.read_excel('data.xlsx')
df


# In[211]:


#convert the date column to datetime and drop the day
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].dt.strftime('%Y-%m')
df


# In[212]:


# get ending balance per customer per month
ending_balance = df.groupby(['Customer Id', 'Date']).agg('sum').reset_index()
ending_balance


# In[213]:


## loop through each customer id and get cumultive balance as seperate column with each transaction
df["cumultive_balance"] = df.groupby(['Customer Id'])['Amount'].cumsum()
df


# In[214]:


##get min balance per customer per month as seperate df
minBalance = df.groupby(['Customer Id', 'Date'])['cumultive_balance'].min().reset_index()
minBalance


# In[215]:


##get max balance per customer per month as seperate df
maxBalance = df.groupby(['Customer Id'])['cumultive_balance'].max().reset_index()
maxBalance


# In[216]:


## merge all the dataframes
df = pd.merge(ending_balance, minBalance, on=['Customer Id', 'Date'])
df = pd.merge(df, maxBalance, on=['Customer Id'])
df


# In[217]:


## rename columns
df = df.rename(columns={'Amount': 'EndingBalance', 'cumultive_balance_x': 'MinBalance', 'cumultive_balance_y': 'MaxBalance'})
df


# In[218]:


## change column order
df = df[['Customer Id', 'Date', 'MinBalance', 'MaxBalance', 'EndingBalance']]
displayhook(df)

## output df as csv
df.to_csv('output.csv')