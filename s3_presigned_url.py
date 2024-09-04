import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Initialize the S3 client
s3_client = boto3.client('s3')

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    """
    Generate a presigned URL for downloading an S3 object.

    :param bucket_name: string, the name of the S3 bucket
    :param object_name: string, the name of the object in the S3 bucket
    :param expiration: Time in seconds for the presigned URL to remain valid (default is 3600)
    :return: Presigned URL as string, or None if error.
    """
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
        return response
    except (NoCredentialsError, PartialCredentialsError) as e:
        print("Credentials not available:", e)
        return None

def generate_presigned_post(bucket_name, object_name, expiration=3600):
    """
    Generate a presigned URL for uploading an object to S3.

    :param bucket_name: string, the name of the S3 bucket
    :param object_name: string, the name of the object to upload
    :param expiration: Time in seconds for the presigned URL to remain valid (default is 3600)
    :return: A dictionary with the presigned URL and fields, or None if error.
    """
    try:
        response = s3_client.generate_presigned_post(
            bucket_name,
            object_name,
            ExpiresIn=expiration
        )
        return response
    except (NoCredentialsError, PartialCredentialsError) as e:
        print("Credentials not available:", e)
        return None

# Example usage
bucket = 'yaadav-s3-private'
object_name = 'your-object-name' #change this with the image name 

# Generate presigned URL for downloading
download_url = generate_presigned_url(bucket, object_name)
if download_url:
    print("Download URL:", download_url)

# Generate presigned URL for uploading
upload_url = generate_presigned_post(bucket, object_name)
if upload_url:
    print("Upload URL:", upload_url['url'])
    print("Upload Fields:", upload_url['fields'])
