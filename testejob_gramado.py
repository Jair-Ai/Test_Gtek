#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 08:17:55 2020

@author: jair_rapids
"""
import requests
from datetime import date, datetime, timedelta
import numpy as np
import calendar

# Define Global variable
global main_city, main_api, days, today



main_api = "0e69e4c3870122868c60b3a15dd03c78"

main_city = "Gramado"

days = 5

today = date.today()

days_of_week = []


def howManyDays(days: int = 5):

    """
    :param days: Days to check Forecast
    :return: Empty dict with date as Key
    """
    dict_days = {}
     
    for i in range(1, days+1):
        nome = (today + timedelta(days=i))
        dict_days[nome] = []
    
    return dict_days


def get_data(city: str, api: str):

    """

    :param city: Name Of city to check forecast
    :param api: Api of OpenWeather
    :return: 1-Json with all data, dict from howManyDays func
    """

    url = "http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}".format(city, api)
    data = requests.get(url)
    
    api_status_return = data.status_code
    
    if api_status_return == 200:
    
        data = requests.get(url)
    
        data_json = data.json()

        dict_days = howManyDays(days)

        return data_json, dict_days
   
    else:
        
        print(data.json()['message'])

        
def dict_d_umbrela(dict_days: dict, data: dict) -> dict:

    """
    :param dict_days: Dict to fill with Humidity data
    :param data: data from api call
    :return: dictionary with all moisture forecasts every 3 hours each day
    """

    
    data_w_hum = data['list']
    
    for each in data_w_hum:
        
        day_on_data = datetime.strptime(each['dt_txt'][:10], '%Y-%m-%d')
        
        if day_on_data.day != today.day:
            dict_days[day_on_data.date()].append(int(each['main']['humidity']))
       
   
    return dict_days
   

def when_take_umbrela(dict_days: dict):

    """
    :param dict_days: dict from dict_d_umbrela func
    :return : No return but print days to take Umbrela
    """
    
    list_days_umb = []
    
    to_print = ""
    
    for key in dict_days:
        if np.mean(dict_days[key]) > 70:
            list_days_umb.append(calendar.day_name[key.weekday()])
    
    if not list_days_umb:
        print("No need to take an umbrella for the next 5 days as it probably won't rain")
        
    elif len(list_days_umb) == 2:
        
        to_print = list_days_umb[0] + ' and ' + list_days_umb[1]
    
    elif len(list_days_umb) == 1:
        
        to_print = list_days_umb[0]

    else:
        
        for i in list_days_umb:
            if i == list_days_umb[-1]:
                to_print = to_print[:-2]
                to_print = to_print + " and " + i
                
            else:
                to_print = to_print + i + ", "

    print("You should take an umbrella in these days: {}.".format(to_print))
        

def main():
    
    data, dict_days = get_data(main_city, main_api)
    
    dict_hum = dict_d_umbrela(dict_days, data)
    
    when_take_umbrela(dict_hum)


if __name__ == "__main__":
    main()
