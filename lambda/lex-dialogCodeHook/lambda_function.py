import json

from intents import fallback, need_funding, qa_auto_reply, anything_else

def lambda_handler(event, context):
    # Handle warm-up requests
    if event.get('reason') == 'warm_up':
        return {
            'statusCode': 200,
            'body': json.dumps('Warm-up completed successfully.')
        }
    
    intent = event['sessionState']['intent']['name']
    response_session_attributes = event['sessionState'].get('sessionAttributes', {})
    invocation_source = event['invocationSource']
    
    # Route based on intent type and invocation source
    if intent == 'FallbackIntent':
            return fallback.handle_dialog(event, response_session_attributes)

    elif intent == 'needFunding':
        if invocation_source == 'DialogCodeHook':
            return need_funding.handle_dialog(event, response_session_attributes)
        else:  # FulfillmentCodeHook
            return need_funding.handle_fulfillment(event, response_session_attributes)
    
    elif intent == 'QA_AutoReply':
        if invocation_source == 'DialogCodeHook':
            # Ensure original question is captured
            if 'original_question' not in response_session_attributes:
                response_session_attributes['original_question'] = event.get('inputTranscript', '')
            return qa_auto_reply.handle_dialog(event, response_session_attributes)
        else:  # FulfillmentCodeHook
            return qa_auto_reply.handle_fulfillment(event, response_session_attributes)
    
    elif intent == 'AnythingElseIntent':
        if invocation_source == 'DialogCodeHook':
            return anything_else.handle_dialog(event, response_session_attributes)
        else:  # FulfillmentCodeHook
            return anything_else.handle_fulfillment(event, response_session_attributes)
    
    # Default handling for any other intents
    if invocation_source == 'DialogCodeHook':
        # Ensure original question is captured
        if 'original_question' not in response_session_attributes:
            response_session_attributes['original_question'] = event.get('inputTranscript', '')
        
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Delegate"
                },
                "intent": {
                    "name": intent,
                    "slots": event['sessionState']['intent'].get('slots', {})
                },
                "sessionAttributes": response_session_attributes
            }
        }
    else:
        # Unexpected case - fallback response
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "slots": event['sessionState']['intent'].get('slots', {}),
                    "state": "Failed"
                },
                "sessionAttributes": response_session_attributes
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Sorry, I encountered an unexpected error."
                }
            ]
        }