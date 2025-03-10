# Connect Intelligent Entry Chatbot

A smart AI-powered chatbot solution for Amazon Connect that handles common customer inquiries through an intelligent knowledge base before routing to human agents.

## Project Overview

This project implements an intelligent entry system for Amazon Connect contact centers to reduce the load on human agents by automatically answering common customer questions. It leverages:

- **Amazon Lex** for natural language understanding and intent recognition
- **Amazon Bedrock** with Claude for AI-powered responses from a knowledge base
- **Amazon Connect** for contact center integration
- **AWS Lambda** for business logic and integration between services
- **Amazon S3** for knowledge base document storage
- **Amazon DynamoDB** for session and data persistence

## Repository Structure

```
connect-eic-chatbot/
├── DynamoDB/                 # DynamoDB table definitions and setup
├── README.md                 # This documentation
├── bedrock/                  # Bedrock knowledge base configuration
│   └── knowledge-base-INFO   # Knowledge base IDs and configuration
├── contact-center/           # Amazon Connect contact flow configuration
│   └── custom-chat-flow.json # Definition for the contact flow
├── lambda/                   # Lambda functions for bot logic
│   ├── bedrock.py            # Integration with Amazon Bedrock
│   ├── index.py              # Main Lambda handler
│   ├── lex-dialogCodeHook    # Lex dialog code hook handler
│   ├── querry-knowledgeBase  # Knowledge base query handler
│   └── requirements.txt      # Python dependencies
├── lex/                      # Amazon Lex bot definitions
│   ├── QA-Bot-DRAFT-en_US-JOVYLDIWFD-LexJson.zip # Exported Lex bot
│   └── sample-lex-event.json # Sample event for testing
└── widget-site/              # Web chat widget implementation
    ├── index.html            # Example webpage with embedded chat widget
    └── widget.js             # Chat widget customization
```

## How It Works

### Conversation Flow

1. **Initial Contact**: Customer initiates contact through the web chat widget.
2. **Intent Recognition**: Amazon Lex identifies customer intent through natural language understanding.
3. **Direct Responses**: For recognized intents (e.g., "joinHub"), the system elicits required slots (email, lastName).
4. **AI-Powered Responses**: When Lex can't determine the intent (FallbackIntent), the query is routed to the "lambdaBedrock" intent.
5. **Knowledge Base Query**: The original question is sent to Amazon Bedrock, which searches the knowledge base for relevant information.
6. **Automated Response**: The AI-generated response is returned to the customer.
7. **Continuation or Escalation**: The customer can ask additional questions or request a human agent if needed.

### Components

#### Amazon Lex Bot

The Lex bot handles intent recognition with defined intents like:
- `joinHub`: For processing hub membership requests
- `FallbackIntent`: Triggers when no intent matches, redirecting to Bedrock
- `lambdaBedrock`: Handles knowledge base queries 
- `AnythingElseIntent`: Checks if the customer has additional questions

#### Bedrock Knowledge Base

The knowledge base contains documents stored in S3 that provide answers to common questions. It uses:
- Titan embeddings for document vectorization
- Claude Instant for generating natural language responses

#### Lambda Functions

Several Lambda functions handle different aspects of the bot logic:
- Processing Lex intent fulfillment
- Querying the Bedrock knowledge base
- Formatting responses for the chat interface

#### Connect Contact Flow

A custom contact flow defined in `custom-chat-flow.json` manages the chat session, integrates with Lex, and handles routing logic.

#### Web Chat Widget

A customizable web chat widget can be embedded in any webpage to provide access to the bot.

## Setup and Configuration

### Prerequisites

- AWS Account with access to:
  - Amazon Connect
  - Amazon Lex
  - Amazon Bedrock
  - AWS Lambda
  - Amazon S3
  - Amazon DynamoDB

### Knowledge Base Setup

1. Create an S3 bucket for your knowledge base documents
2. Upload your FAQ documents and other reference materials
3. Set up a Bedrock knowledge base pointing to the S3 bucket
4. Update the `knowledge-base-INFO` file with your knowledge base ID and ARN

### Lex Bot Configuration

1. Import the provided Lex bot definition or create a new bot
2. Configure the intents and slots based on your requirements
3. Set up the Lambda function as a dialog code hook

### Lambda Function Deployment

1. Create Lambda functions for each Python file in the `lambda` directory
2. Install dependencies specified in `requirements.txt`
3. Configure environment variables for knowledge base IDs and ARNs

### Connect Contact Flow Setup

1. In your Amazon Connect instance, create a new contact flow
2. Import the `custom-chat-flow.json` or create a flow based on your requirements
3. Associate the Lex bot with your contact flow

### Web Widget Integration

1. Customize the chat widget in `widget.js` as needed
2. Update `index.html` with your unique IDs and snippet IDs
3. Embed the modified code in your website

## Customization

### Adding New Intents

To add new intents to handle specific customer requests:
1. Define the intent in the Lex bot
2. Add corresponding logic in the Lambda dialog code hook
3. Update the contact flow if necessary

### Expanding the Knowledge Base

To improve the AI's ability to answer questions:
1. Add more documents to your S3 bucket
2. Ensure proper metadata for improved search relevance
3. Rebuild or refresh the knowledge base in Bedrock

### Customizing the User Interface

To modify the appearance and behavior of the chat widget:
1. Edit the styles in the `amazon_connect('styles', {...})` section of `index.html`
2. Customize the widget behavior in `widget.js`

## Troubleshooting

### Common Issues

- **Lex not recognizing intents**: Check confidence thresholds and training phrases
- **Knowledge base not returning relevant answers**: Add more documents or improve metadata
- **Lambda function errors**: Check CloudWatch logs for detailed error messages

### Logging and Monitoring

- Enable logging for all components
- Set up CloudWatch dashboards to monitor performance
- Track key metrics like:
  - Intent recognition rate
  - Knowledge base query success rate
  - Agent escalation frequency

## Future Enhancements

Potential improvements for the chatbot:
- Integration with additional data sources
- Multi-language support
- Sentiment analysis for customer interactions
- A/B testing for different response strategies


## Contributors

- Etunyi Ashime (@github.com:snipesa)