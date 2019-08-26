from objects.base import Base


class Transformation(Base):
    def __init__(self, name: str, transformation_fields: list, sql: str, mapping_name: str):
        self.name = name
        self.transformation_fields = transformation_fields
        self.sql = sql
        self.mapping_name = mapping_name
