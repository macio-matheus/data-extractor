from objects.base import Base


class TransformationField(Base):
    def __init__(self, data_type: str, name: str, port_type: str, default_value: str, precision: str,
                 transformation_name: str, expression: str):
        self.data_type = data_type
        self.name = name
        self.port_type = port_type
        self.default_value = default_value
        self.precision = precision
        self.transformation_name = transformation_name,
        self.expression = expression
