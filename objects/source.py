from objects.base import Base


class Source(Base):
    def __init__(self, database_type: str, database_name: str, source_name: str, owner_name: str, source_fields: list,
                 folder_name: str):
        self.database_type = database_type
        self.database_name = database_name
        self.source_name = source_name
        self.owner_name = owner_name
        self.source_fields = source_fields
        self.folder_name = folder_name
