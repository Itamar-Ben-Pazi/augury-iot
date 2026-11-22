class Node:

    API_HOSTS = {
        "AHN2": "buildroot_api.azure",
        "CASSIA": "buildroot_api.azure",
        "MOXA": "moxa_api.azure" }

    def __init__(self, uuid: str, version: str):

        parts = uuid.split("_", 1)

        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError("Invalid Node UUID")

        hardware_type = parts[0].upper()

        if hardware_type not in self.API_HOSTS:
            raise ValueError("Unsupported Node type")
        
        self.uuid = uuid
        self.hardware_type = hardware_type
        self.api_host = self.API_HOSTS[hardware_type]
        self.ota_channel = f"OTA_{uuid}"
        self._version = version
        self._endpoints = {}

        self._channel_artifact = None
        self._poll_count = 0
        self._ota_status = "IDLE"
        self._last_error = ""

    
    def add_endpoint(self, endpoint):
        if endpoint.node_uuid != self.uuid:
            raise ValueError("Endpoint belongs to another Node")

        if endpoint.hardware_type in self._endpoints:
            raise ValueError("Endpoint type already exists")

        self._endpoints[endpoint.hardware_type] = endpoint

    def get_endpoints(self) -> list:
        serials = []
        for endpoint in self._endpoints.values():
            serials.append(endpoint.serial_number)
        return serials

    def get_version(self) -> str:
        return self._version

    def validate_artifact(self, artifact: str) -> bool:
        if not artifact.endswith(".swu"):
            return False

        name = artifact.removesuffix(".swu")
        parts = name.split("_", 1)

        if len(parts) != 2 or not parts[0] or not parts[1]:
            return False

        if parts[0].upper() != self.hardware_type.upper():
            return False

        return True

    def receive_ota_artifact(self, artifact: str) -> bool:
        if not self.validate_artifact(artifact):
            self._channel_artifact = None
            self._poll_count = 0
            self._last_error = "Invalid or mismatched artifact"
            self._ota_status = "FAILED"
            return False

        self._channel_artifact = artifact
        self._poll_count = 0
        self._ota_status = "PENDING"
        self._last_error = ""

        return True



    def poll_ota(self) -> str:
        if self._ota_status != "PENDING":
            return self._ota_status

        self._poll_count += 1

        if self._poll_count < 2:
            return "PENDING"

        name = self._channel_artifact.removesuffix(".swu")
        new_version = name.split("_", 1)[1]

        self._version = new_version
        self._ota_status = "UPDATED"

        return "UPDATED"


    def clear_ota_channel(self, artifact: str) -> bool:
        if self._channel_artifact != artifact:
            return False

        self._channel_artifact = None
        self._poll_count = 0
        self._ota_status = "IDLE"
        self._last_error = ""

        return True

    def find_endpoint(self, serial_number: str):
        for endpoint in self._endpoints.values():
            if endpoint.serial_number == serial_number:
                return endpoint
        return None


    def get_last_error(self) -> str:
        return self._last_error

    def get_ota_status(self) -> str:
        return self._ota_status
