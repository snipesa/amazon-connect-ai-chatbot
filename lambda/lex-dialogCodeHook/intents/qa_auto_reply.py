import json
from utils.helpers import invoke_kb_lambda, yes_no_quick_reply_template
from config import SINGLE_HUB_IDS

def handle_dialog(event, response_session_attributes):
    """Handle QA_AutoReply intent at dialog stage"""
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
    """Handle QA_AutoReply intent at fulfillment stage"""
    try:
        original_question = response_session_attributes.get('original_question', '')
        hub_id = response_session_attributes.get('hub_id', '')
        session_id = response_session_attributes.get('session_id', '')
        bedrock_session_id = response_session_attributes.get('bedrock_session_id', '')
        need_funding = response_session_attributes.get('needFunding', '')
        
        single_hub = "yes" if hub_id in SINGLE_HUB_IDS else "no"
        
        # Call the knowledge base lambda function
        knowledge_base_response = invoke_kb_lambda(
            original_question, hub_id, session_id, 
            bedrock_session_id, single_hub, need_funding
        )
        
        knowledge_base_result = json.loads(knowledge_base_response['Payload'].read())
        tips = json.loads(knowledge_base_result['body']).get('tips', 
                        'Sorry, we do not have available data for your inquiry.')
        bedrock_session_id = json.loads(knowledge_base_result['body']).get('bedrock_session_id', '')
        response_session_attributes['bedrock_session_id'] = bedrock_session_id
        
        # Remove the needFunding parameter after use
        if 'needFunding' in response_session_attributes:
            del response_session_attributes['needFunding']

        # After answering, transition to AnythingElseIntent with interactive message
        quick_reply_template = yes_no_quick_reply_template()
        
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "yesNoSlot"
                },
                "intent": {
                    "name": 'AnythingElseIntent',
                    "slots": {
                        "yesNoSlot": None
                    },
                    "state": "InProgress"
                },
                "sessionAttributes": response_session_attributes
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": tips
                },
                {
                    "contentType": "CustomPayload",
                    "content": json.dumps(quick_reply_template)
                }
            ]
        }
            
    except Exception as e:
        print(f"Error calling knowledge base: {str(e)}")
        # Return a fallback response
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": "QA_AutoReply",
                    "slots": {},
                    "state": "Failed"
                },
                "sessionAttributes": response_session_attributes
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "I'm sorry, I encountered an error processing your request."
                }
            ]
        }