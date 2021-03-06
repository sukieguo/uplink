
#dict
SNR_TO_RATE_TABLE = {
    44: 1429,
    42: 1429,
    40: 1365,
    39: 1303,
    36: 1302,
    35: 1107,
    32: 1107,
    30: 1107,
    29: 1091,
    26: 906,
    24: 693,
    23: 693,
    20: 462,
    19: 461,
    16: 335,
    14: 230,
    12: 115,
    11: 110,
    10: 53,
    8: 27,
    6: 6,
    5: 0
}

# print(SNR_TO_RATE_TABLE)
CAP_RATE = 65535
SCALING_FACT = 0.85

def get_uplink_rate(snr_of_uplink_node_beacon, uplink_rate):
    corresponding_rate = SNR_TO_RATE_TABLE[snr_of_uplink_node_beacon]
    if uplink_rate == 65535:
        return (corresponding_rate * uplink_rate * 1) / (corresponding_rate + uplink_rate)
    
    return (corresponding_rate * uplink_rate * SCALING_FACT) / (corresponding_rate + uplink_rate)
