import paho.mqtt.client as mqtt
import time

#Create an array that will act as a database of functions
#Functions are in the form [client_id, action, parameters]
function_db = []

#This is used to callback
def on_message(client, userdata, message):
    request_message = str(message.payload.decode("utf-8"))
    topic = message.topic
    quality_of_service = message.qos
    retain_message = message.retain
    print("message received ", request_message)
    print("message topic=", topic)
    print("message qos=", quality_of_service)
    print("message retain flag=", retain_message)

def declareAction(function_db, client_id, action, parameters):
    function_db.append([client_id, action, parameters])

def getActions(client_id, function_db, client_prefix):
    reply_message = ""
    for function in function_db:
        for element in function:
            if client_prefix in function_db[function][0]:
                reply_message += element + ","
        serverman_client.publish(client_id, reply_message, qos=2, retain=True)

def updateActions(client_id, function_db, client_function_length):
    reply_message =''
    db_length = len(function_db)
    if client_function_length != db_length:
        for function in range(client_function_length, db_length):
            for element in function:
                reply_message += element + ","
        serverman_client.publish(client_id, reply_message, qos=2, retain=True)

#Broker Address
broker_address = "ec2-34-207-65-122.compute-1.amazonaws.com"

#Instantiate Server Manifest Client
serverman_client = mqtt.Client(client_id="serverman", clean_session=True, userdata=None, protocol= mqtt.MQTTv311, transport="tcp")
serverman_client.on_message=on_message # attach function to callback

#Connect to the MOSQUITTO on EC2 instance
serverman_client.username_pw_set("ubuntu", password=None)
serverman_client.connect(broker_address, 1883, 60)
serverman_client.loop_start() # start loop to stay connected

#Subscribe to 'test' topic with QOS of 2
serverman_client.subscribe("serverman", qos=2)
#serverman_client.subscribe("lobby", qos=2)

time.sleep(4) # wait
serverman_client.loop_stop() #stop the loop


