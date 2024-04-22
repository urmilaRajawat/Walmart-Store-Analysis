#!/usr/bin/env python
# coding: utf-8

# In[1]:


# importing libraries 
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 


# In[2]:


df = pd.read_csv(r'C:\Users\Rathore\Downloads\walmart.csv')
df.head(20)


# In[3]:


df.info()


# # Figuring out the Top stores of Walmart
# 

# In[4]:


# df_store_rank = df.groupby('Store')['Weekly_Sales'].sum()
df_store_rank = df.groupby('Store')['Weekly_Sales'].agg(['sum','count'])
df_store_rank=df_store_rank.sort_values('sum',ascending=False)
df_store_rank


# In[5]:


# retrieving the top and bottom performing stores based on sales 
stores_id_rank = df_store_rank.index
top_stores_id = stores_id_rank[:3]
bottom_stores_id = stores_id_rank[-3:]
bottom_stores_id


# In[6]:


top_stores_id


# we can say that the top stores are Store number 20,4 and 14 and bottom stores are 5,44,33 on the basis if weekly sales
# 

# In[7]:


# creating separate dataframes consisting of store data based on store id  

# selecting rows based on condition
top_stores_list = df[df['Store'].isin(top_stores_id)]
bottom_stores_list = df[df['Store'].isin(bottom_stores_id)]
top_stores_list 


# # Visualise Top and Bottom Performing Stores
# 

# In[8]:


# code to visualise the top and bottom perfroming stores 

top_stores_list.loc[:, 'Weekly_Sales_inLakhs'] = top_stores_list['Weekly_Sales'].apply(lambda x: x / 100000)
bottom_stores_list.loc[:, 'Weekly_Sales_inLakhs'] = bottom_stores_list['Weekly_Sales'].apply(lambda x: x / 100000)

# adding the sales of top  performing stores and grouping them by Store id 
top_stores_total_sales = top_stores_list.groupby('Store')['Weekly_Sales_inLakhs'].agg(['sum','count'])

# renaming columns and creating a store_id column 
top_stores_total_sales['Store id'] = top_stores_total_sales.index 
top_stores_total_sales.rename(columns = {'sum':'Total_Sales(in Lakhs)'}, inplace = True)
top_stores_total_sales


# adding the sales of bottom  performing stores and grouping them by Store id 
bottom_stores_total_sales = bottom_stores_list.groupby('Store')['Weekly_Sales_inLakhs'].agg(['sum','count'])

# renaming columns and creating a store_id column 
bottom_stores_total_sales['Store id'] = bottom_stores_total_sales.index 
bottom_stores_total_sales.rename(columns = {'sum':'Total_Sales(in Lakhs)'}, inplace = True)
bottom_stores_total_sales


# In[13]:


import seaborn as sns
plt.figure(figsize=(6,4))
plot_top = sns.barplot(x = 'Store id',
            y = 'Total_Sales(in Lakhs)',
            color='green',
            data = top_stores_total_sales)
 

plot_top .bar_label(plot_top .containers[0])
plt.show()



plot_bottom = sns.barplot(x = 'Store id',
            y = 'Total_Sales(in Lakhs)',
            color='r',
            data = bottom_stores_total_sales)
 

plot_bottom.bar_label(plot_bottom.containers[0])


# Show the plot
plt.show()


# # Temperature Difference Between the high and low selling stores

# In[18]:


bottom_avg_temp = bottom_stores_list['Temperature'].mean()
top_avg_temp= top_stores_list['Temperature'].mean()
percentage = ((bottom_avg_temp-top_avg_temp)/top_avg_temp)*100
print(f"Top selling store average tempertaure is {top_avg_temp}")
print(f"Bottom selling store average tempertaure is", bottom_avg_temp)
print("Percentage Increase in Tempertaure = ",round(percentage,1),'%')


# Top selling store average tempertaure = 58.49
# 
# Bottom selling store average tempertaure = 66.61
# 
# Percentage Increase = **13.9 %**

# One of the reasons for more Weekly sales could be the ideal temperature at the stores locations This is one of the factors that can be considered when setting up Walmart stores in the near future

# # Fuel Price Difference Between the Top and Bottom Stores no significant diff

# In[19]:


