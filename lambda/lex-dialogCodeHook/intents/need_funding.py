def handle_dialog(event, response_session_attributes):
    """Handle needFunding intent at dialog stage
    
        NB the original question gotten from the session attributes will be correct only if they are no slots
        Reason being it will give a wrong value for the original question from input transcript below
    """
    response_session_attributes['needFunding'] = 'yes'
    if 'original_question' not in response_session_attributes:
        response_session_attributes['original_question'] = event.get('inputTranscript', '')
    
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Delegate"
            },
            "intent": {
                "name": "QA_AutoReply",
                "slots": {},
                "state": "ReadyForFulfillment"
            },
            "sessionAttributes": response_session_attributes
        }
    }

def handle_fulfillment(event, response_session_attributes):
    """Handle needFunding intent at fulfillment stage"""
    response_session_attributes['needFunding'] = 'yes'
    if 'original_question' not in response_session_attributes:
        response_session_attributes['original_question'] = event.get('inputTranscript', '')
    
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Delegate"
            },
            "intent": {
                "name": "QA_AutoReply",
                "slots": {},
                "state": "ReadyForFulfillment"
            },
            "sessionAttributes": response_session_attributes
        }
    }