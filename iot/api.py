from .node import Node
from .endpoint import Endpoint



class API:

    def __init__(self):
        self._nodes = {}


    def init_node(self, uuid: str, version: str):

        if uuid in self._nodes:
            raise ValueError("Node already exists")

        node = Node(uuid, version)
        self._nodes[uuid] = node  
    
    def add_endpoint(
    self,
    serial_number: str,
    hardware_type: str,
    node_uuid: str,
    battery: int,
    version: str,
    backlog: int = 0 ):
    
    # Check that the Node exists
        if node_uuid not in self._nodes:
            raise ValueError("Node does not exist")

    # Check that the serial number is unique
        for node in self._nodes.values():
            if node.find_endpoint(serial_number) is not None:
                raise ValueError("Endpoint serial already exists")

    # Create the Endpoint
        endpoint = Endpoint(serial_number, hardware_type, node_uuid, battery, version,backlog)

    # Add the Endpoint to its Node
        node = self._nodes[node_uuid]
        node.add_endpoint(endpoint)
    
    def find_endpoint_by_serial(self, serial_number: str):

        for node in self._nodes.values():
            endpoint = node.find_endpoint(serial_number)

            if endpoint is not None:
                return endpoint

        raise ValueError("Endpoint does not exist")


    def api_get_node_by_uuid(self, uuid: str) -> dict:

        if uuid not in self._nodes:
            raise ValueError("Node does not exist")

        node = self._nodes[uuid]

        return {
        "uuid": node.uuid,
        "ota_channel": node.ota_channel,
        "version": node.get_version(),
        "endpoints": node.get_endpoints(),
        "last_error": node.get_last_error() }   

    
    def api_get_endpoint_by_serial(self, serial_number: str) -> dict:

        endpoint = self.find_endpoint_by_serial(serial_number)

        return {
        "serial_number": endpoint.serial_number,
        "battery": endpoint.get_battery(),
        "hardware_type": endpoint.hardware_type,
        "uuid": endpoint.node_uuid,
        "version": endpoint.get_version(),
        "backlog": endpoint.get_backlog()}


    def find_node_by_channel(self, ota_channel: str):
        for node in self._nodes.values():
            if node.ota_channel == ota_channel:
                return node

        return None


    def api_post_version_to_ota_channel(self, ota_channel: str, version_artifact: str) -> int:

        node = self.find_node_by_channel(ota_channel)
        if node is None:
            return 400
        if node.receive_ota_artifact(version_artifact):
            return 200
        return 400



    def api_clear_ota_channel(self, ota_channel: str, version_artifact: str) -> int:
    
        node = self.find_node_by_channel(ota_channel)
        if node is None:
            return 400
    
        if node.clear_ota_channel(version_artifact):
            return 200
        return 400


    def api_tick_ota(self, ota_channel: str) -> str:

        node = self.find_node_by_channel(ota_channel)

        if node is None:
            raise ValueError("OTA channel does not exist")

        return node.poll_ota()


    
    def api_set_backlog(self, serial_number: str, backlog: int) -> None:
        endpoint = self.find_endpoint_by_serial(serial_number)
        endpoint.set_backlog(backlog)


    def api_drain_backlog(self, serial_number: str) -> None:
        endpoint = self.find_endpoint_by_serial(serial_number)
        endpoint.drain_backlog()


    def api_set_battery(self, serial_number: str, battery: int) -> None:
        endpoint = self.find_endpoint_by_serial(serial_number)
        endpoint.set_battery(battery)


    def api_start_dfu(self, serial_number: str, new_version: str) -> bool:
        endpoint = self.find_endpoint_by_serial(serial_number)
        return endpoint.start_dfu(new_version)

 




