import pandas as pd
import random
import decimal 

def random_num():
    return(decimal.Decimal(random.randrange(100, 200)))

def predict_practitioners(glucose, blood_pressure, insulin, bmi):
    '''
    Predicts results based on Practitioners data
    '''
    
     ## YOUR REAL MODEL HERE
    
    
    ## TESTING SAMPLE
    
    
    risk_index = 0
    risk = 'LOW'
    
    if glucose>90:
        risk_index += 200
    
    if bmi>25:
        risk_index += 100
        
    risk_index += random_num()
        
    if (risk_index>300):
        risk = 'HIGH'
    
    return risk

def predict_public(aboriginal, age_group, alcohol, blood_pressure, diet, family_history, gender, glucose, origin, physical_activity, smoke, waist):
    '''
    Predicts results based on Life Style Habits
    '''
    
    ## YOUR REAL MODEL HERE
    
    
    ## TESTING SAMPLE
    
    risk_index = 0
    risk = 'LOW'
    
    if age_group == '45-54' or age_group == '55-64' or age_group == '65-99':
        risk_index += 100
    
    if gender == 'female':
        risk_index += 100
    
    if aboriginal == 'No':
        risk_index += 100
    
    if origin == 'australia' or origin == 'other' :
        risk_index += 100
    
    if family_history == 'yes':
        risk_index += 300
    
    if glucose == 'yes':
        risk_index += 300
    
    if blood_pressure == 'yes':
        risk_index += 200
    
    if smoke == 'yes':
        risk_index += 200
    
    if diet == 'no':
        risk_index += 200
    
    if physical_activity == 'no':
        risk_index += 200
        
    if alcohol == 'daily':
        risk_index += 300
    
    if alcohol == 'weekly':
        risk_index += 200
    
    if alcohol == 'monthly':
        risk_index += 100
    
    if (risk_index>700):
        risk = 'HIGH'
    
    return risk, risk_index
    