bottom_avg_fuel=bottom_stores_list['Fuel_Price'].mean()
top_avg_fuel=top_stores_list['Fuel_Price'].mean()
percentage = ((bottom_avg_temp-top_avg_fuel)/top_avg_fuel) * 100
print(f"Top selling store average Fuel Price  is {top_avg_fuel}")
print(f"Bottom selling store average Fuel Price  is {bottom_avg_fuel}")
print("There is no significant difference between the fuel prices ")


# In[20]:


df.head()


# # Association between Fuel price and Weekly sales

# In[23]:


stats = df['Fuel_Price'].describe()
min = stats[3]
max = stats[7]
q1=stats[4]
q3=stats[6]
stats


# In[28]:


# dataframe containing fuel price between the lowest and first quartile price range 
min_fuel_data = df[df['Fuel_Price']<= q1]
avg_sales_fuel_min = min_fuel_data['Weekly_Sales'].mean()

#dataframe containing fuel price between the highest and third quartile price range 
max_fuel_data = df[(df['Fuel_Price']>= q3) & (df['Fuel_Price']<= max)]
avg_sales_fuel_max = max_fuel_data['Weekly_Sales'].mean()

print('weekly sales of min is', avg_sales_fuel_min)
print('weekly sales of max is', avg_sales_fuel_max)


# One of the reasons for such cases can be that the vicinity where the fuel prices are higher have better incomes as compared to people where fuel prices are less **Verifying the mentioned hypothesis**

# In[30]:


avg_Unemployment_rate_min = min_fuel_data['Unemployment'].median()
avg_Unemployment_rate_max= max_fuel_data['Unemployment'].median()

print(f"unemployemnt rate is {avg_Unemployment_rate_min}")
print(f"unemployemnt rate is {avg_Unemployment_rate_max}")

unemployment_percent_increase =((avg_Unemployment_rate_min - avg_Unemployment_rate_max)/avg_Unemployment_rate_max)*100
print('Increase in Unemployemnt rate is ',round(unemployment_percent_increase,2),"%")


# We can see there is a **2.35%** increase in unemployemnt rate when comparing the low_fuel_area stores and high_fuel_area stores

# # Association with Holiday Flag and Weekly sales

# In[31]:


holiday_week = df[df['Holiday_Flag']==1]
non_holdiay_week = df[df['Holiday_Flag']==0]

x=holiday_week['Weekly_Sales'].mean()
y=non_holdiay_week['Weekly_Sales'].mean()
print(f'Holdiya week Sales = {x} Non Holiday week sales = { y}')
percentage_increase_holiday_y_n = round(((x-y)/y)*100,2)
print(percentage_increase_holiday_y_n,'%')


# We can see that there is a **7.84 %** percentage increase in sales as compared to weeks which have holidays during the week. This suggests Walmart stores that if holidays occur during the week one can expect decent amount of sales and one can apply marketing strategies to further benefit the stores

# Upon further comparing the results of Holiday week sales as comparing to the top and bottom performing sales

# In[42]:


top_stores_holiday_yes= top_stores_list[top_stores_list['Holiday_Flag']==1]
avg_sales_holiday_yes_topStores=top_stores_holiday_yes['Weekly_Sales'].mean()


bottom_stores_holiday_yes = bottom_stores_list[bottom_stores_list['Holiday_Flag']==1]
avg_sales_holiday_yes_bottomStores=bottom_stores_holiday_yes['Weekly_Sales'].mean()


percentage_change = ((avg_sales_holiday_yes_topStores-avg_sales_holiday_yes_bottomStores)/avg_sales_holiday_yes_bottomStores)*100

print(round((percentage_change),2),'%')


# We can see that when comparing the bottom and top performing Walmart stores there is a **620.24 %** increase in sales

# In[33]:


df.describe()


# # Creating a new column for Holiday Event name

# This is used to check the sales during the holiday days and figure out the top seling stores and bottom selling stores sales stats wrt to Holidays

# In[34]:


df.tail(10)


# In[35]:


# Function to create a new column called Holiday_name and based on that assign values 
def holiday_groups(x):
    if (x == '12-02-2010') | (x=='11-02-2011') | (x=='10-02-0212')| (x=='08-02-2013') :
        return 'Super Bowl'

    elif (x == '07-09-2012') |( x=='10-09-2010')|( x=='09-09-2011')|(x=='06-09-2013'):
        return 'Labour Day' 
   
    elif (x=='26-11-2010')| (x=='25-11-2011')|( x=='23-11-2012')|(x=='29-11-2013'):
        return 'Thanksgiving'
 
    elif (x=='31-12-2010') |( x=='30-12-2011')|( x=='28-12-2011')|(x=='27-12-2011'):
        return 'Christmas'
    else:
        return 'Not a Holiday'

