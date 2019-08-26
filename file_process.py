import json

import pandas as pd

from objects.folder import Folder
from objects.mapping import Mapping
from objects.source import Source
from objects.target import Target
from objects.target_field import TargetField
from objects.source_field import SourceField
from objects.transformation import Transformation
from objects.transformation_field import TransformationField
from objects.connector import Connector


class FileProcess(object):
    def __init__(self, input_file: str = None, output_folder: str = None):
        self.input_file = input_file
        self.output_folder = output_folder

    def _get_folders(self, data: dict):
        # Data folder informations
        powermart_object = data['POWERMART']
        repository_object = powermart_object['REPOSITORY']
        repository_version = powermart_object['REPOSITORY_VERSION']
        repository_name = repository_object['NAME']
        folder_object = repository_object['FOLDER']
        database_type = repository_object['DATABASETYPE']

        folders = []
        for _folder in folder_object:
            folder_name = _folder['NAME']

            # sources **** trazer nomes dos mappi
            sources = self._get_sources(_folder)

            # targets
            targets = self._get_targets(_folder)

            # mappings
            mappings = self._get_mappings(_folder)

            folder = Folder(repository_version, repository_name, folder_name, database_type, sources=sources,
                            mappings=mappings,
                            targets=targets)

            folders.append(folder)

        return folders

    def _get_sources(self, folder: dict):

        sources = []

        if not folder.get('SOURCE'):
            return sources

        if isinstance(folder.get('SOURCE'), list):

            for _source in folder['SOURCE']:
                source_fields = self._get_source_fields(_source)
                source = Source(_source['DATABASETYPE'], _source['DBDNAME'], _source['NAME'], _source['OWNERNAME'],
                                source_fields, folder['NAME'])
                sources.append(source)

        elif isinstance(folder.get('SOURCE'), dict):

            source_fields = self._get_source_fields(folder['SOURCE'])
            source = Source(folder['SOURCE']['DATABASETYPE'], folder['SOURCE']['DBDNAME'], folder['SOURCE']['NAME'],
                            folder['SOURCE']['OWNERNAME'], source_fields, folder['NAME'])
            sources.append(source)

        return sources

    def _get_source_fields(self, source: dict):

        source_fields = []

        if not source.get('SOURCEFIELD'):
            return source_fields

        if isinstance(source.get('SOURCEFIELD'), list):

            for _source_field in source['SOURCEFIELD']:
                source_field = SourceField(_source_field['DATATYPE'], _source_field['NAME'],
                                           _source_field['NULLABLE'], _source_field['KEYTYPE'], source['NAME'],
                                           _source_field['PRECISION'])
                source_fields.append(source_field)

        elif isinstance(source.get('SOURCEFIELD'), dict):

            source_field = SourceField(source['SOURCEFIELD']['DATATYPE'], source['SOURCEFIELD']['NAME'],
                                       source['SOURCEFIELD']['NULLABLE'], source['SOURCEFIELD']['KEYTYPE'],
                                       source['NAME'], source['SOURCEFIELD']['PRECISION'])
            source_fields.append(source_field)

        return source_fields

    def _get_transformation_fields(self, transformation: dict):

        transform_fields = []

        if not transformation.get('TRANSFORMFIELD'):
            return transform_fields

        if isinstance(transformation.get('TRANSFORMFIELD'), list):

            for _transform_field in transformation['TRANSFORMFIELD']:
                transform_field = TransformationField(_transform_field['DATATYPE'],
                                                      _transform_field['NAME'],
                                                      _transform_field['PORTTYPE'],
                                                      _transform_field['DEFAULTVALUE'],
                                                      _transform_field['PRECISION'],
                                                      transformation['NAME'],
                                                      _transform_field.get('EXPRESSION'))
                transform_fields.append(transform_field)

        elif isinstance(transformation.get('TRANSFORMFIELD'), dict):

            transform_field = TransformationField(transformation['TRANSFORMFIELD']['DATATYPE'],
                                                  transformation['TRANSFORMFIELD']['NAME'],
                                                  transformation['TRANSFORMFIELD']['PORTTYPE'],
                                                  transformation['TRANSFORMFIELD']['DEFAULTVALUE'],
                                                  transformation['TRANSFORMFIELD']['PRECISION'],
                                                  transformation['NAME'],
                                                  transformation['TRANSFORMFIELD'].get('EXPRESSION'))
            transform_fields.append(transform_field)

        return transform_fields

    def _get_transformations(self, mapping: dict):

        transformations = []

        if not mapping.get('TRANSFORMATION'):
            return transformations

        if isinstance(mapping.get('TRANSFORMATION'), list):

            for _transformation in mapping['TRANSFORMATION']:
                transformation_fields = self._get_transformation_fields(_transformation)
                transformation_sql = self._get_query(_transformation)
                transformation = Transformation(_transformation['NAME'],
                                                transformation_fields, transformation_sql,
                                                mapping['NAME'])
                transformations.append(transformation)

        elif isinstance(mapping.get('TRANSFORMATION'), dict):

            transformation_fields = self._get_transformation_fields(mapping['TRANSFORMATION'])
            transformation_sql = self._get_query(mapping['TRANSFORMATION'])
            transformation = Transformation(mapping['TRANSFORMATION']['NAME'],
                                            transformation_fields, transformation_sql,
                                            mapping['NAME'])
            transformations.append(transformation)

        return transformations

    def _get_query(self, transformation):

        if isinstance(transformation.get('TABLEATTRIBUTE'), list):

            for _table_attribute in transformation['TABLEATTRIBUTE']:

                if _table_attribute['NAME'] == "Sql Query":
                    return _table_attribute['VALUE']

        return ""

    def _get_targets(self, folder: dict):

        targets = []

        if not folder.get('TARGET'):
            return targets

        if isinstance(folder.get('TARGET'), list):

            for _target in folder['TARGET']:
                target_fields = self._get_target_fields(_target)
                target = Target(_target['NAME'], _target['DATABASETYPE'], target_fields, folder['NAME'])
                targets.append(target)

        elif isinstance(folder.get('TARGET'), dict):

            target_fields = self._get_target_fields(folder['TARGET'])
            target = Target(folder['TARGET']['NAME'], folder['TARGET']['DATABASETYPE'], target_fields, folder['NAME'])
            targets.append(target)

        return targets

    def _get_target_fields(self, target: dict):

        target_fields = []

        if not target.get('TARGETFIELD'):
            return target_fields

        if isinstance(target.get('TARGETFIELD'), list):

            for _target_field in target['TARGETFIELD']:
                target_field = TargetField(_target_field['DATATYPE'], _target_field['NAME'], _target_field['NULLABLE'],
                                           _target_field['KEYTYPE'], target['NAME'], _target_field['PRECISION'])
                target_fields.append(target_field)

        elif isinstance(target.get('TARGETFIELD'), dict):

            # data_type, name, nullable, key_type, precision
            target_field = TargetField(target['TARGETFIELD']['DATATYPE'], target['TARGETFIELD']['NAME'],
                                       target['TARGETFIELD']['NULLABLE'], target['TARGETFIELD']['KEYTYPE'],
                                       target['NAME'], target['TARGETFIELD']['PRECISION'])
            target_fields.append(target_field)

        return target_fields

    def _get_mappings(self, folder: dict):

        mappings = []

        if not folder.get('MAPPING'):
            return mappings

        if isinstance(folder.get('MAPPING'), list):

            for _mapping in folder['MAPPING']:
                connectors = self._get_connectors(_mapping)
                transformations = self._get_transformations(_mapping)
                mapping = Mapping(_mapping['NAME'], connectors, transformations, folder['NAME'])
                mappings.append(mapping)

        elif isinstance(folder.get('MAPPING'), dict):

            connectors = self._get_connectors(folder['MAPPING'])
            transformations = self._get_transformations(folder['MAPPING'])
            mapping = Mapping(folder['MAPPING']['NAME'], connectors, transformations, folder['NAME'])
            mappings.append(mapping)

        return mappings

    def _get_connectors(self, mapping: dict):

        connectors = []

        if not mapping.get('CONNECTOR'):
            return connectors

        if isinstance(mapping.get('CONNECTOR'), list):

            for _connector in mapping['CONNECTOR']:
                connector = Connector(_connector['FROMFIELD'], _connector['FROMINSTANCE'],
                                      _connector['FROMINSTANCETYPE'], _connector['TOFIELD'], _connector['TOINSTANCE'],
                                      _connector['TOINSTANCETYPE'], mapping['NAME'])
                connectors.append(connector)

        elif isinstance(mapping.get('MAPPING'), dict):

            connector = Connector(mapping['MAPPING']['FROMFIELD'], mapping['MAPPING']['FROMINSTANCE'],
                                  mapping['MAPPING']['FROMINSTANCETYPE'], mapping['MAPPING']['TOFIELD'],
                                  mapping['MAPPING']['TOINSTANCE'],
                                  mapping['MAPPING']['TOINSTANCETYPE'],
                                  mapping['NAME'])
            connectors.append(connector)

        return connectors

    def _parser(self, input_file):

        with open(input_file, 'r') as data_file:
            data = json.loads(data_file.read())
        return data

    def generate_documentation(self, folders: list):

        for folder in folders:

            # Sources
            sources = [s.to_dict() for s in folder.sources]

            source_fields = []
            for s in sources:
                source_fields.extend(s.pop('source_fields', None))

            df_sources = pd.DataFrame(sources)

            # source fields
            source_fields = [sf.to_dict() for sf in source_fields]

            df_source_fields = pd.DataFrame(source_fields)

            # targets
            targets = [t.to_dict() for t in folder.targets]

            target_fields = []
            for t in targets:
                target_fields.extend(t.pop('target_fields', None))

            df_targets = pd.DataFrame(targets)

            # target fields
            target_fields = [tf.to_dict() for tf in target_fields]

            df_target_fields = pd.DataFrame(target_fields)

            # mappings
            mappings = [m.to_dict() for m in folder.mappings]

            connectors = []
            transformations = []
            for m in mappings:
                connectors.extend(m.pop('connectors', None))
                transformations.extend(m.pop('transformations', None))

            df_mappings = pd.DataFrame(mappings)

            # connectors
            connectors = [c.to_dict() for c in connectors]
            df_connectors = pd.DataFrame(connectors)

            # transformations
            transformations = [t.to_dict() for t in transformations]

            transformation_fields = []
            for t in transformations:
                transformation_fields.extend(t.pop('transformation_fields', None))

            df_transformations = pd.DataFrame(transformations)

            # transformation_fields
            transformation_fields = [tf.to_dict() for tf in transformation_fields]
            df_transform_fields = pd.DataFrame(transformation_fields)

            # Create a Pandas Excel writer using XlsxWriter as the engine.
            writer = pd.ExcelWriter('{}{}.xlsx'.format(self.output_folder, folder.folder_name), engine='xlsxwriter')

            # Write each dataframe to a different worksheet.
            df_sources.to_excel(writer, sheet_name='Sources', index=False)
            df_source_fields.to_excel(writer, sheet_name='Source Fields', index=False)
            df_targets.to_excel(writer, sheet_name='Targets', index=False)
            df_target_fields.to_excel(writer, sheet_name='Target Fields', index=False)
            df_mappings.to_excel(writer, sheet_name='Mappings', index=False)
            df_transformations.to_excel(writer, sheet_name='Tranformation', index=False)
            df_transform_fields.to_excel(writer, sheet_name='Tranformation Fields', index=False)
            df_connectors.to_excel(writer, sheet_name='Connectors', index=False)

            # Close the Pandas Excel writer and output the Excel file.
            writer.save()

        print("Finish!!")

    def process(self):

        data = self._parser(self.input_file)
        folders = self._get_folders(data)
        self.generate_documentation(folders)


if __name__ == '__main__':
    file_process = FileProcess(input_file='./datasets/todosObjetos.json', output_folder='./datasets/generated_doc/')
    file_process.process()
