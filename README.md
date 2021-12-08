# BRANDWORKZ CODING TASK
Build an API to store meta data from an uploaded file and expose metadata over endpoints.

The API requirements are stored in "Brandworkz - Python CODE-TASK.md".

## USAGE

### `GET /filedata/<int:extr_id>`
GET the stored metadata for the extracted file with given extr_id.

*Response*
```format: json
{
    metadata: {
        extr_id: int,
        date_created: UTC-standard,
        date_modified: UTC-standard,
        file_path: str,
        file_name: str,
        file_ext: str,
        file_type: str
    },
    200 OK on success,
    204 No Content if a valid endpoint but no data,
}
```

### `GET /filedata`
GET the stored metadata for the filedata collection.

*Response*
```format: json
{
    metadata: {
        [{
        extr_id: int,
        date_created: UTC-standard,
        date_modified: UTC-standard,
        file_path: str,
        file_name: str,
        file_ext: str,
        file_type: str
        },
        ...
        ]
    },
    200 OK on success,
    204 No Content if a valid endpoint but no data,
}
```

### `GET /filedata?tag=<tag>&value=<value>`
GET metadata for all files in the filedata collection which match the tag:value pair in the query string.

*Response*
```format: json
{
    metadata: {
        [{
        extr_id: int,
        date_created: UTC-standard,
        date_modified: UTC-standard,
        file_path: str,
        file_name: str,
        file_ext: str,
        file_type: str
        },
        ...
        ]
    },
    200 OK on success,
    204 No Content if a valid endpoint but no data,
}
```
## STORAGE
The uploaded files are stored as a database in a .db file indexed by the unique extr_id value as the primary key.
Using a migration library such as Flask-Migrate mitigates any upscaling issues relating to expansion of the database.
