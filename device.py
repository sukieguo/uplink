

class Device:
    def __init__(self, macAddress, uplinkMacAddress, hop, channel, uplinkRate):
        self.macAddress = macAddress
        self.uplinkMacAddress = uplinkMacAddress
        self.hop = hop
        self.channel = channel
        self.uplinkRate = uplinkRate
    
    def get_device_uplink_rate(self):
        return self.uplinkRate


    