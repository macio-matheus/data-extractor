from objects.base import Base


class SourceField(Base):
    def __init__(self, data_type: str, name: str, nullable: str, key_type: str, source_name: str, precision: str):
        self.data_type = data_type
        self.name = name
        self.nullable = nullable
        self.key_type = key_type
        self.source_name = source_name
        self.precision = precision
