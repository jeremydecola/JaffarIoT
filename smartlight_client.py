import paho.mqtt.client as mqtt
import time

current_state = False
client_name = "smartlight"
updated_id = "" # A copy of the id assigned by lobby for disconnect callback

def on_message(client, userdata, message):
    request_message = str(message.payload.decode("utf-8"))
    topic = message.topic
    quality_of_service = message.qos
    retain_message = message.retain
    # Display incoming message
    #print("message received ", request_message)
    #print("message topic=", topic)
    #print("message qos=", quality_of_service)
    #print("message retain flag=", retain_message)

    if topic == "lobby":
        assigned_id = request_message
        updated_id = assigned_id
        smartlight_client.subscribe(assigned_id, qos=2)
        smartlight_client.unsubscribe("lobby")

        print("Declaring Actions")
        actions = []
        actions.append("toggleLight")
        actions.append("getCurrentState")
        for action in range(len(actions)):
            message = str(("declareAction_" + assigned_id + "_" + actions[action]))
            smartlight_client.publish("serverman", message , qos=2, retain=True)
            print("declared an action")
        return updated_id
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection Successful.")
    elif rc == 1:
        print("Connection Refused - Incorrect Protocol Version.")
    elif rc == 2:
        print("Connection Refused - Invalid Client Identifier.")
    elif rc == 3:
        print("Connection Refused - Server Unavailable.")
    elif rc == 4:
        print("Connection Refused - Bad Username or Password.")
    elif rc == 5:
        print("Connection Refused - Not Authorized.")

    print("Requesting Unique ID")
    smartlight_client.publish("serverman", ("getID_" + client_name), qos=2, retain=True)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnection.")
    smartlight_client.publish("serverman", ("removeActions_" + updated_id), qos=2, retain=True)
    print("Successfully Disconnected")


def toggleLight(current_state):
    print("light toggled")
    current_state = not current_state
    return current_state

def getCurrentState():
    print(current_state)
    return current_state

#Broker Address
broker_address = "ec2-34-207-65-122.compute-1.amazonaws.com"

#Instantiate SmartLight Client
smartlight_client = mqtt.Client(client_id="smartlight", clean_session=True, userdata=None, protocol= mqtt.MQTTv311, transport="tcp")
smartlight_client.on_message=on_message # attach function to callback on message reception
smartlight_client.on_connect=on_connect # attach function to callback on connection

#Connect to the MOSQUITTO on EC2 instance
smartlight_client.username_pw_set("ubuntu", password=None)
smartlight_client.connect(broker_address, 1883, 60)

#Start loop to stay connected
smartlight_client.loop_start()
#smartlight_client.loop_forever()

#Subscribe to 'test' topic with QOS of 2
smartlight_client.subscribe("lobby", qos=2)
print("Subscribed to Lobby")

time.sleep(5000) # wait
smartlight_client.loop_stop() #stop the loop
# smartlight_client.disconnect() #run on_disconnect