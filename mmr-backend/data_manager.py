class DataManager:
    def __init__(self, address: str) -> None:
        self._address = address

    def connect(self) -> None:
        self.connection = open(self._address)

    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()
