import boto3

session = boto3.Session(profile_name='default')
client = session.client('lex-runtime')
ready = False

while not ready:
    request_text = input("Input: ")

    response = client.post_text(
        botName='HelloJaffar',
        botAlias='JaffarTest',
        userId='guest_test',
        sessionAttributes={
            'string': 'string'
        },
        requestAttributes={
            'string': 'string'
        },
        inputText=request_text
    )

    metaData = response.get('ResponseMetadata')
    status = metaData.get('HTTPStatusCode')

    if status == 200:
        dialogState = response['dialogState']
        if dialogState.startswith('Elicit'):
            print(response['message'])
        elif dialogState.startswith('Ready'):
            print('ReadyForFulfillment')
            print('Intent:' + response['intentName'])
            ready = True

    else:
        errorMessage = response['message']
        if(errorMessage != None):
            print(errorMessage)
        else:
            print('Error' + str(status) +'. Terminating bot.')

print('Bye bye!')
