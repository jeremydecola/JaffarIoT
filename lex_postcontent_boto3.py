import boto3

session = boto3.Session(profile_name='default')
client = session.client('lex-runtime')
ready = False

audiopath = 'C:/Users/Jeremy/Desktop/lex-python-postcontent/capture2.wav'
with open(audiopath, 'rb') as fd:
    audio = fd.read()

# request_text = input("Input: ")
# request_text = request_text.encode("utf-8")

response = client.post_content(
    botName='HelloJaffar',
    botAlias='JaffarTest',
    userId='guest',
    sessionAttributes={
        'string': 'string'
    },
    requestAttributes={
        'string': 'string'
    },
    # AUDIO PCM
    contentType='audio/lpcm; sample-rate=8000; sample-size-bits=16; channel-count=1; is-big-endian=false',
    accept='audio/pcm',
    inputStream=audio
)
# TXT UTF-8
'''
    contentType='text/plain; charset=utf-8',
    accept='text/plain; charset=utf-8',
    inputStream=request_text
'''

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
    if (errorMessage != None):
        print(errorMessage)
    else:
        print('Error' + str(status) + '. Terminating bot.')

