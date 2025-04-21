import json
import os
import queryGenKB
import querySingleKB
import queryNeedFundingIntent
import warm_up_handler 

def lambda_handler(event, context):
    # Handle warm-up requests
    if event.get('reason') == 'warm_up':
        return warm_up_handler.handle_warm_up(event, context) 
    
    try:
        print("Received event:", json.dumps(event, indent=2))

        needFunding = event.get("needFunding", "")
        single_hub = event.get("single_hub", "no").lower()
        
        # Route to the appropriate handler based on the intent and single_hub flag
        if needFunding == "yes":
            return queryNeedFundingIntent.handle_query(event, context)
        elif single_hub == "yes":
            return querySingleKB.handle_query(event, context)
        else:
            return queryGenKB.handle_query(event, context)
            
    except Exception as e:
        print(f"Exception in main handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }