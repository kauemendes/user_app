from boto.s3.connection import S3Connection
from boto.s3.key import Key as S3Key
from app import app


class s3Kit(object):

    @staticmethod
    def upload_s3(file, key_name, content_type, bucket_name,
                  callback=None, md5=None, reduced_redundancy=False):
        """ Uploads a given StringIO object to S3. Closes the file after upload.
        Returns the URL for the object uploaded.
        Note: The acl for the file is set as 'public-acl' for the file uploaded.
        Keyword Arguments:
        file -- StringIO object which needs to be uploaded.
        key_name -- key name to be kept in S3.
        content_type -- content type that needs to be set for the S3 object.
        bucket_name -- name of the bucket where file needs to be uploaded.
        """
        # create connection
        conn = S3Connection(app.config['AWS_ACCESS_KEY_ID'], app.config['AWS_SECRET_ACCESS_KEY'])

        # upload the file after getting the right bucket
        bucket = conn.get_bucket(bucket_name)
        obj = S3Key(bucket)
        obj.name = key_name
        obj.content_type = content_type
        obj.set_metadata('Content-Type', content_type)
        obj.set_contents_from_filename(file.name)
        obj.set_acl('public-read')

        # close stringio object
        return obj.generate_url(expires_in=0, query_auth=False)