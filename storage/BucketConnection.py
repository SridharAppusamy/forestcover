import boto3
import os
from botocore.exceptions import NoCredentialsError
import pandas as pd
from io import StringIO,BytesIO
import io

ACCESS_KEY = 'GOOG6JMGZAT5MEIXOPD7BZMS'
SECRET_KEY = 'icN4vNklaSdwv5sHbUBYFrjyhf1f0P1AMLqEYrle'

class Connection():
    def __init__(self):
        self.s3_client=boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
        self.s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        self.bucket='forestclassification'

    def upload_to_aws(self,local_file, s3_file):
        dicf=r'C:\Users\703202952\Downloads\waferFaultDetection (2)\waferFaultDetection\code\WaferFaultDetection_new\Prediction_Batch_files'
        for f in os.listdir(dicf):
            #content.append(f)
            path=os.path.join(dicf,f)
            s3filename='prediction-batch-files/{}' .format(f)
            self.s3.upload_file(path, self.bucket, s3filename)

    def folder_check(self):
        bucket = self.s3_resource.Bucket(self.bucket)
        val=len(list(bucket.objects.filter(Prefix='batch/')))
        if val==0:
            self.s3_client.put_object(Bucket=self.bucket,Key='batch/')
            print('prited')
        else:
            self.s3_client.delete_object(Bucket=self.bucket, Key='batch/')
            print('deleted')

        kwargs = {"Bucket": self.bucket, "Prefix":'prediction-batch-files'}
        response = self.s3_client.list_objects_v2(**kwargs)
        l=[]
        for obj in response["Contents"]:
            l.append(obj['Key'])
        print(l)

        for bucket in self.s3_resource.buckets.all():
            for obj in bucket.objects.filter(Prefix='prediction-batch-files/'):
                print('{0}:{1}'.format(bucket.name, obj.key))


    def delete_folder(self,folder_name):
        foldername='{}/'.format(folder_name)
        self.s3_client.delete_object(Bucket=self.bucket, Key=foldername)
        print('deleted')

    def create_folder(self,folder_name):
        foldername='{}/'.format(folder_name)
        self.s3_client.put_object(Bucket=self.bucket, Key=foldername)
        print('created')

    def list_of_files(self,folder_name):
        foldername = '{}/'.format(folder_name)
        bucket_files = self.s3_resource.Bucket(name=self.bucket)
        folder_exist = len(list(bucket_files.objects.filter(Prefix=foldername)))
        if folder_exist==0:
            return 'No Folder present'
        else:
            list_files=[]
            for object in bucket_files.objects.filter(Prefix=foldername):
                files_path=(object.key).split('/')[-1]
                if files_path:
                    list_files.append(files_path)
        if not list_files:
            return 'No Files present'
        else:
            return list_files


    def files_Copy(self,source_path,desination_path):
        dd='{}/{}'.format(self.bucket,source_path)
        self.s3_resource.Object(self.bucket, desination_path).copy_from(CopySource=dd)

    def readfiles_as_dataframe(self,file_path):
        obj = self.s3_client.get_object(Bucket=self.bucket, Key=file_path)
        grid_sizes = pd.read_csv(obj['Body'])
        return grid_sizes

    def delete_files(self,file_path):
        self.s3_client.delete_object(Bucket=self.bucket, Key=file_path)
        print('deleted')

    def move_files(self,source_path,desination_path):
        self.files_Copy(source_path,desination_path)
        self.delete_files(source_path)



upload=Connection()
#path=r'C:\Users\703202952\Downloads\waferFaultDetection (2)\waferFaultDetection\code\WaferFaultDetection_new\Prediction_Batch_files\wafer_07012020_041011.csv'
#dd=upload.upload_to_aws(path, '', 'Wafer_15010_13053.csv')
#print(upload.upload())