df['Holiday_Name'] = df['Date'].apply(holiday_groups)


# In[36]:


df['Holiday_Name'].unique()


# In[37]:


store_holiday_sales = df.groupby('Holiday_Name')['Weekly_Sales'].mean()


# In[38]:


store_holiday_sales


# In[39]:


christmas_sales = df[df['Holiday_Name']=='Christmas']
labour_day_sales = df[df['Holiday_Name']=='Labour Day']
super_bowl_sales = df[df['Holiday_Name']=='Super Bowl']
thanksgiving_sales = df[df['Holiday_Name']=='Thanksgiving']


# In[40]:


print(christmas_sales['Weekly_Sales'].mean())
print(labour_day_sales['Weekly_Sales'].mean())
print(super_bowl_sales['Weekly_Sales'].mean())
print(thanksgiving_sales['Weekly_Sales'].mean())


# In[41]:


top_stores_list['Holiday_Name'] = top_stores_list['Date'].apply(holiday_groups)

christmas_sales_top = top_stores_list[top_stores_list['Holiday_Name']=='Christmas']
labour_day_sales_top = top_stores_list[top_stores_list['Holiday_Name']=='Labour Day']
super_bowl_sales_top = top_stores_list[top_stores_list['Holiday_Name']=='Super Bowl']
thanksgiving_sales_top = top_stores_list[top_stores_list['Holiday_Name']=='Thanksgiving']

print("***********Top Performing Stores Average Weekly Sales***********")

print("Christmas :",christmas_sales_top['Weekly_Sales'].mean())
print("Labour Day :",labour_day_sales_top['Weekly_Sales'].mean())
print("Super Bowl :",super_bowl_sales_top['Weekly_Sales'].mean())
print("Thanksgiving :",thanksgiving_sales_top['Weekly_Sales'].mean())





bottom_stores_list['Holiday_Name'] = bottom_stores_list['Date'].apply(holiday_groups)

christmas_sales_bottom = bottom_stores_list[bottom_stores_list['Holiday_Name']=='Christmas']
labour_day_sales_bottom = bottom_stores_list[bottom_stores_list['Holiday_Name']=='Labour Day']
super_bowl_sales_bottom = bottom_stores_list[bottom_stores_list['Holiday_Name']=='Super Bowl']
thanksgiving_sales_bottom = bottom_stores_list[bottom_stores_list['Holiday_Name']=='Thanksgiving']

print("***********Bottom Performing Stores Average Weekly Sales***********")
print("Christams:",christmas_sales_bottom['Weekly_Sales'].mean())
print("Labour Day:",labour_day_sales_bottom['Weekly_Sales'].mean())
print("Super Bowl:",super_bowl_sales_bottom['Weekly_Sales'].mean())
print("Thanksgiving:",thanksgiving_sales_bottom['Weekly_Sales'].mean())


# We can see that another thing that differentiates the top and bottom selling Stores are the huge difference in sales during the Holidays. To effectively improve the low performing stores one can use marketing strategies like social media tactics and usage of posters and banners to show users about the offers during the Holiday period

# # Key Takeaways

# 1. The **top 3** performing stores are **20,4,14** and the **bottom 3** performing stores are **5,44,33**
# 2. Weekly sales during weeks that consist of holidays are crucial as there was a **7.84%** increase in sales compared to non-holiday week sales. The bottom performing stores can up their marketing strategies by focusing on weeks that consist of holidays.
# 3. Stores where fuel prices are higher generate more sales as compared to low fuel price located stores. One of the reasons can be the locality where the fuel prices are high have a higher income because we saw there was a **2.35%** increase in the unemployment rate of bottom-performing stores as compared to the high-performing stores.
# 4. The average temperature of top-performing stores was **58.49 units** whereas the bottom-performing stores were **66.61 units**. The ideal temperature of the top stores makes the customers visit more often. This factor can be considered when we would need to set up new Walmart Stores in the Future.

# In[ ]:




