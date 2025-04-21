import json
import boto3
import os

bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime')

KNOWLEDGE_BASE_ID = os.getenv('KNOWLEDGE_BASE_ID')
MODEL_ARN = 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-instant-v1'

def handle_query(event, context):
    try:
        # Extract query, session and hub from event payload
        query = event.get("query")
        hub_id = event.get("hub_id")
        session_id = event.get("session_id")
        bedrock_session_id = event.get("bedrock_session_id")
        
        if not query:
            raise Exception("No query provided in the event")
        if not hub_id:
            raise Exception("No hub_id provided in the event")

        # Construct the query prompt with modified instructions for funding intent
        prompt = f"\n\nHuman: Please answer the following question appropriately related to assistance needed in funding a business in their area.\nQuestion: {query}\nAssistant:"

        # Prepare the base request to Bedrock
        request_params = {
            'input': {'text': prompt},
            'retrieveAndGenerateConfiguration': {
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': KNOWLEDGE_BASE_ID,
                    'modelArn': MODEL_ARN,
                    'retrievalConfiguration': {
                        'vectorSearchConfiguration': {
                            'filter': {
                                "equals": {"key": "hub_id", "value": hub_id}
                            },
                            'numberOfResults': 5,
                            'overrideSearchType': 'HYBRID'
                        }
                    },
                    'generationConfiguration': {
                        'inferenceConfig': {
                            'textInferenceConfig': {
                                'maxTokens': 500,
                                'temperature': 0.7,
                                'topP': 0.9
                            }
                        }
                    }
                }
            }
        }
        
        # Add sessionId only if it exists (for subsequent calls)
        if bedrock_session_id:
            request_params['sessionId'] = bedrock_session_id
            
        # Call Bedrock API
        response = bedrock_agent_runtime_client.retrieve_and_generate(**request_params)

        # Log the full response for debugging
        print("Bedrock response:", json.dumps(response, default=str))

        # Extract the Bedrock sessionId from the response to use in subsequent calls
        bedrock_session_id = response.get('sessionId')

        # Extract response content
        response_output = response.get('output', {}).get('text', '').strip()
        if not response_output:
            response_output = "Sorry, no relevant information found for your inquiry about business funding."
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'tips': response_output,
                'bedrock_session_id': bedrock_session_id
            }, ensure_ascii=False)
        }

    except Exception as e:
        print(f"Exception in queryNeedFundingIntent: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }