#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import Libraries
import csv
import math
    
# Part 1
def part1(data):
    for i in range (1, len(data)):
        if '-' in data[i][1]:
            bounds = data[i][1].split('-')
            data[i][1] = round((int(bounds[0])+int(bounds[1]))/2);
    return data

# Part 2
def part2(data):
    for i in range(1, len(data)):
        # date_onset_symptoms
        bounds_1 = data[i][8].split('.')
        data[i][8] = bounds_1[1]+'.'+bounds_1[0]+'.'+bounds_1[2]
        # date_admission_hospital
        bounds_2 = data[i][9].split('.')
        data[i][9] = bounds_2[1]+'.'+bounds_2[0]+'.'+bounds_2[2]
        # date_confirmation
        bounds_3 = data[i][10].split('.')
        data[i][10] = bounds_3[1]+'.'+bounds_3[0]+'.'+bounds_3[2]
    return data;

# Part 3
def part3(data):
    
    # Dictionaries
    avg_lat = {}
    avg_long = {}
    
    # Find average latitudes for every province
    for i in range(1, len(data)):
        latitude = float(data[i][6])
        if math.isnan(latitude):
            continue
        province = data[i][4]
        if province in avg_lat:
            old_average = avg_lat[province][0]
            old_frequency = avg_lat[province][1]
            new_frequency = old_frequency + 1
            new_average = ((old_average*old_frequency)+latitude)/(new_frequency)
            avg_lat[province] = [new_average, new_frequency]
        else:
            avg_lat[province] = [latitude, 1]
            
    # Find average longitudes for every province
    for i in range(1, len(data)):
        longitude = float(data[i][7])
        if math.isnan(longitude):
            continue
        province = data[i][4]
        if province in avg_long:
            old_average = avg_long[province][0]
            old_frequency = avg_long[province][1]
            new_frequency = old_frequency + 1
            new_average = ((old_average*old_frequency)+longitude)/(new_frequency)
            avg_long[province] =[new_average, new_frequency]
        else:
            avg_long[province] = [longitude, 1]
            
    # Update Data
    for i in range(1, len(data)):
        province = data[i][4]
        latitude = float(data[i][6])
        longitude = float(data[i][7])
        if math.isnan(latitude):
            data[i][6] = round(avg_lat[province][0],2)
        if math.isnan(longitude):
            data[i][7] = round(avg_long[province][0],2)
        
    return data

def part4(data): 
    provinces = {}
    # Find the frequency of each city in a province
    for i in range(1, len(data)):
        city = data[i][3]
        if city == "NaN":
            continue
        province = data[i][4]
        if province in provinces:
            if any(city in tuples for tuples in provinces[province]):
                for i in range (len(provinces[province])):
                    tup = provinces[province][i]
                    if tup[0] == city:
                          provinces[province][i][1] = tup[1] + 1
            else:
                provinces[province].append([city, 1])
        else:
            provinces[province] = [[city,1]]
    # Sort all cities by frequencies
    for key, value in provinces.items():
        value.sort(key = lambda x: x[1])
        value.reverse()
    # Find most frequent city in each province
    most_occuring_cities = {}
    for key, value in provinces.items():
        if len(value) == 1:
            most_occuring_cities[key] = value[0][0]
        else: 
            cities_list = []
            cities_list.append(value[0][0])
            top_frequency = value[0][1]
            for i in range(1,len(value)):
                if(top_frequency > value[i][1]):
                    break
                else:
                    cities_list.append(value[i][0])
            cities_list.sort()
            most_occuring_cities[key] = cities_list[0]      
    # Update data
    for i in range(1, len(data)):
        city = data[i][3]
        if city == "NaN":
            data[i][3] = most_occuring_cities[data[i][4]]
    return data

def part5(data):
    
    provinces = {}
    
    #Calculate frequency of each symptom for each province
    for i in range(1, len(data)):
        symptoms = data[i][11]
        if symptoms == "NaN":
            continue
        bounds = symptoms.split(';')
        for j in range(len(bounds)):
            bounds[j] = bounds[j].strip()
        province = data[i][4]
        if province in provinces:
            for s in bounds:
                if s in provinces[province]:
                    provinces[province][s] = provinces[province][s] + 1
                else:
                    provinces[province][s] = 1     
        else:
            provinces[province] = {}
            for s in bounds:
                provinces[province][s] = 1;    
    
    # Find the most frequenct symtpoms
    largest_symptoms = {}
    for providence, symptoms in provinces.items():
        symptoms_array = []
        max_freq = -1
        for s, freq  in symptoms.items():
            if freq > max_freq:
                symptoms_array.clear()
                symptoms_array.append(s)
                max_freq = freq
            elif freq == max_freq:
                symptoms_array.append(s)
        symptoms_array.sort()
        largest_symptoms[providence] = symptoms_array[0]
    for i in range(1, len(data)):  
        symptoms = data[i][11]
        province = data[i][4]
        if symptoms == "NaN":
            data[i][11] = largest_symptoms[province]
    return data

# Main Method
def main():
    with open('covidTrain.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    data = part1(data)
    data = part2(data)
    data = part3(data)
    data = part4(data)
    data = part5(data)   
    with open("covidResult.csv","w+") as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerows(data) 
# Execute Main Method
main()


# In[ ]:




