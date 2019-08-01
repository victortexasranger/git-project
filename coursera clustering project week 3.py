#!/usr/bin/env python
# coding: utf-8

# # tranforming wikipedia into pandas data frame
# 

# In[1]:


import pandas as pd
import requests
from bs4 import BeautifulSoup


# In[2]:


wiki_url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
resp = requests.get(wiki_url).text


# In[3]:


soup = BeautifulSoup(resp, 'xml')#Beautiful Soup to Parse the url page


# In[4]:


table=soup.find('table')


# In[5]:


column_names=['Postalcode','Borough','Neighbourhood']
df = pd.DataFrame(columns=column_names)


# In[6]:


# extracting information from the table
for tr_cell in table.find_all('tr'):
    row_data=[]
    for td_cell in tr_cell.find_all('td'):
        row_data.append(td_cell.text.strip())
    if len(row_data)==3:
        df.loc[len(df)] = row_data


# In[7]:


df.head()


# In[8]:


# remove rows where Borough is 'Not assigned'
df=df[df['Borough']!='Not assigned']


# In[9]:


# assign Neighbourhood=Borough where Neighbourhood is 'Not assigned'
df[df['Neighbourhood']=='Not assigned']=df['Borough']


# In[10]:


df.head()


# In[11]:


# group multiple Neighbourhood under one Postcode
temp_df=df.groupby('Postalcode')['Neighbourhood'].apply(lambda x: "%s" % ', '.join(x))
temp_df=temp_df.reset_index(drop=False)
temp_df.rename(columns={'Neighbourhood':'Neighbourhood_joined'},inplace=True)


# In[12]:


# join the newly constructed joined data frame
df_merge = pd.merge(df, temp_df, on='Postalcode')


# In[13]:


# drop the Neighbourhood column
df_merge.drop(['Neighbourhood'],axis=1,inplace=True)


# In[14]:


# drop duplicates from the data frame
df_merge.drop_duplicates(inplace=True)


# In[15]:


# rename Neighbourhood_joined back to Neighbourhood
df_merge.rename(columns={'Neighbourhood_joined':'Neighbourhood'},inplace=True)


# In[16]:


df_merge.head()


# In[17]:


df_merge.shape


# In[ ]:




