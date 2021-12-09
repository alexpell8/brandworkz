# BRANDWORKZ CODING TASK
Build an API to store meta data from an uploaded file and expose metadata over endpoints.

The API requirements are stored in ["Brandworkz - Python CODE-TASK.md"](http://127.0.0.1:5000/task).

## USAGE

### `GET /filedata/<int:extr_id>`
GET the stored metadata for the extracted file with given extr_id.

**Response**

format: json

    ```
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
        status: 200 OK on success, 204 No Content if a valid endpoint but no data
    }
    ```

### `GET /filedata`
GET the stored metadata for the filedata collection.

**Response**

format: json

    ```
    {
        filedata: [{metadata: {
            extr_id: int,
            date_created: UTC-standard,
            date_modified: UTC-standard,
            file_path: str,
            file_name: str,
            file_ext: str,
            file_type: str
            },
            ...
            ],
        status: 200 OK on success, 204 No Content if a valid endpoint but no data
    }
    ```

### `GET /filedata?tag=<tag>&value=<value>`
GET metadata for all files in the filedata collection which match the tag:value pair in the query string.

**Response**

format: json

    ```
    {
        filedata: [{metadata: {
            extr_id: int,
            date_created: UTC-standard,
            date_modified: UTC-standard,
            file_path: str,
            file_name: str,
            file_ext: str,
            file_type: str
            },
            ...
            ],
        status: 200 OK on success, 204 No Content if a valid endpoint but no data
    }
    ```

## STORAGE
The uploaded files are stored as a database in a .db file indexed by the unique extr_id value as the primary key.

## HTML Form
A HTML form for POSTing a file path has been selected for ease. A second GET query string passing path=<path/to/file> is an equally viable alternative and this may be more desirable if batch processing.

---

## EXPANDING THE API
### End Points
For production use the API would benefit from being version controlled (/api/v1/...) which would allow for backwards compatibility and beta versions for testing.

### Querying
Opening up further query options such as;

- `WHERE date created > <date>`
- `WHERE date created < <date>`
- `WHERE file name CONTAINS <substring>`
- `WHERE ext = <extension>`
- `WHERE file type = <html>`
- `WHERE file type = null - may be particularly useful for selecting unrecognised mime types.`

or a combination of these filter examples.

### Storage
The database choice would likely need to be reconsidered at much larger volumes however the transition is made much easier by the choice to use an ORM like SQLAlchemy.

SQLAlchemy has been selected as an ORM aids in protection against SQL injection and provides a database agnostic solution. In this case a .db file has been used however SQLAlchemy makes migrating to other databases easy.
Further on migration and upscaling, using a migration extension such as Flask-Migrate mitigates upscaling issues relating to expansion or modification of the database without having to re-ingest data.

If upscaling the upload business logic to handle batch processing to create assets in the database then the upload_file service should be refactored to detect for a list of paths, or other multi-file input, and this case the db commit should take place after all resources have been added. Care would need to be taken to catch unsuccessful additions such as paths that do not exist.

### Security
The potential for storing personal data means that protection against threats like SQL injection is a priority. An ORM further protects/obscures the raw database queries.
THe use of a API keys should also be considered so that a level of authorisation may take place.