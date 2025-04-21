def handle_dialog(event, response_session_attributes):
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
