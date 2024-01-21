import os

import oss2
from dotenv import load_dotenv


class OSSStorage:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        load_dotenv(dotenv_path)
        access_key_id = os.getenv("ACCESS_KEY_ID")
        access_key_secret = os.getenv("ACCESS_KEY_SECRET")
        bucket_name = os.getenv("BUCKET_NAME")
        endpoint = os.getenv("ENDPOINT")

        self.bucket = oss2.Bucket(
            oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name
        )

    def list(self, path):
        return [obj.key for obj in oss2.ObjectIterator(self.bucket, prefix=path)]

    def put(self, obj, path):
        return self.bucket.put_object(path, obj)

    def delete(self, path):
        return self.bucket.delete_object(path)

    def get(self, path):
        return self.bucket.get_object(path).read()
