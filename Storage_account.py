from google.cloud import storage

storage_client = storage.Client()
bucket_name = "all-set-bucket"
bucket = storage_client.create_bucket(bucket_name)
print(f"Bucket {bucket.name} created.")