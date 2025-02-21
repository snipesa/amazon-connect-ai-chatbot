import json
import boto3

bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime')

def lambda_handler(event, context):
    try:

        print("Received event:", json.dumps(event, indent=2))
        
        # Extract the query from the event
        query = event.get("query")
        
        if not query:
            raise Exception("No query provided in the event")        
        # Define the Knowledge Base ID and Model ARN
        knowledge_base_id = 'XGGCBXWWIE'
        model_arn = 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-instant-v1'
        
        # Define the prompt
        prompt = f"""\n\nHuman: Please answer the following question appropriately and concise.
        Question: {query}
        Assistant: 
        """
        

        response = bedrock_agent_runtime_client.retrieve_and_generate(
            input={
                'text': prompt,
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': knowledge_base_id,
                    'modelArn': model_arn,
                }
            }
        )
        
        print("Received response:", json.dumps(response, ensure_ascii=False))
        
        # Extract the response content
        response_output = response['output']['text']
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'tips': response_output
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        print(f"Exception: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }