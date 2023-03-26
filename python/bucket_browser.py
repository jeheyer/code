
def ReadBucket(bucket_url: str, prefix: str = '') -> list:

    from boto3 import Session
    from google.cloud import storage

    try:

        bucket_name = bucket_url.split('://')[1]

        files = []; dirs = {}

        # AWS S3
        if bucket_url.startswith('s3'):
            download_url = f"http://{bucket_name}.s3.amazonaws.com/"
            s3_client = Session()
            s3_resource = s3_client.resource('s3')
            s3_bucket = s3_resource.Bucket(bucket_name)
            for _ in s3_bucket.objects.filter(Prefix=prefix):
                files.append(download_url + _.key)

        # Google Cloud Storage
        if bucket_url.startswith('gs') or bucket_url.startswith('gcs'):
            download_url = f"http://{bucket_name}.storage.googleapis.com/"
            storage_client = storage.Client.create_anonymous_client()
            for _ in storage_client.list_blobs(bucket_name, prefix=prefix):
                files.append(download_url + _.name)

        return files

    except Exception as e:
        raise(e)


if __name__ == "__main__":

    import sys

    if len(sys.argv) > 1:
        bucket_url = sys.argv[1]
    else:
        sys.exit("Usage: " + sys.argv[0] + " s3://BUCKET_NAME/path")
    
    try:
        files = ReadBucket(bucket_url)
        for f in files:
            print(f)

    except Exception as e:
        sys.exit(e)
