from api import db
import datetime
import os.path
import mimetypes

class MetaData(db.Model):
    extr_id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    file_path = db.Column(db.String(256))
    file_name = db.Column(db.String(64))
    file_ext = db.Column(db.String(32))
    file_type = db.Column(db.String(32))

    def to_json(self):
        return {k: v for k, v in vars(self).items() if k in [
                'extr_id',
                'date_created',
                'date_modified',
                'file_path',
                'file_name',
                'file_ext',
                'file_type'
            ]}
    
    def parse_meta(self):
        if self.file_path is not None:
            root, ext = os.path.splitext(self.file_path)
            self.file_name = os.path.basename(root)
            self.file_ext = ext
            self.date_created = datetime.datetime.fromtimestamp(os.path.getctime(self.file_path))
            self.date_modified = datetime.datetime.fromtimestamp(os.path.getmtime(self.file_path))
            self.file_type, enc = mimetypes.guess_type(self.file_path)