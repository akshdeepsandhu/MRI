from minio import Minio
client = Minio("192.168.21.61:9000" , access_key="minioadmin", secret_key="minioadmin", secure=False)

bucket_name="imrh-data"