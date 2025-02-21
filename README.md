AWS Bedrock + Lex AI Chatbot with Knowledge Base Integration

Overview

This repository contains an AI-powered chatbot leveraging AWS Bedrock and Amazon Lex to provide automated responses based on a knowledge base stored in Amazon S3.

How It Works
	1.	User interacts with Amazon Lex via an AWS Connect flow.
	2.	If the user’s query matches:
        •	joinHub Intent: Validates user email and last name before proceeding.
        •	lambdaBedrock Intent: Queries the knowledge base via AWS Bedrock.
        •	FallbackIntent: If no predefined response is found, queries Claude AI via Bedrock.
	3.	Bedrock responds based on retrieved data from the Knowledge Base.
	4.	AWS Lambda handles logic, validation, and fulfillment.


==================================================================================================================================    


    Architecture

==================================================================================================================================    





Setup Instructions

1. AWS Bedrock Knowledge Base
	1.	Upload your knowledge base to Amazon S3
	•	Store documents in a dedicated S3 bucket (e.g., bedrock-knowledge-store).
	•	Ensure the IAM role has read permissions (s3:GetObject).
	2.	Create an Amazon Bedrock Knowledge Base
	•	Navigate to AWS Bedrock Console → Knowledge Base.
	•	Select Amazon Titan Embeddings for indexing.
	•	Point to your S3 bucket as the data source.


==================================================================================================================================    
2. Amazon Lex Setup
	1.	Create a Lex V2 bot (e.g., DevFAQsBot).
	2.	Define Intents:
	•	joinHub → Validates user email and last name.
	•	lambdaBedrock → Queries AWS Bedrock for responses.
	•	FallbackIntent → Triggers Bedrock query when no match is found.
	3.	Configure Lambda Function in Lex:
	•	Attach lex_handler.py as the Lambda function for fulfillment.
	•	Set FallbackIntent to redirect to lambdaBedrock.




==================================================================================================================================    

	3.	Configure Lambda Function in Lex:
	•	Attach lex_handler.py as the Lambda function for dialod and fulfillment.

        Deploy index.py (Main Lex Handler)
        ls lambda/lex-dialogCodeHook/index.py




	•	Set second function to  to querry the knowledge base

        ls lambda/querry-knowledgeBase/index.py


==================================================================================================================================    

4. Amazon Connect Contact Flow
	1.	Import the JSON file contact_flow.json into Amazon Connect.
	2.	Set Lex bot alias to DevFAQsBot.
	3.	Link to your Amazon Lex bot inside the contact flow.


==================================================================================================================================

    Usage Example

1️⃣ User Queries via Amazon Lex
User: "How do I access surveys in Startup Space?"
Bot: "Give me a moment!" (Triggers Bedrock query)
Claude Instant: "To access surveys, navigate to 'My Community' → 'Surveys' → 'Surveys I Can Take'."


2️⃣ Invalid Email Validation
User: "Join the Startup Hub"
Bot: "Please enter your email address."
User: "invalid@email.com"
Bot: "Please enter a valid email."
==================================================================================================================================


Troubleshooting

403 Bedrock Access Error	Ensure IAM role has bedrock:InvokeModel permissions.
Lex Not Triggering FallbackIntent	Confirm intent transitions in Lex console.
Lambda Execution Fails	Check CloudWatch logs (aws logs tail /aws/lambda/lexHandler --follow).


Contributors
	•	Etunyi Ashime (@github.com:snipesa)