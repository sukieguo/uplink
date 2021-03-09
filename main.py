import json
from device import Device
from calculate import get_uplink_rate
# import ipdb; ipdb.set_trace()
with open('/Users/sguo/Downloads/fake_eventtype16.json') as json_file:
    metrics = json.load(json_file)
# print (type(metrics)) # "dict"

topology = []
settled_device_mac = [] #list of string 
# list_of_satellite = []
settled_device = {}

def get_router_info(metric):
    router_mac_address = metric["routerHardware"]["deviceInfo"]["macAddress"]
    router_info = Device(router_mac_address,"",0,"", 65535)
    return router_info

router = get_router_info(metrics) # print(get_router_info(metrics).macAddress)

def add_device_to_topo(topology, device):
    topology.append(device)

def add_mac_to_list(mac_list, mac_address):
    mac_list.append(mac_address)

def add_device_to_dict(dict, device):
    dict[device.macAddress] = device

add_device_to_topo(topology, router)
add_mac_to_list(settled_device_mac, router.macAddress)
add_device_to_dict(settled_device, router)



# import ipdb; ipdb.set_trace()
for satellite in metrics["SatelliteInfo"]["Satellite"]:
    satellite_mac = satellite["deviceInfo"]["macAddress"]
    best_rate = 0
    best_ap_mac = ""
    best_ap_channel = 0
    for ap in satellite["detectedAP"]:
        ap_mac = ap["deviceInfo"]["deviceMAC"].replace(":", "") #58:0A:20:7F:E3:DF to 580A207FE3DF
        print(ap_mac)
        if  ap_mac in settled_device_mac:
            
            snr_of_ap = ap["SNRofUplinkNodeBeacon"]
            # print(snr_of_ap)
            # if only has router settled
            if len(settled_device_mac) == 1:
                best_rate = get_uplink_rate(snr_of_ap, router.uplinkRate)
                # print(best_rate)
                best_ap_mac = ap_mac
                best_ap_channel = ap["channel"]
                break
            
                
            else:
                ap_rate = settled_device[ap_mac].uplinkRate
                current_rate = get_uplink_rate(snr_of_ap, ap_rate)
                if current_rate > best_rate:
                    best_rate = current_rate
                    best_ap_mac = ap_mac
                    best_ap_channel = ap["channel"]

    
    
    new_satellite = Device(satellite_mac, best_ap_mac, 1, best_ap_channel, best_rate)
    add_device_to_topo(topology, new_satellite)
    add_mac_to_list(settled_device_mac, satellite_mac)
    add_device_to_dict(settled_device, new_satellite)
        
print(topology)
