from bucket_browser import *

bucket_region = None

# AWS S3
bucket_url = "s3://j5-org"
#bucket_region = "us-west-2"
prefix = "www/primus/audio/"

# GCS
#bucket_url = "gs://primus-j5-org"
#prefix = "audio/"


for _ in ReadBucket(bucket_url, prefix, bucket_region=bucket_region):
    print(_)
