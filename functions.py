import json

file_state = open('final_state_wise.json', 'r')
data_state = json.load(file_state)

file_highway = open('final_highway_wise.json', 'r')
data_highway = json.load(file_highway)


def fetch_states():
    return list(data_state.keys())

def fetch_plazas(state):
    return list(data_state[state].keys())

def fetch_highways(state, plaza):
    highway =  list(data_state[state][plaza].keys())[0]
    plaza_id = plaza.split('-')[1]
    length = data_state[state][plaza][highway]['Highway Length']
    plaza_name = data_state[state][plaza][highway][plaza_id]['Plaza Name']
    latitude = data_state[state][plaza][highway][plaza_id]['Latitude']
    longitude = data_state[state][plaza][highway][plaza_id]['Longitude']
    model = data_state[state][plaza][highway][plaza_id]['Model']
    data = data_state[state][plaza][highway][plaza_id]['Details']
    return highway, length, plaza_name, latitude, longitude, model, data

def fetch_highway_wise():
    return list(data_highway.keys())

def fetch_highway_state(highway):
    state_list = {}
    for data in data_highway[highway]:
        if list(data.keys())[0] not in state_list:
            state_list[list(data.keys())[0]] = 1
        else:
            state_list[list(data.keys())[0]] += 1
    
    return state_list

def fetch_toll_state(highway, state):
    length, id, plaza_name, latitude, longitude, model, details = [], [], [], [], [], [], []
    for tolls in data_highway[highway]:
     
        for temp_state, values in tolls.items():
            if temp_state == state:
                length.append(values['Highway Length'])   
                temp_id = list(values.keys())[-1]
                id.append(temp_id)
                data = values[temp_id]
                plaza_name.append(data['Plaza Name'])
                latitude.append(data['Latitude'])
                longitude.append(data['Longitude'])
                model.append(data['Model'])
                details.append(data['Details'])

    return length, id, plaza_name, latitude, longitude, model, details  


