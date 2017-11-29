import paho.mqtt.client as mqtt
import time

#Create an array that will act as a database of functions
#Functions are in the form [client_id, action, parameters]
function_db = []

def declareAction(function_db, actor_id, action, parameters):
    function_db.append([actor_id, action, parameters])


def getActions(function_db,requester_id, actor_prefix):
    print("Replying to ID:" + requester_id)
    print("Requesting functions from actors related to IDs with prefix:" + actor_prefix)
    for function in range(len(function_db)):
        reply_message = ""
        prefix_match = False
        for element in range(len(function_db[function])):
            if actor_prefix in function_db[function][0]:
                reply_message += str(function_db[function][element]) + ","
                prefix_match = True
        #serverman_client.publish(client_id, reply_message, qos=2, retain=True)
        if prefix_match == True:
            print(str(function) + ", " + reply_message)

def updateActions(function_db, client_id, client_function_length):
    db_length = len(function_db)
    if client_function_length != db_length:
        for function in range(client_function_length, db_length):
            reply_message = ""
            for element in function_db[function]:
                reply_message += str(function_db[function][element]) + ","
        serverman_client.publish(client_id, reply_message, qos=2, retain=True)

#This is used to callback
def on_message(client, userdata, message):
    request_message = str(message.payload.decode("utf-8"))
    topic = message.topic
    quality_of_service = message.qos
    retain_message = message.retain

    ##########################################################
    ######       Examples of an incoming messages:      ######
    ###### declareAction_clientID_action_param1_param2  ######
    ######          getActions_clientID_door1           ######
    ##########################################################

    # Split incoming payload into function elements
    function_elements = request_message.split("_")
    request_type = function_elements[0]
    actor_client_id = function_elements[1]
    # for a declare request_type
    request_action = function_elements[2]
    # for a get request_type
    requested_client_id = function_elements[2]

    if len(function_elements) >= 3:
        request_parameters = function_elements[3:]

    if "declareAction" in request_type:
        declareAction(function_db, actor_client_id, request_action, request_parameters)
    elif "getActions" in request_type:
        getActions(function_db, actor_client_id, requested_client_id)

    #Display incoming message
    print("message received ", request_message)
    print("message topic=", topic)
    print("message qos=", quality_of_service)
    print("message retain flag=", retain_message)

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