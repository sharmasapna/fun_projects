#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

from datetime import datetime


# ## Importing data from the csv file downloaded from strava

# In[2]:



path = '/Users/sapnasharma/Downloads/export_37140684/activities.csv'
df = pd.read_csv(path)
df.head(3)


# ### Renaming the columns and converting Activity_Date to datetime object

# In[3]:


df.rename(columns = {"Activity Date":"Activity_Date",'Activity Name':'Activity_Name','Activity Type':'Activity_Type','Elapsed Time':'Duration'},inplace = True)
df = df[['Activity_Date', 'Distance']]
# converting to date
df['Activity_Date'] = pd.to_datetime(df['Activity_Date'])
df.head(3)


# ### Extracting the data for the year 2021

# In[4]:


df = df[df['Activity_Date'].dt.year == 2021]
df


# ### Converting the Activity_Date to date

# In[5]:


df['Activity_Date'] = pd.to_datetime(df['Activity_Date']).dt.date
df.head(3)


# ### Grouping by date to sum all the activities done in day

# In[6]:


df1 = df.groupby(['Activity_Date'],as_index = False).sum(['Distance'])
df1


# In[7]:


print(df.info(),df1.info())


# ### Creating a dataframe with all the dates in the year 2021

# In[8]:



from datetime import datetime, timedelta

def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days

start_date = datetime(2021, 1, 1)
end_date = datetime(2021, 12, 31)
    
complete_year = pd.DataFrame(date_range(start_date, end_date))
complete_year.rename(columns = {0:'Activity_Date'},inplace =True)
complete_year


# In[9]:


complete_year['Activity_Date'] = pd.to_datetime(complete_year['Activity_Date']).dt.date
complete_year.head(3)


# In[10]:


complete_year.info()


# ### Joining the activity file with the all dates dataframe

# In[11]:


merged_df = complete_year.merge(df1, on='Activity_Date', how='left')
merged_df.head(11)


# In[12]:


merged_df.to_csv('stats.csv')


# ### We will use turtle do draw the graphics

# In[13]:


import turtle
import pandas as pd
from datetime import datetime
import calendar


# In[14]:


df = merged_df.copy()
df['dt'] = pd.to_datetime(df['Activity_Date'])
my_window = turtle.Screen()
my_window. bgcolor("black")
tur = turtle.Turtle()
n=52 # total weeks in a year
k = 0
tur.speed(800)
tur.hideturtle() # we do not want to display the turtle icon
tur.width(0.01)

for i in range(n):
    tur.pencolor('grey')
    for j in range(7):                           # for each week

        tur.forward(30)
        if (df.Distance[k]) > 0:
            tur.dot(df.Distance[k],'cyan')       # when an activity is observed
        else:
            tur.dot(2,'red')                     # when no activity is performed
        k+=1
    tur.penup()
    tur.forward(40)
    tur.pencolor('cyan')
    s = calendar.month_name[df.dt[k].month][0:3] # Extracing first three alphabets of the month
    tur.pendown()
    tur.write(s,font = ("Calibri",8,"bold"))     # prints the month around the perifery
    tur.penup()
    tur.backward(250)
    tur.pendown()
    tur.left(360/n)                              # setting the angle to accomodate 52 weeks, n= 52
tur.penup()
active_days = df[df.Distance >0]['Distance'].count()
tur.setpos(-250,300)
tur.pendown()
tur.pencolor('cyan')
tur.write("Active Days : "+ str(active_days),font=("Calibri", 20, "bold")) # title display of active days
tur.penup()
tur.setpos(-250,270)
tur.pendown()
tur.pencolor('cyan')
tur.write("Total Distance : "+ str(int(df.Distance.sum()))+" Kms",font=("Calibri", 20, "bold")) # title display of total distance
tur.penup()

tur.setpos(-250,-300)
tur.pendown()
tur.pencolor('cyan')
tur.write("My Walk / Run / Bike /Hike Highlights of 2021",font=("Calibri", 20, "bold")) # title display of total distance


# In[15]:


turtle.done()


# ![title](my_stats.png)

# In[ ]:




