from django.conf import settings
import os
import json

def Pin_dis(pin):
    data_res=[]
    file_path = os.path.join(settings.BASE_DIR,'data_files/pincode.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for i in data:
            x=str(i["Pincode"])
            if x==pin:
                data_r=i["Office Name"]
                data_res.append(data_r)
                data_dist=i["District"]
                data_state=i["StateName"]
        return {"data_c":data_res,"data_d":data_dist,'data_state':data_state}
    
def state_data_sending():
    try:
        states_data = []
        file_path = os.path.join(settings.BASE_DIR, 'data_files/states_dist.json')
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for values in data:
                states_data.append(values['state'])
    except Exception as e:
        states_data=['Please Try again later.']
    return states_data