import json
import boto3
import os

bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime')

KNOWLEDGE_BASE_ID = os.getenv('KNOWLEDGE_BASE_ID')
MODEL_ARN = 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-instant-v1'


def handle_warm_up(event, context):
    try:
        # Custom warm-up question
        warm_up_question = "Can I get funding, answer yes or no."

        # Construct the query prompt for the warm-up
        prompt = f"\n\nHuman: {warm_up_question}\nAssistant:"

        # Prepare the base request to Bedrock for the warm-up
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
                                "orAll": [
                                    {"equals": {"key": "hub_id", "value": "all"}},
                                    {"equals": {"key": "hub_id", "value": "305"}}
                                ]
                            },
                            'numberOfResults': 5,
                            'overrideSearchType': 'HYBRID'
                        }
                    },
                    'generationConfiguration': {
                        'inferenceConfig': {
                            'textInferenceConfig': {
                                'maxTokens': 50,
                                'temperature': 0.7,
                                'topP': 0.9
                            }
                        }
                    }
                }
            }
        }

        # Call Bedrock API for the warm-up query
        response = bedrock_agent_runtime_client.retrieve_and_generate(**request_params)

        print("Bedrock warm-up response:", json.dumps(response, default=str))

        # Extract the output text from the response
        response_output = response.get('output', {}).get('text', '').strip()
        if not response_output:
            response_output = "Sorry, no relevant information found for your inquiry."

        return {
            'statusCode': 200,
            'body': json.dumps({
                'warm_up_response': response_output
            }, ensure_ascii=False)
        }

    except Exception as e:
        print(f"Exception in warm-up handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }