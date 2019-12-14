# EC601_MiniProject_3 - Video Object Detection Website

## Demo
[![Watch the demo video]](https://youtu.be/zKVONcwYjqY)

## Deployment Instructions
### 1. Environment Requirements
- Python 3.6/3.7 - https://www.python.org/downloads/
- npm and node.js - https://nodejs.org/en/

### 2. Install AWS Command Line Interface
- Command: `pip3 install awscli`

### 3. Configure AWS CLI
- Command: `aws configure`  
- Then enter the AWS account key and ID (offered in my email to professor), default region name is ‘us-east-2’, default output format is none (type nothing).

### 4. Python and Node Modules
- Install using requirements.txt: type ‘pip3 install -r requirements.txt’ in terminal to install the required python libraries.
- Install using npm: type ‘npm install’ to install all the required npm libraries.

### 5. Running the Website
- Add the AWS key info:  
  - Go to the following path in our project: `Google_Photos_for_Audio/googleAudioProject/frontend/AWS_keys.js`
  - Add AWS ID and Key (offered in my email to professor), this is required for Uploading function.
  - After installation, type `npm run dev` to automatically create/update the main.js file, which must be done before start up the website.
  - Then type `python/python3 manage.py runserver` , this will start up the website and return a localhost link. Click it and you will head to our website.

Note:
- Right now it only supports mp4 type and each file should be no longer than 1 minute and no larger than 30 megabytes, which is the supported file type of Amazon Rekogniton.
- There may be incompatibilities with Safari, so please use Google Chrome.

## Vision and Goals Of The Project
In this project, I will build a website for object detection of videos. On a high level, users can come to the site to upload their video files (mp4); the object detection of these videos will be completed by AWS Rekogniton, allowing users to search for video using object classes found in their video content.

High-level goals including:
* Building a user-friendly website that allows users to upload/download and use specific classes to search for videos.
* Utilizing AWS services like AWS S3, Lambda, Rekogniton, DynamoDB, Comprehend for cloud platform, storage, etc. functions.

## Users/Personas Of The Project
* Video object detection will be used by people who want to store and organize video files in a user-searchable manner on the cloud. 
* These people include journalists, academic researchers, and reporters who need to be able to search through the files with detected classes.

## User Stories
TBD

## Scope and Features Of The Project
This project is not built from scratch. I will build on this project on the foundation of one of my other project working together with the other three teammates (historical commits to the project can be checked). In this project, the major work is as below:
- Adjust the previous project code to fit with the new project goal
- Set up all required AWS cloud services including DyanmoDB, EC2, S3, Lambda, Rekognition, IAM, etc. and integrate these services with the project
- Complete the Lambda function for triggering Rekognition to detect objects right after the user upload a video to his/her unique S3 folder and then store the result into his/her unique DynamoDB item.

Overall, below is an overview of the program features from the perspective of the program architecture.

- Front end
  - provides user-friendly UI
    - displays a user’s video files in a grid/list sorted by date uploaded
  - allows users to login/register using Amazon/Google sign-in forms
  - allows users to upload/download video files from/to their computer’s file system
  - allows users to search for vidoo using text
  - allows users to delete video files
- Back end
  - audio file management
    - retrieve an video file
    - store new/uploaded video file
    - update status of video file (has it been detected or not)
    - delete video file
  - video file object detection
    - detect object classes included in the video files
    - store detected classes
  - user management
    - create a new user in the system
    - retrieve user details
    
## Solution Concept
### High-Level architecture and goals:
* Upload the video files in Amazon S3, an object storage service.
* An upload event will be pushed to AWS Pub/Sub topic.
* Use AWS Lambda to watch for the pubsub topic.
* Use AWS Rekognition to detect object classes contained in the uploaded videos.
* Store the analysis result and user data into AWS DaynamoDB, queryable by our website.
* The site will be hosted on AWS EC2.
The diagram of whole project's structure is as followed.
![Image text](https://github.com/MengtingSong/EC601_MiniProject_3/blob/master/project_architecture.png)

## Issues not solved
In completing the Lambda function for object detection, the Rekognition service always runs longer than 15 minutes which is the highest time limitaion of keep a Lambda function running set by AWS. This always causes the close of the function before the object detection process to be finished.

