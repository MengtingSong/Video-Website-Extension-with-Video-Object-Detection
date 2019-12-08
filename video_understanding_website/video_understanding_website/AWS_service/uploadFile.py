import json
import boto3
from urllib.request import urlopen
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    dynamodb = boto3.resource('dynamodb')

    if event:
        file_obj = event["Records"][0]
        bucket_name = str(file_obj["s3"]["bucket"]["name"])
        file_name = str(file_obj["s3"]["object"]["key"])
        user_email = file_name.split('/')[0]

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

        #TODO: get object detection by usinng frame-level logistics model



        # put result into DynamoDB table
        table = dynamodb.Table('videos')

        response = table.query(
        KeyConditionExpression=Key('email').eq(user_email)
    )
        count = response['Count']
        video_dic = {'file_name': file_name.split('/')[1], 'classes': classes}

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
                Key = {'email':user_email},
                UpdateExpression='SET videos = :val1',
                ExpressionAttributeValues={
                ':val1': video_list
                }
            )
        return {
        'statusCode': 200,
        'body': json.dumps('Object detection result has been stored into DynamoDB!')
        }
