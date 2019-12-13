import boto3
import json
import sys
import time
import json
import boto3
from urllib.request import urlopen
from boto3.dynamodb.conditions import Key, Attr


class VideoDetect:
    jobId = ''
    rek = boto3.client('rekognition')
    sqs = boto3.client('sqs')
    sns = boto3.client('sns')

    roleArn = ''
    bucket = ''
    video = ''
    startJobId = ''

    sqsQueueUrl = ''
    snsTopicArn = ''
    processType = ''

    def __init__(self, role, bucket, video):
        self.roleArn = role
        self.bucket = bucket
        self.video = video

    def StartLabelDetection(self):
        response = self.rek.start_label_detection(Video={'S3Object': {'Bucket': self.bucket, 'Name': self.video}},
                                                  NotificationChannel={'RoleArn': self.roleArn,
                                                                       'SNSTopicArn': self.snsTopicArn})

        self.startJobId = response['JobId']
        print('Start Job Id: ' + self.startJobId)
        print(response)

    def GetLabelDetectionResults(self):
        maxResults = 20
        paginationToken = ''
        finished = False

        class_list = []

        while finished == False:
            response = self.rek.get_label_detection(JobId=self.startJobId,
                                                    MaxResults=maxResults,
                                                    NextToken=paginationToken,
                                                    SortBy='TIMESTAMP')

            for labelDetection in response['Labels']:
                label = labelDetection['Label']
                class_list.append(label['Name'])

                if 'NextToken' in response:
                    paginationToken = response['NextToken']
                else:
                    finished = True

        return class_list


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    dynamodb = boto3.resource('dynamodb')

    if event:
        file_obj = event["Records"][0]
        bucket_name = str(file_obj["s3"]["bucket"]["name"])
        file_name = str(file_obj["s3"]["object"]["key"])
        user_email = file_name.split('/')[0]

        print("processing")

        # terminate processing if file already existed
        table = dynamodb.Table('videos')
        response = table.query(
            KeyConditionExpression=Key('email').eq(user_email)
        )
        count = response['Count']
        if count == 1:
            video_list = response['Items'][0]['videos']
            for video in video_list:
                if video['file_name'] == file_name.split('/')[1]:
                    return {
                        'statusCode': 500,
                        'body': json.dumps('Uploading failed. File already existed')
                    }

        roleArn = 'arn:aws:iam::832724215976:role/service-role/objectDetection-role-ss2mf9gn'
        bucket = bucket_name
        video = file_name

        analyzer = VideoDetect(roleArn, bucket, video)

        analyzer.StartLabelDetection()
        time.sleep(300)
        class_list = analyzer.GetLabelDetectionResults()

        # put result into DynamoDB table
        table = dynamodb.Table('videos')

        response = table.query(
            KeyConditionExpression=Key('email').eq(user_email)
        )
        count = response['Count']
        video_dic = {'file_name': file_name.split('/')[1], 'classes': class_list}

        if count == 0:
            table.put_item(
                Item={
                    'email': user_email,
                    'videos': [video_dic]
                }
            )

        elif count == 1:
            video_list = response['Items'][0]['videos']
            video_list.append(video_dic)
            table.update_item(
                Key={'email': user_email},
                UpdateExpression='SET videos = :val1',
                ExpressionAttributeValues={
                    ':val1': video_list
                }
            )

        return {
            'statusCode': 200,
            'body': json.dumps('Object detection result has been stored into DynamoDB!')
        }