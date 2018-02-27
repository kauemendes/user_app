import os

import magic

from app.helper_kit.s3kit import s3Kit
from app import app


class FileKit(object):

    @staticmethod
    def create_or_open_file(file_name):
        try:
            file = open(os.path.join(app.config["UPLOAD_FOLDER"], file_name), "xb")
        except FileNotFoundError as e:
            file = open(os.path.join(app.config["UPLOAD_FOLDER"], file_name), "wb")
        except Exception as e:
            app.logger.error('{0} Failed to create file'.format(file_name))
            return False

        return file

    @staticmethod
    def send_file_to_s3(file, final_name, mime_type) -> str or bool:
        try:
            uri = s3Kit.upload_s3(file, final_name, mime_type, app.config["S3_BUCKET_NAME"])
            return uri
        except Exception as e:
            app.logger.error('{0} Failed to send file to s3'.format(final_name))
            return False

    @staticmethod
    def get_mime_type(file):
        try:
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(file.name)
        except Exception as e:
            app.logger.error('{0} Failed to get mimetype using Magic'.format(file.name))
            return False

        if not any([mime_type == key for key in app.config["ALLOWED_EXTENSIONS"]]):
            app.logger.error('{0} Failed to create file, mismatching extensions'.format(file.name))

        return mime_type

    @staticmethod
    def remove_file_from_tmp(file_name):
        try:
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], file_name))
        except Exception as e:
            app.logger.error('{0} Failed to remove file from tmp file'.format(file_name))
