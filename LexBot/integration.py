# Getting data from practitioners
import pandas as pd
import requests as requests
import json
import os

def get_dataset():
    '''
    This function returns the Practitioners data from JotForms
    '''
    
    
    ##  YOUR REAL FORM HERE
    form_id = '212878443002856'
    
    ## PLEASE INCLUDE YOU API KEY IN THE ENVIRONMENT VARIABLES
    api_key = os.environ['JOTFORMS_API_KEY']

    #Practitioners Froms
    url = f"https://api.jotform.com/form/{form_id}/submissions?apiKey={api_key}"

    response_data = requests.get(url).json()
    submissions = response_data['content']

    number_of_submissions = len(submissions)

    if number_of_submissions > 0:
        number_of_questions = len(response_data['content'][0]['answers'])
    
    data = []
    response = {}

    for submission in submissions:
        
        submission_id = submission['id']
        form_id = submission['form_id']
        created_at = submission['created_at']
        
        first_name = submission['answers'].get('3').get('answer').get('first')
        last_name = submission['answers'].get('3').get('answer').get('last')
        dob = submission['answers'].get('16').get('prettyFormat')
        phone = submission['answers'].get('4').get('prettyFormat')
        glucose = submission['answers'].get('17').get('answer')
        blood_pressure = submission['answers'].get('18').get('answer')
        skin_thickness = submission['answers'].get('19').get('answer')
        insulin = submission['answers'].get('20').get('answer')
        bmi = submission['answers'].get('21').get('answer')

        response = {
            'submission_id': submission_id
            , 'form_id': form_id
            , 'created_at': created_at
            , 'first_name': first_name
            , 'last_name': last_name
            , 'phone': phone.replace(' ','')
            , 'dob': dob
            , 'glucose': float(glucose)
            , 'blood_pressure': float(blood_pressure)
            , "skin_thickness": float(skin_thickness)
            , 'insulin': float(insulin)
            , 'bmi':float(bmi)
        }

        data.append(response)

    data_df = pd.DataFrame(data)    
    return data_df  

def get_patient_data(phone, dob):
    '''
    Get a particular record from pracitioneres data
    '''
    
    data = get_dataset()
    patient = pd.DataFrame(data[(data["phone"] == phone) & (data["dob"] == dob)])

    if len(patient)>0:
        patient = patient.iloc[0]
    
    return patient