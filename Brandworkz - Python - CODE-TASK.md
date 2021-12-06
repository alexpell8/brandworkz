# Coding Task
Your primary task is to build an API to store and retrieve/query metadata extracted from files.

In this task, as in our business, performance and scalability are key factors.
It would be great if the architecture of the application reflected these constraints.


## Requirements
* Python must be used as a programming language.
* README file explaining how to run your service and describing how you would extend the API to store a
  large amount of data(millions/billions) and have it queryable way. Please try to add as much detail as you can.

## Endpoints

### Extract metadata
This endpoint will allow the user to upload a file to the system in order to extract its metadata(any file type/ any size).

Internally the endpoint is responsible to extract the metadata of the file and store the file's metadata
in a way to be possible to query it via another endpoint.

Note: _Metadata is a very unstructured piece of data, but there are certain data we want to store in a more structured way:_
* Extraction id - a generated unique id that is recorded on every extraction
* Date Created - the date that the file was created, should be obtained from the metadata, this will be located in several fields of the metadata
* Date Created - the date that the file was last modified, should be obtained from the metadata, this will be located in several fields of the metadata
* File Path - the path where the file was uploaded
* File Name - the original file name
* File Extension - the extension of the file
* File Mime Type - the mime-type of the file uploaded

Examples of where dates could be found(just few examples):
* EXIF: DateTimeOriginal
* XMP: DateCreated

* EXIF: ModifyDate
* XMP: ModifyDate

### Get metadata
This endpoint will retrieve the metadata stored in the system for a given Extraction id

### Query metadata
This endpoint will retrieve all the assets in the system that have a given metadata key:value

Example: GET endpoint?tag=<tag>&value=<value>


## Notes
* Feel free to choose the technologies/tools from the frameworks/libraries to the data storage.
* It may be easier to give us a link to a git repo when you're done, otherwise a compressed git archive would be fine.
