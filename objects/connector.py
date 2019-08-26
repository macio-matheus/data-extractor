from objects.base import Base


class Connector(Base):
    def __init__(self, from_field: str, from_instance: str, from_instance_type: str, to_field: str, to_instance: str,
                 to_instance_type: str, mapping_name: str):
        self.from_field = from_field
        self.from_instance = from_instance
        self.from_instance_type = from_instance_type
        self.to_field = to_field
        self.to_instance = to_instance
        self.to_instance_type = to_instance_type
        self.mapping_name = mapping_name
