import os

import boto3
from services.utils.object_downloader import get_raw_object
from services.utils.constants import IMAGE_NOT_FOUND
from django.http import Http404


class AmazonS3Connection:
    def __init__(self, profile_name, bucket_name):
        self.session = boto3.Session(profile_name=profile_name)
        self.s3_resource = self.session.resource("s3")
        self.bucket = self.s3_resource.Bucket(bucket_name)

    def post_object_from_url(self, url):
        downloaded_obj = get_raw_object(url)
        if downloaded_obj:
            key = url.split("/")[-1]
            return self.bucket.upload_fileobj(downloaded_obj, key)
        else:
            raise Http404(IMAGE_NOT_FOUND)

    def get_object_from_url(self, url):
        key = url.split("/")[-1]
        return self.bucket.Object(key)

    def get_object_url(self, url):
        key = url.split("/")[-1]
        obj = self.bucket.Object(key)
        if obj:
            url = "https://%s.s3.amazonaws.com/%s" % (self.bucket.name, key)
            return url
        else:
            raise Http404(IMAGE_NOT_FOUND)

    def delete_object_from_url(self, url):
        key = url.split("/")[-1]
        obj = self.bucket.Object(key)
        if obj:
            return obj.delete()
        else:
            pass

    def put_object_from_url(self, url, new_url):
        key = url.split("/")[-1]
        obj = self.bucket.Object(key)
        if obj:
            obj.delete()
        return self.post_object_from_url(new_url)


s3_connection = AmazonS3Connection(profile_name=os.environ.get("PROFILE_NAME"), bucket_name="imagecontainer")
