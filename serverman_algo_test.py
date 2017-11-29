
function_db = []

request_1 = "declareAction_kitchen/toaster_start-toast_time_intensity"
request_2 = "declareAction_kitchen/light1_on_intensity"
request_3 = "declareAction_hallway/light2_on_intensity"
request_4 = "declareAction_kitchen/toaster_stop-toast"
request_5 = "declareAction_kitchen/light1_off"
request_6 = "declareAction_hallway/light2_off"
request_7 = "getActions_myID_kitchen"
request_8 = "getActions_myID_light"
request_9 =  "getActions_myID_light1"
request_10 = "getActions_myID_"

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

def getRequest(request_message):
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

getRequest(request_1)
getRequest(request_2)
getRequest(request_3)
getRequest(request_4)
getRequest(request_5)
getRequest(request_6)
print('The following functions have been added to the DB')
for element in range(len(function_db)):
    print(function_db[element])
print("------------------------------------------------")
print("-------------------getActions-------------------")
print("------------------------------------------------")
getRequest(request_7)
getRequest(request_8)
getRequest(request_9)
getRequest(request_10)