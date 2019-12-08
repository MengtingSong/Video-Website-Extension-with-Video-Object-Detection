from botocore.exceptions import ClientError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import generics
from .serializers import FileSerializer
import boto3


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('videos')


class Userfiles(generics.CreateAPIView):
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        user_email = request.data['user_email']
        new_email = user_email.replace('@', '__')
        try:
            response = table.get_item(
                Key={
                    'email': new_email
                }
            )
            video_info = response['Item']['videos']
            print(video_info)
            context = {}
            context['email'] = new_email
            context['Info'] = video_info
            return Response(data=video_info, status=200)
        except:
            return Response(data='Videos not loaded.', status=400)
