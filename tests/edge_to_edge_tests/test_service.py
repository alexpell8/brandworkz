import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from src.service_layer.upload import file_uploader
from src.service_layer.view_builder import get_metadata, get_metadata_collection, query_metadata_by_tag
from src.orm_layer.orm import metadata_obj, start_mappers, Transaction

import datetime

@pytest.fixture
def session_factory():
    """
    Set up a session for the transaction.
    """
    engine = create_engine('sqlite://') # set up in memory
    metadata_obj.create_all(engine)
    start_mappers()
    session_maker = sessionmaker()
    session_maker.configure(bind=engine)
    yield session_maker
    clear_mappers()

def insert_file_data(session, file_data_dict):
    """
    Insert file data to be read.
    """
    session.execute('INSERT INTO meta_data ('
    'extr_id, date_created, date_modified, file_path, file_name, file_ext, file_type)'
        ' VALUES (:extr_id, :date_created, :date_modified, :file_path, :file_name, :file_ext, :file_type)',
        file_data_dict)


class TestUploadService:

    def test_file_uploader_uploads_to_database(self, session_factory):
        """
        Test that the file is uploaded to a database in memory
        """
        transaction = Transaction(session=session_factory)
        extr_id, status_code = file_uploader('tests/test_media/test_jpg.jpg', transaction) # feature under test

        session = session_factory()
        cur = session.execute('SELECT * FROM meta_data') # database read

        assert extr_id == 1 == cur.first()[0]
        assert status_code == 201


    def test_file_uploader_does_not_upload_if_path_not_exists(self, session_factory):
        """
        Test that a bad file path does not get uploaded and returns a content not found error code.
        """
        transaction = Transaction(session=session_factory)
        extr_id, status_code = file_uploader('bad_path', transaction) # feature under test

        session = session_factory()
        cur = session.execute('SELECT * FROM meta_data') # database read

        assert cur.first() == None # nothing inserted
        assert extr_id == None
        assert status_code == 204


class TestViewBuilderService:

    def test_file_is_read_using_extraction_id(self, session_factory):
        """
        Test that the correct file is read using the extraction id.
        """
        session = session_factory()

        ts = datetime.datetime.now()
        file_data = dict(extr_id=2, date_created=ts.date(), date_modified=ts.date(),
            file_path="filepath", file_name="filename", file_ext="ext", file_type="image/jpeg")
        insert_file_data(session, file_data)

        transaction = Transaction(session=session_factory)
        response = get_metadata(2, transaction)
        assert response['metadata'] == file_data
    
    def test_all_file_are_read(self, session_factory):
        """
        Test that the full collection is returned.
        """
        session = session_factory()

        ts = datetime.datetime.now()
        file_data_1 = dict(extr_id=1, date_created=ts.date(), date_modified=ts.date(),
            file_path="filepath", file_name="filename", file_ext="ext", file_type="image/jpeg")
        insert_file_data(session, file_data_1)

        file_data_2 = dict(extr_id=2, date_created=ts.date(), date_modified=ts.date(),
            file_path="filepath", file_name="filename", file_ext="ext", file_type="image/jpeg")
        insert_file_data(session, file_data_2)

        transaction = Transaction(session=session_factory)
        response = get_metadata_collection(transaction)
        assert response['filedata'] == [{'metadata': file_data_1}, {'metadata': file_data_2}]
    
    def test_tag_value_query_returns_matches(self, session_factory):
        """
        Test that the selected tag, value pair are queried and returned.
        """
        session = session_factory()

        ts = datetime.datetime.now()
        file_data_1 = dict(extr_id=1, date_created=ts.date(), date_modified=ts.date(),
            file_path="filepath", file_name="filename", file_ext="ext", file_type="image/jpeg")
        insert_file_data(session, file_data_1)

        file_data_2 = dict(extr_id=2, date_created=ts.date(), date_modified=ts.date(),
            file_path="filepath", file_name="filename_to_select", file_ext="ext", file_type="image/jpeg")
        insert_file_data(session, file_data_2)

        transaction = Transaction(session=session_factory)
        response = query_metadata_by_tag(tag='file_name', value='filename_to_select', transaction=transaction)
        assert response['filedata'][0]['metadata'] == file_data_2