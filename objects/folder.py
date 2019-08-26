from objects.base import Base


class Folder(Base):
    def __init__(self, repository_version: str, repository_name: str, folder_name: str, database_type: str,
                 targets: list = None, sources: list = None, mappings: list = None):
        self.repository_version = repository_version
        self.repository_name = repository_name
        self.folder_name = folder_name
        self.database_type = database_type
        self.targets = targets
        self.sources = sources
        self.mappings = mappings
