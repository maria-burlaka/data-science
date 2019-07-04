#!/usr/bin/env python
# coding: utf-8

# # App Store and Google Play
# 
# The aim of this project is to find out how popular apps are depending on their genres. Here were used data sets 
# from App Store and Google Play. Data was cleaned, prepared, genre frequencies were found. Using amount of installs
# and amount of reviews, there were found out relations between genre and inquiry for apps.
# 
# Links for data and documentation:
# - App Store - [Link](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home)
# - Google Play - [Link](https://www.kaggle.com/lava18/google-play-store-apps/home)
# 
# Goals:
# - to get some practice
# - to get additional knowledge
# - to improve data science skills

# In[14]:


from csv import reader
from langdetect import detect
from collections import OrderedDict


# ## Data reading

# In[2]:


open_as = open('AppleStore.csv')
open_gp = open(r'googleplaystore.csv', encoding="utf-8")

as_file = list(reader(open_as))
as_data = as_file[1:]
as_header = as_file[0]

gp_file = list(reader(open_gp))
gp_data = gp_file[1:]
gp_header = gp_file[0]


# ## Data exploration

# In[3]:


# Exploring the data

# A function for data exploration
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

        
print(as_header)
explore_data(as_data, 0, 2, True)
print('\n')
print(gp_header)
explore_data(gp_data, 0, 2, True)


# ## Data cleaning

# In[10]:


# A function for checking if a string is in english
def is_english(string):
    count = 0
    for char in string:
        if ord(char) > 127: count += 1
    if count > 4: return False
    
    
    
# App Store data cleaning
def as_cleaning(as_data):
    clean_data = []
    for i in range(len(as_data)):
        # Removing incomplete data
        if len(as_data[i]) == len(as_header): 
            clean_data.append(as_data[i])
        # Selecting free apps with names in english
        if as_data[i][5] == '0' or is_english(as_data[i][2]) != False: 
            clean_data.append(as_data[i])
        # Removing duplicates
        for k in range(0, i):
            if as_data[i][2] == as_data[k][2]:
                if as_data[i][6] >= as_data[k][6]:
                    clean_data.append(as_data[i])
                else:
                    clean_data.append(as_data[k])          
        # Removing apps with incorrect rating
        if float(as_data[i][8]) <= 5.0:
            clean_data.append(as_data[i])
    return clean_data

                    
# Google Play data cleaning                                      
def gp_cleaning(gp_data):
    # Removing an app with incorrect category
    del gp_data[10472]
    clean_data = []
    for i in range(len(gp_data)):
        # Removing incomplete data
        if len(gp_data[i]) == len(gp_header): 
            clean_data.append(gp_data[i])
        # Selecting free apps with names in english
        if gp_data[i][7] == 'Free' or is_english(gp_data[i][0]) != False: 
            clean_data.append(gp_data[i])
        # Removing duplicates
        for k in range(0, i):
            if gp_data[i][0] == gp_data[i][0]:
                if gp_data[i][6] >= gp_data[k][6]:
                    clean_data.append(gp_data[i])
                else:
                    clean_data.append(gp_data[k])
        # Removing apps with incorrect rating
        if float(gp_data[i][2]) <= 5.0:
            clean_data.append(gp_data[i])
    return clean_data


# App Store data cleaning
as_clean = as_cleaning(as_data)
        
# Google Play data cleaning
gp_clean = gp_cleaning(gp_data)


# ## Genre frequencies

# In[30]:


# Geting genre frequency on App Store
def as_genre_frequecy(as_data):
    genre_frequency = {}
    for row in as_data:
        if row[-5] in genre_frequency: genre_frequency[row[-5]] += 1
        else: genre_frequency[row[-5]] = 1
    return OrderedDict(sorted(genre_frequency.items(), key=lambda t: t[1], reverse = True))
            
            
# Geting genre frequency on Google Play
def gp_genre_frequecy(gp_data):
    genre_frequency = {}
    for row in gp_data:
        if row[-4] in genre_frequency: genre_frequency[row[-4]] += 1
        else: genre_frequency[row[-4]] = 1
    return OrderedDict(sorted(genre_frequency.items(), key=lambda t: t[1], reverse = True))


# Geting category frequency on Google Play
def gp_category_frequecy(gp_data):
    genre_frequency = {}
    for row in gp_data:
        if row[1] in genre_frequency: genre_frequency[row[1]] += 1
        else: genre_frequency[row[1]] = 1
    return OrderedDict(sorted(genre_frequency.items(), key=lambda t: t[1], reverse = True))

# A function for printing an ordered dictionary
def print_dict(freq):
    for item in freq:
        print(item, ': ', freq[item])


# Genre frequencies on App Store
as_genre_frequecy = as_genre_frequecy(as_clean)
print('App Store genres')
print_dict(as_genre_frequecy)

# Genre frequencies on Google Play
gp_genre_frequecy = gp_genre_frequecy(gp_clean)
print('\nGoogle Play genres')
print_dict(gp_genre_frequecy)

# Category frequencies on Google Play
gp_category_frequecy = gp_category_frequecy(gp_clean)
print('\nGoogle Play categories')
print_dict(gp_category_frequecy)


# ## Number of ratings (App Store, Google Play) and installs (Google Play) 
# To find out how popular a genre is

# In[41]:


# Finding an average amount of reviews per genre on App Store
def as_reviews_per_genre(as_data, as_genre_frequecy):
    as_reviews = {}
    for genre in as_genre_frequecy:
        count_of_apps = 0
        reviews = 0
        for row in as_data:
            if row[-5] == genre:
                count_of_apps += 1
                reviews += int(row[6])
        average_reviews = reviews / count_of_apps
        as_reviews[genre] = average_reviews
    as_reviews = OrderedDict(sorted(as_reviews.items(), key=lambda t: t[1], reverse = True))
    return as_reviews


# Finding an average amount of reviews per genre on Google Play
def gp_reviews_per_genre(gp_data, gp_genre_frequecy):
    gp_reviews = {}
    for genre in gp_genre_frequecy:
        count_of_apps = 0
        reviews = 0
        for row in gp_data:
            if row[-4] == genre:
                count_of_apps += 1
                reviews += int(row[3])
        average_reviews = reviews / count_of_apps
        gp_reviews[genre] = average_reviews
    gp_reviews = OrderedDict(sorted(gp_reviews.items(), key=lambda t: t[1], reverse = True))
    return gp_reviews


# Finding an average amount of installs per genre on Google Play
def gp_installs_per_genre(gp_data, gp_genre_frequecy):
    gp_installs = {}
    for genre in gp_genre_frequecy:
        installs = {}
        for row in gp_data:
            if row[-4] == genre:
                if row[5] in installs: 
                    installs[row[5]] += 1
                else:
                    installs[row[5]] = 1
        gp_installs[genre] = OrderedDict(sorted(installs.items(), key=lambda t: t[1], reverse = True))
    return gp_installs


as_average_reviews = as_reviews_per_genre(as_data, as_genre_frequecy)
print('Average amout of reviews per genre on App Store\n')
print_dict(as_average_reviews)
gp_average_reviews = gp_reviews_per_genre(gp_data, gp_genre_frequecy)
print('\n\n\nAverage amout of reviews per genre on Google Play\n')
print_dict(gp_average_reviews)
gp_average_installs = gp_installs_per_genre(gp_data, gp_genre_frequecy)
print('\n\n\nAverage amout of installs per genre on Google Play\n')
for genre in gp_average_installs:
    print(genre)
    for number in gp_average_installs[genre]:
        print(number,  ': ', gp_average_installs[genre][number])
    print('\n')
