#Getting filesize and rows:
#Method 1:
import os
print('File path: s3://{s3_landing_bucket}/{bucket_location}/{file_name}')
c=os.popen('aws s3 cp s3://{s3_landing_bucket}/{bucket_location}/{file_name} - | wc -c -l')
Total_rows,Size=c.read().split()
print("Total rows of the file:"+ Total_rows)
print("Size of the file:"+ str(int(Size)/1000)+'KB')
#Method 2:
import boto3
filename={file_name}
bucket_name={bucket_name}
file_nm="bucket_location"+'/'+filename
s3=boto3.client('s3','us-west-2')
response=s3.head_object(Bucket=bucket_name,Key=file_nm)
print(f"Size of the file {filename} is {response['ContentLength']} bytes.")

#Copying file from Mount to S3:
import boto3
session=boto3.Session(aws_access_key_id='',aws_secret_access_key='',)
s3=session.resource('s3')
s3.meta.client.upload_file(Filename='/apps',Bucket='pllidpdev',Key='data/cycledate')

#Boto3 S3 client Generator:
def s3_create_client(bucket):
    try:
        if 'dev' in bucket:
            client=boto3.client('s3',aws_access_key_id='',aws_secret_access_keys='')
        else:
            client=boto3.client('s3')
        return client
    except Exception as e:
        raise(e)

#Upload file to s3:
def s3_upload_file(s3_object,bucket,filename):
    try:
        client=s3_create_client(bucket)
        client.upload_file(filename,bucket,s3_object)
    except Exception as e:
        raise(e)
    
#Dataframe containing downloaded parquet file data
def s3_download_parquet(bucket,s3_object):
    try:
        fs=s3fs.S3FileSystem()
        p_dataset=pq.ParquetDataset(
            "s3://{0}/{1}".format(bucket,s3_object),
            filesystem=fs
        )
    except Exception as e:
        raise(e)

#Deleting S3 file:
def s3_delete_object(bucket,s3_object):
    try:
        client=s3_create_client(bucket)
        client.delete_object(Bucket=bucket, Key=s3_object)
    except Exception as e:
        raise(e)

#Deleting multiple S3 file:
def s3_delete_objects(bucket_name,s3_prefix):
    try:
        s3=boto3.resource('s3')
        bucket=s3.Bucket(bucket_name)
        s3_objects=[os.key for os in bucket.objects.filter(Prefix=s3_prefix)]
        client=s3_create_client(bucket_name)
    except Exception as e:
        raise(e)