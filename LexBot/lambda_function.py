import json
from integration import *
from prediction_model import *

def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']
    
def get_slot(intent_request, slotName):
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        return slots[slotName]['value']['interpretedValue']
    else:
        return None    

def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']

    return {}

def elicit_intent(intent_request, session_attributes, message):
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitIntent'
            },
            'sessionAttributes': session_attributes
        },
        'messages': [ message ] if message != None else None,
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }


def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }

def practSearch(intent_request):
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)
    
    phone = str(get_slot(intent_request, 'phone'))
    dob = str(get_slot(intent_request, 'dob'))
    
    patient = get_patient_data(phone, dob)
    
    if len(patient)>0:
        
        risk = predict_practitioners(
            patient.glucose
            ,patient.blood_pressure
            ,patient.insulin
            ,patient.bmi
            )
    
        text = "Thank you. Based on what we can see. "+ patient.first_name +" is at "+risk+" risk"
        message =  {
                'contentType': 'PlainText',
                'content': text
            }
            
    else:
        text = "I could not find any records associated with that information. Would you like to enter the datails once again?"
        message =  {
                'contentType': 'PlainText',
                'content': text
            }
        
    fulfillment_state = "Fulfilled"    
    return close(intent_request, session_attributes, fulfillment_state, message)   

def practAsk(intent_request):
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)
    
    glucose = float(get_slot(intent_request, 'glucose'))
    blood_pressure = float(get_slot(intent_request, 'bloodPressure'))
    insulin = float(get_slot(intent_request, 'insulin'))
    bmi = float(get_slot(intent_request, 'bmi'))
        
    risk = predict_practitioners(
        glucose
        ,blood_pressure
        ,insulin
        ,bmi
        )
    
    text = "Thank you. Based on those parameters. The patient is at "+risk+" risk"
    message =  {
            'contentType': 'PlainText',
            'content': text
        }
            
    fulfillment_state = "Fulfilled"    
    return close(intent_request, session_attributes, fulfillment_state, message)

def publicAsk(intent_request):
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)
    
    aboriginal = str(get_slot(intent_request, 'aboriginal'))
    age_group = str(get_slot(intent_request, 'ageGroup'))
    alcohol = str(get_slot(intent_request, 'alcohol'))
    blood_pressure = str(get_slot(intent_request, 'blood_pressure'))
    diet = str(get_slot(intent_request, 'diet'))
    family_history = str(get_slot(intent_request, 'family_history'))
    gender = str(get_slot(intent_request, 'gender'))
    glucose = str(get_slot(intent_request, 'glucose'))
    origin = str(get_slot(intent_request, 'origin'))
    physical_activity = str(get_slot(intent_request, 'physical_activity'))
    smoke = str(get_slot(intent_request, 'smoke'))
    waist = str(get_slot(intent_request, 'waist'))
    
    risk, risk_index = predict_public(
        aboriginal
        ,age_group
        ,alcohol
        ,blood_pressure
        , diet
        , family_history
        , gender
        , glucose
        , origin
        , physical_activity
        , smoke
        , waist
        )
        
    text = "Thank you. Based on the information that you provided. You are at "+risk+" risk. Score: " + str(risk_index)
    message =  {
            'contentType': 'PlainText',
            'content': text
        }
            
    fulfillment_state = "Fulfilled"    
    return close(intent_request, session_attributes, fulfillment_state, message)     
    
def dispatch(intent_request):
    intent_name = intent_request['sessionState']['intent']['name']
    response = None
    # Dispatch to your bot's intent handlers
    if intent_name == 'pract_Search':
        return practSearch(intent_request)
    elif intent_name == 'pract_Ask':
        return practAsk(intent_request)
    elif intent_name == 'public_Ask':
        return publicAsk(intent_request)    

    raise Exception('Intent with name ' + intent_name + ' not supported')

def lambda_handler(event, context):
    response = dispatch(event)
    return response