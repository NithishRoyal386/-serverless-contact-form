import json
import boto3

def lambda_handler(event, context):
    try:
        # Get form data from the event
        body = event.get('body', '')
        
        # Parse the form data
        params = {}
        for param in body.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                params[key] = value.replace('+', ' ')
        
        fname   = params.get('fname', '')
        lname   = params.get('lname', '')
        email   = params.get('email', '')
        message = params.get('message', '')
        
        # Basic validation
        if not fname or not lname or not email or not message:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'All fields are required'})
            }
        
        # Send email via SES
        client = boto3.client('ses', region_name='ap-south-2')
        
        client.send_email(
            Source='bandinithishroyal@gmail.com',
            Destination={
                'ToAddresses': ['bandinithishroyal@gmail.com']
            },
            Message={
                'Subject': {
                    'Data': 'New Contact Form Submission'
                },
                'Body': {
                    'Text': {
                        'Data': f'Name: {fname} {lname}\nEmail: {email}\nMessage: {message}'
                    }
                }
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Email sent successfully!'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
