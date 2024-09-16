# Task 2

The program extracts specified data from an XML file and exports it to JSON, CSV, or TSV formats, or converts the file's encoding to UTF-8.
When parsing single file use parse_file subcommand with following arguments:
```sh
poetry run python main.py parse_file  --source_file .\obecna_osoba.xml  --output_file .\obecna_osoba.xml --otype csv
``` 
To search for all XML files that match a given regular expression (in double quotes) within a specified directory (including its subdirectories), use search_and_parse subcommand:
```sh
poetry run python main.py search_and_parse  --source_dir . --source_dir_recurse True --source_file_regexp "^test.*" --output_dir .  --otype csv
``` 
Unit tests:
```sh
poetry run pytest tests.py -v
``` 