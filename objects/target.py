from objects.base import Base


class Target(Base):
    def __init__(self, name: str, database_type: str, target_fields: str, folder_name: str):
        self.name = name
        self.database_type = database_type
        self.target_fields = target_fields
        self.folder_name = folder_name
