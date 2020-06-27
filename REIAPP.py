# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 01:05:50 2020

@author: Boming
"""

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import itertools
import streamlit as st


def net_operating(price, rent, tax_rate, property_mgmt, repairs, vacancy,insurance
                  , utilities, broker_fee, HOA):
    
    #Takes input as monthly mortgage amount and monthly rental amount
    #Uses managment expense, amount for repairs, vacancy ratio
    #Example input: net_operating(1000,1,400,200)
    #879.33
    #1000 - 16.67 (tax) - 100 (managment) - 4 (repairs)
    
    mortgage_amt = mortgage_monthly(price,30,Annual_Interest_Rate,down_payment_percent)
    prop_managment = rent * (property_mgmt/100)
    prop_tax = (price * (tax_rate/100)/12)
    prop_repairs = rent*repairs/100
    vacancy = rent*vacancy/100
    utilities = rent * utilities/100
    broker_fee = rent * broker_fee/100
    HOA = rent * HOA/100
    insurance = rent * insurance/100
    #These sections are a list of all the expenses used and formulas for each
    
    net_income = round(rent - prop_managment - prop_tax - prop_repairs - vacancy - mortgage_amt - utilities - insurance - broker_fee - HOA,2)
    #Summing up expenses
    output = [prop_managment, prop_tax, prop_repairs, insurance ,vacancy, utilities, broker_fee, HOA,net_income]
  
    
    return output

def down_payment(price,down_payment_percent):
    #This function takes the price and the downpayment rate and returns the downpayment amount 
    #Ie down_payment(100,20) returns 20
    amt_down = price*down_payment_percent/100
    return(amt_down)

def mortgage_monthly(price,years,Annual_Interest_Rate,down_payment_percent):
    
    
    #This implements an approach to finding a monthly mortgage amount from the purchase price,
    #years and percent. 
    #Sample input: (300000,20,4) = 2422
    #
    
    
    down = down_payment(price,down_payment_percent)
    loan = price - down
    months = years*12
    interest_monthly = (Annual_Interest_Rate/100)/12
    interest_plus = interest_monthly + 1
    exponent = (interest_plus)**(-1*months)
    subtract = 1 - exponent
    division = interest_monthly / subtract
    payment = division * loan
    
    
    return(payment)


#def price_mine(url):
    #Currently this function takes an input of a URL and returns the listing prices 
    #The site it mines is remax
    #The input must be a string input, we can reformat the input to force this to work
    #Next we use regex to remove space and commas and dollar signs 
  #  headers = ({'User-Agent':
  #          'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
   # Link = url
  #  source= requests.get(Link,headers=headers).text
  #  html_soup = BeautifulSoup(source, 'html.parser')
  #  prices = html_soup.find('span',{'class': 'price'}).text
  #  prices = prices.replace(",", "")
  #  prices = prices.replace("$", "")
  #  #prices = prices.replace(" ", "")
 #   prices = float(prices)
 # 
 #   return prices
    
    
def cap_rate(monthly_income, price):
    #This function takes net income, and price and calculates the cap rate
    #
    cap_rate = round(((monthly_income*12) / price)*100,2)
    
    return cap_rate


def cash_on_cash(monthly_income, down_payment):
    cash_return = round(((monthly_income*12)/down_payment)*100,2)
    return cash_return

st.title('Real Estate Investment Analysis App')

#insert image cuz it's too blank bruh
from PIL import Image
import requests
from io import BytesIO

response = requests.get('https://www.nsaen.com/wp-content/uploads/2018/07/building-wealth.jpg')
img = Image.open(BytesIO(response.content))
st.image(img,use_column_width=True)

st.subheader("Return Metrics")

#trial = st.text_input('Enter the Listing URL from Realtor.com to get the price:  ')
#trial = price_mine(str(trial))
#st.write("""Any real estate listing can be automatically analyzed""") 

# trial = input("Enter a URL to a Remax listing:   ")
# rent_amt = input("Enter the monthly rent price:  ")
# property_tax = input("Enter the tax rate:  ")
#We have to change these generic inputs to streamlit inputs

st.sidebar.markdown("**Purchase_Info:** ")         
#trial = st.sidebar.text_input("Enter the listing URL:   ")

Price = st.sidebar.text_input(label = "Enter the Purchase Price: ",value ='100000' )#value = trial if trial is not None else '100000')
down_payment_percent = st.sidebar.slider("Enter the Down Payment Rate (% of rent):   ", 0,100,20)
Annual_Interest_Rate = st.sidebar.text_input("Enter the Annual Interest Rate (% of rent):   ", value = '3.5')

st.sidebar.markdown("**Revenue_Variables:** ")
#st.sidebar.text("Revenue Variables: ") 
rent_amt = st.sidebar.text_input("Enter the monthly rent price:   ", value = '1000')
vacancy = st.sidebar.text_input("Enter the vacancy rate (% of rent):   ", value = '5')

st.sidebar.markdown("**Expense_Variables:** ")
#st.sidebar.text("Expense Variables: ") 
property_mgmt = st.sidebar.slider("Property management fee(% of rent):   ", 0, 15, 10)
property_tax = st.sidebar.slider("Property tax rate(% of price):", 0.0, 3.0, 1.5)
#property_tax = st.sidebar.text_input("Enter the tax rate (% of price):   ", value = '1.5')
repairs = st.sidebar.text_input("Enter the maintenance (% of rent):   ", value = '7')
insurance = st.sidebar.text_input("Enter the insurance expense (% of rent):   ", value = '1.5')
utilities = st.sidebar.text_input("Enter the utilities (% of rent):   ", value = '5') 
broker_fee = st.sidebar.text_input("Enter the broker fee (% of rent):   ", value = '0') 
HOA = st.sidebar.text_input("Enter the HOA expense (% of rent):   ", value = '0')



Price = float(Price)
rent_amt = float(rent_amt)
property_mgmt = float(property_mgmt)
property_tax = float(property_tax)
repairs = float(repairs)
vacancy = float(vacancy)
insurance = float(insurance)
utilities = float(utilities)
broker_fee = float(broker_fee)
HOA = float(HOA)
down_payment_percent = float(down_payment_percent)
Annual_Interest_Rate = float(Annual_Interest_Rate)

#listing_notice = price_mine(trial)
listing_notice = Price
mortgage = mortgage_monthly(listing_notice,30,Annual_Interest_Rate,down_payment_percent)

cash = down_payment(listing_notice, down_payment_percent)
net_income = net_operating(Price, rent_amt, property_tax, property_mgmt, repairs, vacancy,insurance
                  , utilities, broker_fee, HOA)
monthly_cash = net_income[8]
cap_return = cap_rate(monthly_cash,listing_notice)
cash_percent = cash_on_cash(monthly_cash,cash)
# net_operating(rent, tax_rate, mortgage_amt, price):

# print("INPUT: ")
# print("The price of: ", listing_notice) 
# print("The monthly rent of : ", rent_amt)
# print("The tax rate of : ", property_tax)
# print("OUTPUTS: ")
# print("Monthly mortgage of  :  ",mortgage)
# print("Net operating income:  ", net_income)
# print("Cap rate of:  ", cap_return," % ")
# print("Cash return rate of:  ", cash_percent, " % ")

#We have to convert the above outputs to streamlit outputs 
st.write('The **monthly cashflow** :sunglasses: is :')
st.write(monthly_cash)
st.write("The **cap rate** is: ")
st.write(cap_return)
st.write("The **cash on cash return rate** is: ")
st.write(cash_percent)

