import boto3
import requests
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from matplotlib import pyplot as plt
from PIL import Image
from io import BytesIO

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

# Example usage
bucket = 'yaadav-s3-private'
object_name = 'black.png'  # Replace with your image file name

# Generate presigned URL for downloading the image
download_url = generate_presigned_url(bucket, object_name)

if download_url:
    print("Download URL:", download_url)
    
    # Fetch the image from the presigned URL
    response = requests.get(download_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Open the image using PIL and display using matplotlib
        image = Image.open(BytesIO(response.content))
        plt.imshow(image)
        plt.axis('off')  # Hide axis
        plt.show()
    else:
        print("Failed to retrieve the image. Status code:", response.status_code)
else:
    print("Failed to generate presigned URL.")
