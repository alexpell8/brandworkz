# BRANDWORKZ CODING TASK
Build an API to store meta data from an uploaded file and expose metadata over endpoints.

The API requirements are stored in ["Brandworkz - Python CODE-TASK.md"](http://127.0.0.1:5000/task).

## USAGE

To run the app;

Use the requirements.txt provided
Activate environment and navigate to brandworkz root folder.
Call `python run_api.py`

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
For production use the API would benefit from being version controlled (/api/v1/...) which would allow for backwards compatibility and beta versions.

### Querying
Opening up further query options such as;

- `WHERE date created > <date>`
- `WHERE date created < <date>`
- `WHERE file name CONTAINS <substring>`
- `WHERE ext = <extension>`
- `WHERE file type = <html>`
- `WHERE file type = null - may be particularly useful for selecting unrecognised mime types.`

or a combination of these filter examples.

It is worth noting that for very large queries using multiple joins or chains there may be a performance improvement
by using raw SQL rather than the ORM API.

### Storage
The database choice may need to be reconsidered at much larger volumes however the transition/migration is made much easier by the choice to use an ORM like SQLAlchemy.

SQLAlchemy has been selected as an ORM aids in protection against SQL injection and provides a database agnostic solution. In this case a .db file has been used however SQLAlchemy makes migrating to other databases easy.
Further on migration and upscaling, using a migration extension such as Flask-Migrate mitigates upscaling issues relating to expansion or modification of the database schema without having to re-ingest data.

### Architectural Design
The current design has a presentation layer (/api), a domain layer (/domain), an ORM layer (/orm_layer) and a service layer (/service_layer). This has been chosen to separate responsibilities of each module.

- api shall handle web-facing and user interaction.
- domain shall handle the business objectives/logic
- orm_layer is the abstraction of the database transactions
- service_layer is the orchestration of the upload and view services.

This design, while potentially over-complex for this CRUD API, should net some scalability benefits.

If upscaling the upload business logic to handle batch processing to create assets in the database then the upload service is easily extended to detect for a list of paths, or other multi-file input, and this case the uploading is completed within one transaction. A potential example has been commented out in the upload.py module. The trade-off of locking the database for sustained periods of time should be considered.
Care would need to be taken to handle unsuccessful inserts/violations of domain logic such as paths that do not exist. We may not want to fail to upload N files if the N+1 file is invalid. Any unique file upload should fail independently in this case. This may prompt a refactor towards event-driven design such that an upload can be commanded and events can be raised and handled appropriately.

To deal with potential locking if larger transactions are occuring then it may be useful to implement a read-only table as to not obstruct other users from uploading files. This would be a fairly easy addition to this code by allowing a ReadOnlyTransaction to use a get_read_only_session factory which would be configured at a separate table. This should all be possible by modifying/extending the orm_layer database abstraction and refactoring the GET end-points.

### Security
The potential for storing personal data means that protection against threats like SQL injection is a priority. An ORM further protects/obscures the raw database queries.
The use of a API keys should also be considered so that a level of authorisation may take place.