# PowerCenter data extractor

Script to extract structured data in spreadsheets from PowerCenter exported .xmls (converted to .jsons) files.


### Example Usage

```python

file_process = FileProcess(input_file='./input/export.json', output_folder='./output/')
file_process.process()

```
### Input file structure

File input structure example

```sh
  JSON
    CREATION_DATE : "08/19/2019"
    REPOSITORY_VERSION : "1"
    REPOSITORY
      NAME : "Foo"
      VERSION : "1"
      CODEPAGE : "UTF-8"
      DATABASETYPE : "SQL SERVER"
      FOLDER
        NAME : "Example"
        GROUP : ""
        OWNER : "Admin"
        SHARED : "NOTSHARED"
        DESCRIPTION : "EXAMPLE"
        PERMISSIONS : "rwx------"
        UUID : "e255b70f"
        SOURCE: [{}]
        TARGET: [{}]
        MAPPING: [{}]
        CONFIG: [{}]
        SESSION: [{}]
        WORKFLOW: [{}]
```
