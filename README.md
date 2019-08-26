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
        NAME : "PRD_CMSN_EXPT_DDOS_TRANSACAO"
        GROUP : ""
        OWNER : "Administrator"
        SHARED : "NOTSHARED"
        DESCRIPTION : "PRD_CMSN_EXPT_DDOS_TRANSACAO PRD_CMSN_EXPT_DDOS_CADASTRO PRD_CMSN_EXPT_DDOS_PRODUTO"
        PERMISSIONS : "rwx------"
        UUID : "e255b70f-2dda-43f0-b450-23ae52ff3165"
        SOURCE: [{}]
        TARGET: [{}]
        MAPPING: [{}]
        CONFIG: [{}]
        SESSION: [{}]
        WORKFLOW: [{}]
```
