import pytest
import datetime
from os.path import abspath

from src.domain.models import FileMetaData

def test_file_meta_data_is_parsed():
    f_path = abspath('tests/test_media/test_jpg.jpg')
    fmd = FileMetaData(f_path)
    fmd.parse_file_path()
    
    expected = {
        'file_path': f_path,
        'file_name': 'test_jpg',
        'date_created': datetime.date(2021, 12, 9),
        'date_modified': datetime.date(2021, 12, 9),
        'file_type': 'image/jpeg',
        'file_ext': '.jpg'
        }
    for k, v in expected.items():
        assert fmd.__getattribute__(k) == v

