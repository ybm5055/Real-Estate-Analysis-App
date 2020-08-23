# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 01:05:50 2020

@author: Boming
"""

import requests
from requests import get
import pandas as pd
import itertools
import streamlit as st
import numpy as np


#Takes Monthly Rent and Expense Variables to calculate the Net Operating Income
def net_operating(price, rent, tax_rate, property_mgmt, repairs, vacancy,insurance
                  , utilities, broker_fee, HOA):
    #Expense Variables
    mortgage_amt = mortgage_monthly(price,30,Annual_Interest_Rate,down_payment_percent)
    prop_managment = rent * (property_mgmt/100)
    prop_tax = (price * (tax_rate/100)/12)
    prop_repairs = rent*repairs/100
    vacancy = rent*vacancy/100
    utilities = rent * utilities/100
    broker_fee = rent * broker_fee/100
    HOA = rent * HOA/100
    insurance = rent * insurance/100
    
    net_income = round(rent - prop_managment - prop_tax - prop_repairs - vacancy - mortgage_amt - utilities - insurance - broker_fee - HOA,2)
    #Summary
    output = [prop_managment, prop_tax, prop_repairs, insurance ,vacancy, utilities, broker_fee, HOA,net_income]
  
    
    return output

# Create function to calculate the downpayment amount
def down_payment(price,down_payment_percent):
    amt_down = price*down_payment_percent/100
    return(amt_down)

#Create function to calculate the monthly mortgage payment
def mortgage_monthly(price,years,Annual_Interest_Rate,down_payment_percent):
    
    #formula used: M = P [ i(1 + i)^n ] / [ (1 + i)^n – 1]
    down = down_payment(price,down_payment_percent)
    loan = price - down
    months = years*12
    interest_monthly = (Annual_Interest_Rate/100)/12
    payment =  np.pmt(interest_monthly, months, loan)
    
    
    return(-payment)

#test_number = mortgage_monthly(125000,30,3.5,20)
    
# Create Cap Rate function which is simply NOI/Price    
def cap_rate(monthly_income, price):
    cap_rate = round(((monthly_income*12) / price)*100,2)
    
    return cap_rate

#COC Return which is simply Annual Cash FLOW/how much money down
def cash_on_cash(monthly_income, down_payment):
    cash_return = round(((monthly_income*12)/down_payment)*100,2)
    
    return cash_return

 #Streamlit UI 
st.title('Real Estate Investment Analysis App')

#Add an overview
text = """
    ## Overview: ##
    ---------------------
    This App was created because the author was bored of using his excel model for a real estate deal analysis one day, and decided to spend hours on creating an app with streamlit for the first time instead :upside_down_face:\n
    He did think it was a fun experience and streamlit is pretty cool.\n
    If you are a real estate investor and want to take a break from the spreadsheets, feel free to use this for a simple and quick analysis on the COC return and Cap Rate by entering the variables below :point_down:\n
    ---------------------
    """
st.sidebar.markdown(text)

#insert image cuz we don't like too much white space
from PIL import Image
import requests
from io import BytesIO

response = requests.get('https://www.nsaen.com/wp-content/uploads/2018/07/building-wealth.jpg')
img = Image.open(BytesIO(response.content))
st.image(img,use_column_width=True)

st.subheader("Return Metrics")

st.sidebar.subheader("Purchase Info: ")         

Price = st.sidebar.text_input(label = "Enter the Purchase Price: ",value ='100000' )#value = trial if trial is not None else '100000')
down_payment_percent = st.sidebar.slider("Enter the Down Payment Rate (% of purchase price):   ", 0,100,20)
Annual_Interest_Rate = st.sidebar.text_input("Enter the Annual Interest Rate (%):   ", value = '3.5')

st.sidebar.subheader("Revenue Variables: ")
#st.sidebar.text("Revenue Variables: ") 
rent_amt = st.sidebar.text_input("Enter the monthly rent price:   ", value = '1000')
vacancy = st.sidebar.text_input("Enter the vacancy rate (% of rent):   ", value = '5')

st.sidebar.subheader("Expense Variables: ")
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

listing_notice = Price
mortgage = mortgage_monthly(listing_notice,30,Annual_Interest_Rate,down_payment_percent)

cash = down_payment(listing_notice, down_payment_percent)
net_income = net_operating(Price, rent_amt, property_tax, property_mgmt, repairs, vacancy,insurance
                  , utilities, broker_fee, HOA)
monthly_cash = net_income[8]
cap_return = cap_rate(monthly_cash,listing_notice)
cash_percent = cash_on_cash(monthly_cash,cash)

#Display the return outputs in Streamlit 
st.write('The **monthly cashflow** :sunglasses: is :')
st.write(monthly_cash)
st.write("The **cap rate** is: ")
st.write(cap_return)
st.write("The **cash on cash return rate** is: ")
st.write(cash_percent)

st.sidebar.subheader("About Author")
text = """\
   - Name: Brian Yu
   - Occupation: Analytics Consultant
   - Interests: Investing, data analysis and fitness
   - [**Linkedin**](https://www.linkedin.com/in/brian-boming-yu-00206994/) \n
   **Thanks for checking this out!**
      """
st.sidebar.markdown(text)
