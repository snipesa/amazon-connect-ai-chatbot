def handle_dialog(event, response_session_attributes):
    """Handle AnythingElseIntent at dialog stage"""
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Delegate"
            },
            "intent": {
                "name": "AnythingElseIntent",
                "slots": event['sessionState']['intent'].get('slots', {}),
                "state": "InProgress"
            },
            "sessionAttributes": response_session_attributes
        }
    }

def handle_fulfillment(event, response_session_attributes):
    """Handle AnythingElseIntent at fulfillment stage"""
    slots = event['sessionState']['intent'].get('slots', {})
    
    yes_no_value = None
    if 'yesNoSlot' in slots and slots['yesNoSlot'] is not None:
        if 'value' in slots['yesNoSlot'] and 'interpretedValue' in slots['yesNoSlot']['value']:
            yes_no_value = slots['yesNoSlot']['value']['interpretedValue'].lower()
    
    if yes_no_value == 'yes':
        # If the user wants to ask another question, reset the original_question
        response_session_attributes['original_question'] = ''
        response_session_attributes['yesNoSlot'] = 'yes'
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitIntent"
                },
                "intent": {
                    "name": "QA_AutoReply",
                    "state": "InProgress"
                },
                "sessionAttributes": response_session_attributes
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "What else would you like to ask about?"
                }
            ]
        }
    else:
        # If the user doesn't have more questions, save 'no' and close the conversation
        response_session_attributes['yesNoSlot'] = 'no'
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": "AnythingElseIntent",
                    "slots": slots,
                    "state": "Fulfilled"
                },
                "sessionAttributes": response_session_attributes
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Thank you for using our service!"
                }
            ]
        }