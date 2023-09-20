from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'static'

    def delete(self, name):
        self.bucket.delete_object(Key=self._normalize_name(name))


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False

    def delete(self, name):
        self.bucket.delete_object(Key=self._normalize_name(name))
