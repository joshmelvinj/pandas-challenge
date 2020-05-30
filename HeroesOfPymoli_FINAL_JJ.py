#!/usr/bin/env python
# coding: utf-8

# ### Heroes Of Pymoli Data Analysis
# * Of the 1163 active players, the vast majority are male (84%). There also exists, a smaller, but notable proportion of female players (14%).
# 
# * Our peak age demographic falls between 20-24 (44.8%) with secondary groups falling between 15-19 (18.60%) and 25-29 (13.4%).  
# -----

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[274]:


# Dependencies and Setup
import pandas as pd
import numpy as np 
import os

# File to Load (Remember to Change These)
Heroes_Data = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(Heroes_Data)


# In[275]:


purchase_data.columns


# ## Player Count

# * Display the total number of players
# 

# In[276]:


player_count = len(purchase_data["SN"].value_counts())


# In[277]:


total_players = pd.DataFrame({"Total Players":[player_count]})
total_players


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[278]:


unique_items = len((purchase_data["Item ID"]).unique())


# In[279]:


avg_price = (purchase_data["Price"]).mean()


# In[280]:


number_purchases = (purchase_data["Purchase ID"]).count()


# In[281]:


total_revenue = (purchase_data["Price"]).sum()


# In[282]:


purchase_analysis = pd.DataFrame({"Number of Unique Items":[unique_items],
                                 "Average Price ($)":[avg_price],
                                 "Number of Purchases":[number_purchases],
                                 "Total Revenue ($)":[total_revenue]})


# In[283]:


purchase_analysis.style.format({"Average Price ($)":"${:,.2f}",
                               "Total Revenue ($)":"${:,.2f}"})


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[284]:


grouped_df = purchase_data.groupby(["Gender"]) 


# In[285]:


gender_count = grouped_df.nunique()["SN"]


# In[286]:


gender_percent = gender_count/ player_count * 100


# In[287]:


gender_dem_df = pd.DataFrame({"Total Count": gender_count,
                              "Percentage of Players (%)": gender_percent})


# In[288]:


gender_dem_df.index.name = None


# In[289]:


gender_dem_df.sort_values(["Total Count"], ascending = False).style.format({"Percentage of Players (%)":"%{:.2f}"})


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[290]:


purchase_count = purchase_data.groupby(["Gender"]).count()["Price"]


# In[291]:


avg_purchase_price = purchase_data.groupby(["Gender"]).mean()["Price"]


# In[292]:


purchase_tot = purchase_data.groupby(["Gender"]).sum()["Price"]


# In[293]:


avg_purchase_per_person = purchase_tot/gender_count


# In[294]:


purchase_analysis = pd.DataFrame({"Purchase Count":purchase_count,
                                "Average Purchase Price ($)":avg_purchase_price,
                                "Total Purchase Value ($)": purchase_tot,
                                "Normalized Total ($)":avg_purchase_per_person})


# In[295]:


purchase_analysis.style.format({"Average Purchase Price ($)":"${:.2f}", 
                               "Total Purchase Value ($)":"${:.2f}",
                               "Normalized Total ($)":"${:.2f}"})


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[296]:


organized_df = purchase_data.drop_duplicates("SN")


# In[297]:


bins = [0,9.90,14.90,19.90,24.90,29.90,34.90,39.90,120]
groups = ['<10','10-14','15-19','20-24','25-29','30-34','35-39','40+']


# In[298]:


organized_df["Age Groups"] = pd.cut(organized_df["Age"], bins, labels=groups)


# In[299]:


ages_grouped = organized_df.groupby(["Age Groups"])


# In[300]:


age_group_tot = ages_grouped["SN"].nunique()


# In[301]:


age_group_percent = (age_group_tot / player_count) * 100


# In[302]:


age_demographics = pd.DataFrame({"Total Count": age_group_tot, "Percentage of Players (%)": age_group_percent})


# In[303]:


age_demographics.index.name = None


# In[304]:


age_demographics.style.format({"Percentage of Players (%)":"%{:,.2f}"})


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[305]:


bins = [0,9.90,14.90,19.90,24.90,29.90,34.90,39.90,120]
groups = ['<10','10-14','15-19','20-24','25-29','30-34','35-39','40+']


# In[306]:


age_group_purchases = ages_grouped["Purchase ID"].count()


# In[307]:


avg_group_purchase_price = ages_grouped["Price"].mean()


# In[308]:


tot_purchases_per_group = ages_grouped["Price"].sum()


# In[309]:


avg_purchase_per_person = tot_purchases_per_group/age_group_tot


# In[310]:


purchase_demographics = pd.DataFrame({"Purchase Count": age_group_purchases, "Average Purchase Price ($)": avg_group_purchase_price, "Total Purchase Value ($)": tot_purchases_per_group, "Avg Total Purchase per Person ($)": avg_purchase_per_person})


# In[311]:


purchase_demographics.index.name = None
purchase_demographics.style.format({"Average Purchase Price ($)":"${:,.2f}", "Total Purchase Value ($)":"${:,.2f}", "Avg Total Purchase per Person ($)":"${:,.2f}"})


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[312]:


user_df = purchase_data.groupby(["SN"])


# In[313]:


user_purchase_count = user_df["Purchase ID"].count()


# In[314]:


user_avg_purchase_price = user_df["Price"].mean()


# In[315]:


tot_purchase_value = user_df["Price"].sum()


# In[316]:


biggest_spenders = pd.DataFrame({"Purchase Count": user_purchase_count,
                                "Average Purchase Price ($)": user_avg_purchase_price,
                                "Total Purchase Value ($)":tot_purchase_value})


# In[317]:


biggest_spenders_format = biggest_spenders.sort_values(["Total Purchase Value ($)"], ascending=False).head()


# In[318]:


biggest_spenders_format.style.format({"Purchase Count":"${:,.2f}",
                                "Average Purchase Price ($)":"${:,.2f}",
                                "Total Purchase Value ($)":"${:,.2f}"})
biggest_spenders_format.head()


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[319]:


most_popular = purchase_data[["Item ID", "Item Name", "Price"]]


# In[320]:


grouped_items = most_popular.groupby(["Item ID", "Item Name"])


# In[321]:


item_purchase_count = grouped_items["Price"].count()


# In[322]:


item_price = grouped_items["Price"].sum()


# In[323]:


item_value = item_price/item_purchase_count


# In[324]:


most_popular_items = pd.DataFrame({"Purchase Count":item_purchase_count,
                                  "Item Price ($)":item_value,
                                  "Total Purchase Value ($)":item_price})


# In[325]:


most_popular_items_format = most_popular_items.sort_values(["Purchase Count"], ascending=False).head()


# In[326]:


most_popular_items_format.style.format({"Item Price ($)":"${:,.2f}", "Total Purchase Value ($)":"${:,.2f}"})


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[327]:


most_popular_items_format = most_popular_items.sort_values(["Total Purchase Value ($)"], ascending=False).head()


# In[328]:


most_popular_items_format.style.format({"Item Price ($)":"${:,.2f}", "Total Purchase Value ($)":"${:,.2f}"})


# In[ ]:




