import json
import boto3
lambda_client = boto3.client('lambda')
emails = ['etunyiashime@gmail.com', 'etunyiashime@eicatalyst.com', 'test@gmail.com']
lastNames = ['danny', 'etu', 'lana']

def validate_joinhub(slots):
    # validate lastnames
    if not slots['lastName']:
        print('lastName slot is invalid')
        return {
            'isValid': False,
            'invalidSlot': 'lastName'
        }

    if slots['lastName']['value']['originalValue'].lower() not in lastNames:
        print('lastName not in files')
        return {
            'isValid': False,
            'invalidSlot': 'lastName',
            'message': 'Please enter a valid last name'
        }

    # validate emailAddress
    if not slots['emailAddress']:
        print('emailAddress slot is invalid')
        return {
            'isValid': False,
            'invalidSlot': 'emailAddress'
        }

    if slots['emailAddress']['value']['originalValue'].lower() not in emails:
        print('emailAddress not in files')
        return {
            'isValid': False,
            'invalidSlot': 'emailAddress',
            'message': 'Please enter a valid email'
        }
    # Valid request
    return {
        'isValid': True
    }

def qa_autoReply(slots):
    # Example validation logic for lambdaBedrock intent
    if not slots['emailAddress']:
        return {
            'isValid': False,
            'invalidSlot': 'emailAddress'
        }

    if slots['emailAddress']['value']['originalValue'].lower() not in emails:
        return {
            'isValid': False,
            'invalidSlot': 'emailAddress',
            'message': 'Please input a valid email'
        }

    return {
        'isValid': True
    }

# Update the intent mappings to match exact Lex intent names
VALIDATION_FUNCTIONS = {
    'joinHub': validate_joinhub, 
    'lambdaBedrock': qa_autoReply,
}

FULFILLMENT_MESSAGES = {
    'joinHub': lambda slots: f"A case will be created for {slots['lastName']['value']['originalValue']}",
    'lambdaBedrock': lambda slots: f"Creating a {slots['priority']['value']['originalValue']} priority {slots['category']['value']['originalValue']} lambdaBedrock ticket"
}

def lambda_handler(event, context):
    print(event)
    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    response_session_attributes = event['sessionState'].get('sessionAttributes', {})

    # get appropriate  validation for the given intent
    if intent == 'FallbackIntent':
        # transfer to lambdaBedrock intent
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "ConfirmIntent"
                },
                "intent": {
                    "name": "lambdaBedrock",
                    "slots": {},
                    "state": "InProgress"
                },
                "sessionAttributes": {
                    "original_question": event['inputTranscript']
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Give me a moment!"
                }
            ]
        }
        return response
    else:
        validate_function = VALIDATION_FUNCTIONS.get(intent)
        if not validate_function:
            raise Exception(f"no validation function found for intent: {intent}")
        validation_result = validate_function(slots)



    if event['invocationSource'] == 'DialogCodeHook':
        # only update session attributes if they are empty
        if not response_session_attributes:
            response_session_attributes = {
                'original_question': event['inputTranscript']
            }

        if not validation_result['isValid']:
            if 'message' in validation_result:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        },
                        "sessionAttributes": response_session_attributes
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": validation_result['message']
                        }
                    ]
                }
            else: 
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        },
                        "sessionAttributes": response_session_attributes
                    }
                }
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        "name": intent,
                        "slots": slots
                    },
                    "sessionAttributes": response_session_attributes
                }
            }                
    
    elif event['invocationSource'] == 'FulfillmentCodeHook':
        # original question from session attributes
        original_question = event['sessionState'].get('sessionAttributes', {}).get('original_question', '')

        # Get the appropriate fulfillment message for the intent
        if intent == 'lambdaBedrock':
            # call the bedrock knowledge base lambda function
            knowledge_base_response = lambda_client.invoke(
                FunctionName='lexBedrockKnowlegeIntergration',
                InvocationType='RequestResponse',
                Payload=json.dumps({
                    "query": original_question 
                })
            )
            knowledge_base_result = json.loads(knowledge_base_response['Payload'].read())
            tips = json.loads(knowledge_base_result['body']).get('tips', 'Sorry we do not have available data for your inquiry.')
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        "name": intent,
                        "slots": slots,
                        "state": "Fulfilled"
                    },
                    "sessionAttributes": response_session_attributes
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": tips
                    }
                ]
            }


        else:
        
            fulfillment_message = FULFILLMENT_MESSAGES.get(intent)
            if not fulfillment_message:
                raise Exception(f"No fulfillment message found for intent: {intent}")
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        "name": intent,
                        "slots": slots,
                        "state": "Fulfilled"
                    },
                    "sessionAttributes": response_session_attributes                    
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": fulfillment_message(slots)
                    }
                ]
            }

    print(response)    
    return response

