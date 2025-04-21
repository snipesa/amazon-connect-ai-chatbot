import json
import boto3

lambda_client = boto3.client('lambda')

def invoke_kb_lambda(query, hub_id, session_id, bedrock_session_id, single_hub, need_funding=None):
    from config import QUERY_KB_FUNCTION

    """Helper function to invoke the knowledge base lambda"""
    payload = {
        "query": query,
        "hub_id": hub_id,
        "session_id": session_id,
        "bedrock_session_id": bedrock_session_id,
        "single_hub": single_hub
    }     
    if need_funding:
        payload["needFunding"] = need_funding
        
    return lambda_client.invoke(
        FunctionName=QUERY_KB_FUNCTION,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )

def yes_no_quick_reply_template():
    """Create the standard quick reply template"""
    return {
        "templateType": "QuickReply",
        "version": "1.0",
        "data": {
            "replyMessage": {
                "title": "Thanks for selecting!"
            },
            "content": {
                "title": "Is there anything else I can help you with?",
                "elements": [
                    {
                        "title": "yes"
                    },
                    {
                        "title": "no"
                    }
                ]
            }
        }
    }