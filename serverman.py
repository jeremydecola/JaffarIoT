import paho.mqtt.client as mqtt
import time

#Create a dictionairy to store messages


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

def declareAction(request_dictionary, client_id, action, parameters):
    request_dictionary[client_id] = {}
    for i in range(len(parameters)):
        request_dictionary[client_id][action] = parameters[i]

def getActionAll(client_id, request_dictionary):
    for key, value in request_dictionary.items():
        reply_message = str(key) + "," + str(value)
        serverman_client.publish(client_id, reply_message, qos=2, retain=True)

def getActionRange(client_id, request_dictionary, a, b):
    for




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


