class Endpoint:

    BATTERY_THRESHOLDS = {
        "EP1": 2500,
        "EP2": 2500,
        "Canary_A": 3600, }

    def __init__(self,
        serial_number: str,
        hardware_type: str,
        node_uuid: str,
        battery: int,
        version: str,
        backlog: int = 0,  ):

        if hardware_type not in self.BATTERY_THRESHOLDS:
            raise ValueError("Unsupported endpoint type")
        if battery < 0:
            raise ValueError("Battery cannot be negative")
        if backlog < 0:
            raise ValueError("backlog cannot be negative")

        self.serial_number = serial_number
        self.hardware_type = hardware_type
        self.node_uuid = node_uuid
        self._battery = battery
        self._version = version
        self._backlog = backlog
    
    def can_start_dfu(self) -> bool:
        if self._backlog!=0 or self._battery < self.BATTERY_THRESHOLDS[self.hardware_type]:
            return False
        return True

    def start_dfu(self, new_version: str) -> bool:
        if self.can_start_dfu():
            self._version = new_version
            return True
        return False
    
    def drain_backlog(self):
        self._backlog = 0

    def get_battery(self):
        return self._battery

    def set_battery(self, battery):
        if battery < 0:
            raise ValueError("Battery cannot be negative")
        self._battery = battery
    
    def get_backlog(self):
        return self._backlog

    def set_backlog(self, backlog):
        if backlog < 0:
            raise ValueError("Backlog cannot be negative")
        self._backlog = backlog


    def get_version(self): 
        return self._version


       
