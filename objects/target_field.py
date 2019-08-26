from objects.base import Base


class TargetField(Base):
    def __init__(self, data_type: str, name: str, nullable: str, key_type: str, target_name: str, precision: str):
        self.data_type = data_type
        self.name = name
        self.nullable = nullable
        self.key_type = key_type
        self.target_name = target_name
        self.precision = precision
