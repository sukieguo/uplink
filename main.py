import json
from topo import Device
from calculate import get_uplink_rate
# import ipdb; ipdb.set_trace()
with open('/Users/sguo/Downloads/fake_eventtype16.json') as json_file:
    metrics = json.load(json_file)
# print (type(metrics)) # "dict"

topology = []
list_of_settled_device_mac = [] #list of string 
list_of_satellite = []
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
    dict[device.mac_address] = device

add_device_to_topo(topology, router)
add_mac_to_list(list_of_settled_device_mac, router.macAddress)
add_device_to_dict(settled_device, router)




for satellite in metrics["SatelliteInfo"]["Satellite"]:
    satellite_mac = satellite["deviceInfo"]["macAddress"]
    best_rate = 0
       
    for ap in satellite["detectedAP"]:
        ap_mac = ap["deviceInfo"]["deviceMAC"].replace(":", "") #58:0A:20:7F:E3:DF to 580A207FE3DF
        if  ap_mac in list_of_settled_device_mac:
            
            snr_of_ap = ap["SNRofUplinkNodeBeacon"]
            # print(snr_of_ap)
            # if only has router settled
            if len(list_of_settled_device_mac) == 1:
                best_rate = get_uplink_rate(snr_of_ap, router.uplinkRate)
                # print(best_rate)
                new_satellite = Device(satellite_mac, ap_mac, 1, ap["channel"], best_rate)
                add_device_to_topo(topology, new_satellite)
                add_mac_to_list(list_of_settled_device_mac, satellite_mac)
                # print(list_of_settled_device_mac)
            
                
            else:
                ap_rate = settled_device[ap_mac].uplink_rate
                current_rate = get_uplink_rate(snr_of_ap, ap_rate)
                if current_rate > best_rate:
                    best_rate = current_rate

                new_satellite = Device(satellite_mac, ap_mac, 1, ap["channel"], best_rate)
                add_device_to_topo(topology, new_satellite)
                add_mac_to_list(list_of_settled_device_mac, satellite_mac)

        

