#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df_opr = pd.read_csv("fatec_opr.csv", sep="|", usecols=[2, 11])
df_opr.head(10)


# In[3]:


df_opr.dtypes


# In[4]:


df_opr['DOC_CLI'] = df_opr.DOC_CLI.astype('str')
df_opr.dtypes


# In[5]:


df_opr['DOC_CLI'].duplicated().sum()


# In[6]:


df_opr.describe


# In[7]:


df_opr.dtypes


# In[8]:


df_opr_ok = df_opr.loc[df_opr['DOC_CLI'].str.len() == 11]


# In[9]:


df_opr_ok.describe


# In[10]:


df_opr_ok.to_csv('df_opr_ok.csv', index=False, header=True)
print(df_opr_ok)


# In[ ]:




