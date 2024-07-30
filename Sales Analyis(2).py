#!/usr/bin/env python
# coding: utf-8

#                             SALES DATA ANALYSIS

# ![image.png](attachment:image.png)

# Introduction
# 
# Sales play an esesntial role of generating income for businesses. As such, it is important for businesses to understand sales data for proper planning.
# Through EDA, this project will examine a data sample on https://www.kaggle.com/datasets to uncover insights that could help boost profits and aid decision making.
# 

# import the necessary libraries

# In[54]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')
#importing the necessary libraries


# Data processing and cleaning

# In[55]:


df=pd.read_csv(r'C:\Users\ADMIN\Documents\sales_data_sample.csv')
#loading the dataset


# In[56]:


df.head(5)


# In[57]:


df.shape


# In[58]:


df.info()


# the columns ADDRESSLINE2,STATE,POSTALCODE and TERRITORY have missing data.

# In[59]:


df.columns
# displaying names of columns in the dataset


# In[60]:


df.describe()
#count,mean, median, max, min and quartiles of the numerical columns.


# In[61]:


df.duplicated().sum()
#there are no duplicated values in the dataset.


# In[62]:


#dropping irrelevant columns
df.drop(['ORDERNUMBER', 'PRICEEACH', 'ORDERLINENUMBER', 'STATUS', 'QTR_ID', 'PRODUCTCODE', 'PHONE', 'ADDRESSLINE2', 'STATE', 'POSTALCODE', 'TERRITORY', 'CONTACTLASTNAME', 'CONTACTFIRSTNAME'], axis=1, inplace=True)


# In[63]:


df.shape


# In[64]:


df.isnull().sum()
#the dataset have no missing values now that i dropped the columns that had missing values


# Data Analysis and Visualization

# In[65]:


df.head(5)


# Year with the highest sales

# In[66]:


df1=df.groupby('YEAR_ID')['SALES'].sum().reset_index()
df1


# In[67]:


sns.barplot(data=df1, x='YEAR_ID', y='SALES')
           
plt.title('Sales volume by Year')

plt.show()
# out of the three years, 2004 had the highest sales volume.


# Month with the highest sales

# In[68]:


df2=df.groupby('MONTH_ID')['SALES'].sum().reset_index()
df2
#November had the highest sales volume


# In[69]:


sns.barplot(data=df2, x='MONTH_ID', y='SALES')
plt.title('Sales by Month')
plt.show()


# In[70]:


#creating subplots for each year

unique_months=df['MONTH_ID'].unique()
temp=pd.DataFrame()
for i, month in enumerate(unique_months):
    month_data= df[df['MONTH_ID']== month]
    month_data= month_data.groupby('YEAR_ID')['SALES'].sum().reset_index()
    month_data['MONTH_ID']=month
    temp= pd.concat([temp, month_data], ignore_index=True)
plt.figure(figsize=(20, 8))
plt.title('Month Revenue by Year')
a=sns.barplot(data=temp, x= 'MONTH_ID', y='SALES', hue='YEAR_ID')
plt.xticks()
plt.show()
#Nov 2004 had the highest sales. Year 2005 had only 5 months data reported hence the low sales in the year. Also, revenue was increasing every year. 


# Country with the most sales

# In[71]:


unique_countries=df['COUNTRY'].unique()
temp= pd.DataFrame()
for i, country in enumerate(unique_countries):
        country_data=df[df['COUNTRY']== country]
        country_data= country_data.groupby('YEAR_ID')['SALES'].sum().reset_index()
        country_data['COUNTRY']= country
        temp= pd.concat([temp, country_data], ignore_index= True)
plt.figure(figsize= (20,8))
plt.title('Sales Volume by Country')
a=sns.barplot(x= 'COUNTRY', y='SALES', data=temp, hue='YEAR_ID')
plt.xticks()
plt.show()
        


# USA  had the highest sales followed by France and Norway. Norway had no data recorded for 2005. 

# In[72]:


df.head(2)


# Country with More Sales Growth

# In[73]:


df['COUNTRY'].unique()


# In[74]:


df['YEAR_ID'].unique()


# In[75]:


unique_countries=df['COUNTRY'].unique()
temp= pd.DataFrame()
for i, country in enumerate(unique_countries):
    country_data=df[df['COUNTRY']==country]
    country_data= country_data.groupby('YEAR_ID')['SALES'].sum().reset_index()
    country_data['COUNTRY']= country
    temp= pd.concat([temp, country_data], ignore_index= True)
temp.head(2)


# In[76]:


temp['GROWTH_RATE']= temp['SALES'].pct_change(periods=1)*100
temp.head(2)


# In[77]:


sns.lineplot(data=temp,
            x='COUNTRY',
            y= 'GROWTH_RATE')
plt.title('Growth Rate by Country')
plt.xticks(rotation= 90)
plt.show()
# Belgium had the highest growth rate


# Most sold items by year
# 

# In[79]:


df3=df.groupby('YEAR_ID')['PRODUCTLINE'].value_counts()
df3

##Classic cars and vintage cars are the most selling cproducts in the 3 years.


# In[48]:


dfs= df['PRODUCTLINE'].value_counts().reset_index()
dfs


# Top Customers

# In[27]:


unique_years = df['YEAR_ID'].unique()
# Create subplots for each year
for i, year in enumerate(unique_years):
    year_data = df[df['YEAR_ID'] == year]
    year_data=year_data.groupby('CUSTOMERNAME')['SALES'].sum().reset_index()
    year_data['YEAR_ID'] = year
    plt.figure(figsize=(20,8))
    plt.title(str(year)+" Revenue by Customer (TOP 20)") # add title 
    year_data =year_data.sort_values(by = "SALES", ascending=False)
    year_data=year_data.head(20)
    a= sns.barplot(x='CUSTOMERNAME',y='SALES',data=year_data)
    plt.xticks(rotation = 90)
    plt.show()


# Revenue contributed by the top 20% customers every year

# In[28]:


unique_years= df['YEAR_ID'].unique()
temp2003= pd.DataFrame()
temp2005= pd.DataFrame()
temp2006= pd.DataFrame()
for i, year in enumerate(unique_years):
    year_data= df[df['YEAR_ID']==year]
    year_data= year_data.groupby('CUSTOMERNAME')['SALES'].sum().sort_values(ascending= False).reset_index()
    year_data['YEAR_ID']= year
    
    if(year==2003):
        temp2003= year_data
    elif(year==2004):
        temp2004= year_data
    else:
        temp2005= year_data
        

temp2003['revenue_accum']= temp2003['SALES'].cumsum()
temp2003['%revenue_accum']= temp2003['revenue_accum']/temp2003['SALES'].sum()
n= int(0.2* len(temp2003.index))
temp2003.head(n)

label=['Top 20% customers', 'Others']


# In[29]:


data= [(temp2003.head(n)['%revenue_accum'].max())*100, (1- temp2003.head(n)['%revenue_accum'].max())*100]
plt.pie(data, labels=label, autopct='%1.1f%%', explode=(0, 0.01), startangle=90)
plt.title('% revenue contribution by top 20% customers yr 2003')
plt.show()


# In 2003, the top 20% customers contributed 42.7% of the total revenue earned that year.

# In[30]:


temp2004['revenue_accum']= temp2004['SALES'].cumsum()
temp2004['%revenue_accum']= temp2004['revenue_accum']/temp2004['SALES'].sum()
n=int(0.2*len(temp2004.index))
label= ['Top 20% customers', 'Others']
temp2004.head(n)


# In[31]:


data= [(temp2004.head(n)['%revenue_accum'].max())*100, (1- temp2004.head(n)['%revenue_accum'].max())*100]
plt.pie(data, labels= label, autopct='%1.1f%%', explode=(0, 0.01), startangle=90)
plt.title('%revenue contributed by top 20% customers yr 2004')
plt.show()


# In[32]:


temp2005['revenue_accum']= temp2005['SALES'].cumsum()
temp2005['%revenue_accum']= temp2005['revenue_accum']/temp2005['SALES'].sum()
n=int(0.2*len(temp2005.index))
label= ['Top 20% customers', 'Others']
temp2005.head(n)


# In[33]:


data= [(temp2005.head(n)['%revenue_accum'].max())*100, (1- temp2005.head(n)['%revenue_accum'].max())*100]
plt.pie(data, labels= label, autopct='%1.1f%%', explode=(0, 0.01), startangle=90)
plt.title('%revenue contributed by top 20% customers yr 2005')
plt.show()

yr 2005 had top20% customers contributing the highest % of the year's total revenue compared to yr 2004 and yr 2003
#                                  END
#                                  
#                                  THANK YOU

# In[ ]:




