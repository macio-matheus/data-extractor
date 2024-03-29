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

            # sources
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
                                                      _transform_field.get('EXPRESSION'),
                                                      transformation['MAPPING_NAME'])
                transform_fields.append(transform_field)

        elif isinstance(transformation.get('TRANSFORMFIELD'), dict):

            transform_field = TransformationField(transformation['TRANSFORMFIELD']['DATATYPE'],
                                                  transformation['TRANSFORMFIELD']['NAME'],
                                                  transformation['TRANSFORMFIELD']['PORTTYPE'],
                                                  transformation['TRANSFORMFIELD']['DEFAULTVALUE'],
                                                  transformation['TRANSFORMFIELD']['PRECISION'],
                                                  transformation['NAME'],
                                                  transformation['TRANSFORMFIELD'].get('EXPRESSION'),
                                                  transformation['MAPPING_NAME'])
            transform_fields.append(transform_field)

        return transform_fields

    def _get_transformations(self, mapping: dict):

        transformations = []

        if not mapping.get('TRANSFORMATION'):
            return transformations

        if isinstance(mapping.get('TRANSFORMATION'), list):

            for _transformation in mapping['TRANSFORMATION']:
                _transformation['MAPPING_NAME'] = mapping['NAME']
                transformation_fields = self._get_transformation_fields(_transformation)
                transformation_sql = self._get_query(_transformation)
                transformation = Transformation(_transformation['NAME'],
                                                transformation_fields, transformation_sql,
                                                mapping['NAME'])
                transformations.append(transformation)

        elif isinstance(mapping.get('TRANSFORMATION'), dict):

            mapping['TRANSFORMATION']['MAPPING_NAME'] = mapping['NAME']
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

    def _get_session_name(self, folder: dict, mapping_name: str):

        if isinstance(folder.get('SESSION'), list):
            for session in folder['SESSION']:

                if session['MAPPINGNAME'] == mapping_name:
                    return session['NAME']

        elif isinstance(folder.get('SESSION'), dict):

            if folder['SESSION']['MAPPINGNAME'] == mapping_name:
                return folder['SESSION']['NAME']

        return None

    def _get_task_name(self, task_instance: dict):

        if not task_instance['NAME']:
            return None

        if 's_' in task_instance['TASKNAME'] and task_instance['TASKTYPE'] == 'Session':
            return task_instance['TASKNAME']

        return None

    def _get_workflow_name(self, folder: dict, session_name: str):

        if isinstance(folder.get('WORKFLOW'), list):
            for workflow in folder['WORKFLOW']:

                if isinstance(workflow['TASKINSTANCE'], list):

                    for task_instance in workflow['TASKINSTANCE']:

                        task_name = self._get_task_name(task_instance)
                        if task_name == session_name:
                            return workflow['NAME']

                elif isinstance(workflow['TASKINSTANCE'], dict):

                    task_name = self._get_task_name(workflow['TASKINSTANCE'])
                    if task_name == session_name:
                        return workflow['NAME']

        elif isinstance(folder.get('WORKFLOW'), dict):

            if isinstance(folder['WORKFLOW']['TASKINSTANCE'], list):

                for task_instance in folder['WORKFLOW']['TASKINSTANCE']:

                    task_name = self._get_task_name(task_instance)
                    if task_name:
                        return task_name

            elif isinstance(folder['WORKFLOW']['TASKINSTANCE'], dict):

                task_name = self._get_task_name(folder['WORKFLOW']['TASKINSTANCE'])
                if task_name:
                    return task_name

        return None

    def _get_mappings(self, folder: dict):

        mappings = []

        if not folder.get('MAPPING'):
            return mappings

        if isinstance(folder.get('MAPPING'), list):

            for _mapping in folder['MAPPING']:
                session_name = self._get_session_name(folder, _mapping['NAME'])
                workflow_name = self._get_workflow_name(folder, session_name)
                connectors = self._get_connectors(_mapping)
                transformations = self._get_transformations(_mapping)
                mapping = Mapping(_mapping['NAME'], connectors, transformations, folder['NAME'], session_name,
                                  workflow_name)
                mappings.append(mapping)

        elif isinstance(folder.get('MAPPING'), dict):

            session_name = self._get_session_name(folder, folder['MAPPING']['NAME'])
            workflow_name = self._get_workflow_name(folder, session_name)
            connectors = self._get_connectors(folder['MAPPING'])
            transformations = self._get_transformations(folder['MAPPING'])
            mapping = Mapping(folder['MAPPING']['NAME'], connectors, transformations, folder['NAME'], session_name,
                              workflow_name)
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

    def _write_files(self, data_frames: list, names_sheets: list, writer):

        if len(data_frames) == len(names_sheets):
            ValueError("Dataframes and names sheets must be equal lengths")

        for df, sheet_name in zip(data_frames, names_sheets):
            # Write each dataframe to a different worksheet.
            df.to_excel(writer, sheet_name=sheet_name)

    def generate_documentation(self, folders: list):

        for folder in folders:

            dfs, sheets = [], []

            # Sources
            sources = [s.to_dict() for s in folder.sources]

            source_fields = []
            for s in sources:
                source_fields.extend(s.pop('source_fields', None))

            dfs.append(pd.DataFrame(sources))
            sheets.append("Sources")

            # source fields
            source_fields = [sf.to_dict() for sf in source_fields]

            dfs.append(pd.DataFrame(source_fields))
            sheets.append("Source Fields")

            # targets
            targets = [t.to_dict() for t in folder.targets]

            target_fields = []
            for t in targets:
                target_fields.extend(t.pop('target_fields', None))

            dfs.append(pd.DataFrame(targets))
            sheets.append("Targets")

            # target fields
            target_fields = [tf.to_dict() for tf in target_fields]

            dfs.append(pd.DataFrame(target_fields))
            sheets.append("Target Fields")

            # mappings
            mappings = [m.to_dict() for m in folder.mappings]

            connectors = []
            transformations = []
            for m in mappings:
                connectors.extend(m.pop('connectors', None))
                transformations.extend(m.pop('transformations', None))

            dfs.append(pd.DataFrame(mappings))
            sheets.append("Mappings")

            # connectors
            connectors = [c.to_dict() for c in connectors]

            dfs.append(pd.DataFrame(connectors))
            sheets.append("Connectors")

            # transformations
            transformations = [t.to_dict() for t in transformations]

            transformation_fields = []
            for t in transformations:
                transformation_fields.extend(t.pop('transformation_fields', None))

            dfs.append(pd.DataFrame(transformations))
            sheets.append("Transformations")

            # transformation_fields
            transformation_fields = [tf.to_dict() for tf in transformation_fields]

            dfs.append(pd.DataFrame(transformation_fields))
            sheets.append("Transformation Fields")

            # Create a Pandas Excel writer using XlsxWriter as the engine.
            writer = pd.ExcelWriter('{}{}.xlsx'.format(self.output_folder, folder.folder_name), engine='xlsxwriter')

            self._write_files(dfs, sheets, writer)

        print("Finish!!")

    def process(self):

        data = self._parser(self.input_file)
        folders = self._get_folders(data)
        self.generate_documentation(folders)


if __name__ == '__main__':
    file_process = FileProcess(input_file='/home/jovyan/work/datasets/todosObjetos.json',
                               output_folder='/home/jovyan/work/datasets/log/')
    file_process.process()
