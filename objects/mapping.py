from objects.base import Base


class Mapping(Base):
    def __init__(self, name: str, connectors: list, transformations: list, folder_name: str):
        self.name = name
        self.connectors = connectors
        self.transformations = transformations
        self.folder_name = folder_name
