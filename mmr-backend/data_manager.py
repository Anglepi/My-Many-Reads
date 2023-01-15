class DataManager:
    def __init__(self, address: str) -> None:
        self._address = address

    def __connect(self) -> None:
        self.connection = open(self._address)

    def __disconnect(self) -> None:
        if self.connection:
            self.connection.close()
