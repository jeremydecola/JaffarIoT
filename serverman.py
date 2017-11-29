import paho.mqtt.client as mqtt
import time

#This is used to callback
def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

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
serverman_client.subscribe("server/test", qos=2)

#Publish the payload "ON" to 'test' topic with a QOS of 2 and retain value
serverman_client.publish("server/test","ON", qos=2, retain=True)

time.sleep(4) # wait
serverman_client.loop_stop() #stop the loop


