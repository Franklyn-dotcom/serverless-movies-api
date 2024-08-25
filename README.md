# How to create a serverless movie API using AWS, Python, and AWS SDK for Python (boto3)

## Table of Contents

1. Install AWS CLI
2. Configure AWS Credentials in the command line (CLI)
3. Create a virtual environment(venv)
4. Create Python files
5. Testing the application using lambda function event
6. Create an API Gateway Trigger
7. Wrapping Up

[AWS](https://aws.amazon.com/what-is-aws/) is one of the most popular cloud computing platforms. It offers over 200 different services including Compute, Databases, Storage, Networking, Machine language, Artificial Intelligence, and Internet of Things, etc.

In this article,  we'll walk you through creating a serverless movie API using the power of AWS, Python, and the AWS SDK for Python (boto3). This approach allows you to create a scalable, and cost-effective backend for your movie application without managing servers.

## Prerequisite

We're going to be using an IAM user throughout this tutorial. If you do not know how to create an IAM user, you can create an IAM user using this [link](https://www.geeksforgeeks.org/how-to-create-an-iam-user-in-aws/).

If you don't have an account with AWS, you can create a free tier account using this [link](https://aws.amazon.com/free/?gclid=EAIaIQobChMI8rLkze31hwMVTYFQBh30PyFgEAAYASAAEgLZ-PD_BwE&trk=99f831a2-d162-429a-9a77-a89f6b3bd6cd&sc_channel=ps&ef_id=EAIaIQobChMI8rLkze31hwMVTYFQBh30PyFgEAAYASAAEgLZ-PD_BwE:G:s&s_kwcid=AL!4422!3!645125273279!e!!g!!aws%20sign%20up!19574556890!145779847592&all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all)

You will also need to have a basic understanding of Python.

## Step 1: Install AWS CLI

The AWS CLI(Command Line Interface) allows you to interact with AWS services from your terminal. You can install the AWS CLI using the following [link](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

## Step 2: Configure AWS Credential in the CLI

After installing the AWS CLI, You need to configure your AWS CLI to enable you to connect and access your account. Run the following command to connect your access account:

`aws configure`

![aws-configure](/serverless-movies-api/images/aws-configure.PNG)

## Step 3: Create a virtual environment(venv)

After configuring your AWS CLI, You need to create a virtual environment(venv) for Python to enable you to manage separate package installations.

To create a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/), create a directory called `serverless`.
You can rename the directory to your own choice. After creating your directory, navigate to your project directory and run the following command for Windows:

```bash
py -m venv venv
```

After creating your virtual environment, you need to activate your virtual environment before installing or using any packages in your virtual environment. To activate it, run the following command:

`venv/Scripts/activate.bat`

![venv-activate](/serverless-movies-api/images/venv-activate-full-1.PNG)

## Step 4: Create Python files

After creating and activating your virtual environment, you need to create two python files named **main.py** and **lambda.py**. You can use any name of your choice.

The `main.py` will be used to handle the creation of your list of movies that contains the title, release year, cover image, and genre of the movies and automates the creation of an S3 bucket, DynamoDB table, and a Lambda function.

The `lambda.py` will serve as the lambda handler that handles retrieving your movie data.

After creating the files, copy and paste the following code into the `main.py`:

```python


import boto3
import json
import uuid


# create a simple list of movie data request


movie_data = [
    {
        "title": "The BeeKeeper",
        "releaseYear": "2024",
        "genre": "Action, Drama",
        "coverImage": "beekeeper.jpg"
    },
    {
        "title": "The Equaliser3",
        "releaseYear": "2024",
        "genre": "Action",
        "coverImage": "theequalizer3.jpg"
    }
   
]


# create a bucket policy to ignore public block access


bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowPerm",
            "Principal": "*",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::storage-movie-data/*"
            ]
        }
    ]
}


policy_json = json.dumps(bucket_policy)


# create a function that creates an AWS S3 SDK


def store_s3():
    s3_client = boto3.client('s3')
   
    try:
         # create a bucket name storage-movie-data and located at eu-north-1
         
        s3_client.create_bucket(Bucket='storage-movie-data', CreateBucketConfiguration={
    'LocationConstraint': 'eu-north-1'})
       
        # Applies an Amazon S3 bucket get object policy to an Amazon S3 bucket.
       
        s3_client.put_bucket_policy(
            Bucket = 'storage-movie-data',
            Policy = policy_json
        )
   
    except Exception as e:
        print(f"Bucket exist!. {e}")
   


# create a function that creates an AWS Dynamodb SDK, located in the same region(eu-north-1)


def db_nosql():  
    db_client = boto3.client('dynamodb')
    try:
        db_create = db_client.create_table(
            AttributeDefinitions = [
                {
                    'AttributeName': 'moviesID',
                    'AttributeType': 'S'
                }
            ],
            TableName = 'Movies',
           
            KeySchema = [
                {
                    'AttributeName': 'moviesID',
                    'KeyType': 'HASH'
                }
            ],
           
            BillingMode = 'PROVISIONED',
           
            ProvisionedThroughput = {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            },
           
            Tags = [
                {
                    'Key': 'project',
                    'Value': 'serverless'
                }
            ],
           
            TableClass = 'STANDARD',
           
            DeletionProtectionEnabled = False
           
        )
       
    except Exception as e:
        print(e)


# Create a function that creates an AWS Lambda SDK


def serverless_func():


    # call the AWS Lambda SDK API


    lambda_client = boto3.client('lambda')


    try:
       
       
        # Create the Lambda function with the zip file


        with open('serverless-project.zip', 'rb') as zip_data:
            lambda_client.create_function(
            FunctionName ='serverless-api-app',
            Runtime = "python3.12",
            Role = 'arn:aws:iam::885668376128:role/service-role/firstLambda-role-hp1zb8sr',
            Handler = 'lambda.getMovies',
            Code={
                'ZipFile': zip_data.read()
            }
        )
           
    except Exception as e:
        print(e)
       
       

# create a function that loops through the movie, uploads objects to the S3 bucket, generates a pre-signed URL, and adds items to the Dynamodb table  


def put_objects_s3_db():
   
    s3_client = boto3.client('s3')
    dynamo_add_item = boto3.client('dynamodb')
    try:
       
        movie_data
       
        # Loop through the movie date
        for item in movie_data:
       
            # get the coverImage of each of the movie data
            DATA_KEY = item['coverImage']
           
            # upload the objects to s3 bucket using the
            s3_client.upload_file(
                DATA_KEY, 'storage-movie-data', DATA_KEY
            )
           
            # generate a pre-signed URL for the s3 bucket
            presigned_url = s3_client.generate_presigned_url(
            ClientMethod = 'get_object',
            Params = {
               'Bucket': 'storage-movie-data',
               'Key': DATA_KEY,
            },
            ExpiresIn = 5000
            )
           
            # generate a unique ID to be used to store the value of your table item
            movie_id = str(uuid.uuid4())
           
            # add items to the Dynamodb table
            dynamo_add_item.put_item(
            TableName = 'Movies',
            Item = {
                'moviesID': {
                    "S": movie_id
                },
                'title': {
                    "S" : item['title']
                },
                'releaseYear': {
                    "S" : item['releaseYear']
                },
               
                'genre': {
                    "S" : item['genre']
                },
               
                'coverUrl' : {
                    "S" : presigned_url
                }
            }
        )
           
    except Exception as e:
        print(e)




store_s3()
db_nosql()
serverless_func()
put_objects_s3_db()


```

Now, let's go through what our code does. This code creates a simple list of movies that contains the title, releaseYear, coverImage, and genre of the movies and automates the creation of an S3 bucket, DynamoDB table, and a Lambda function using a zip file (with potential error) for managing movie data using the AWS SDK for Python ([boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)).

```python
with open('serverless-project.zip', 'rb') as zip_data:
    lambda_client.create_function(
        FunctionName ='serverless-api-app',
        Runtime = "python3.12",
        Role = 'arn:aws:iam::885668376128:role/service-role/firstLambda-role-hp1zb8sr',
        Handler = 'lambda.getMovies',
        Code={
            'ZipFile': zip_data.read()
        }
    )
```

The above code from your `main.py` allows you to open and read the zip file we will create before running the file named `serverless-project` that creates a lambda function named `serverless-api-app` that contains a runtime, role, handler, and a code that reads the zip file.

This is why we created the zip file because to create a Lambda function using AWS SDK for Python, you will need a deployment package and an execution role. For more information, visit the official [boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/create_function.html).

copy and paste the following code in the `lambda.py`

```python


import boto3
import main
import json


# main.movie_data contains a list of movies
list_search = main.movie_data


# Initialize DynamoDB resource 


db_client = boto3.resource('Dynamodb')


def getMovies(event, context):
# Retrieving the name of the table


    table = db_client.Table('Movies')


    response = table.scan()
    items = response['Items']


   # List to store retrieved items


    movies = []
   
    for item in items:
        movie = {
            'title': item['title'],
            'releaseYear': item['releaseYear'],
            'genre': item['genre'],
            'coverUrl': item['coverUrl']
        }
   
        movies.append(movie)


    # Construct a response dictionary
    return {
           'statusCode': 200,
           'headers': {
               'content-type': 'application/json'
           },
           'body': json.dumps({'movies': movies, 'getMoviesByYear': getMoviesByYear()})
        }


   
def getMoviesByYear():
    movies_year = []
   
    # Loop through the list of movies
    for item in list_search:
       
        # append the movie years to the movies_year list
        movies_year.append(item['releaseYear'])
   
    # return the movies_year
   
    return movies_year

```

To run your application, you need to install the following package:

`boto3`

Run the following command to install the package:

```bash
pip install boto3
```

After installing the following package, run the following command to create the zip file:

On Windows:

```bash
powershell Compress-Archive C:\serverless\* C:\serverless\serverless-project.zip
```

Run the following command to execute your application:

```python
python main.py
```

After running your application, navigate to your AWS console and search for S3, Dynamodb, and Lambda services to see your services in creation.

![s3-aws-console](/serverless-movies-api/images/s3.PNG)

![s3-aws-console](/serverless-movies-api/images/s3-obj.PNG)

![dynamodb-console](/serverless-movies-api/images/dynamo.PNG)

![dynamodb-console](/serverless-movies-api/images/dynamo-item.PNG)

![lambda-console](/serverless-movies-api/images/lambda-service.PNG)

## Step 5: Testing the application using Lambda function event

Now, you need to test your application using the lambda function event. In your AWS console, navigate to your Lambda service console.

![lambda-console](/serverless-movies-api/images/lambda-service.PNG)

To test your Lambda function, click on the test button to create a new test event:

![test-button](/serverless-movies-api/images/dynamo-test.PNG)

![create-event](/serverless-movies-api/images/save-test.PNG)

click on save to save the event.

After creating the event, click on the test button to test your application. You should see an output that looks like this:

```json

{
  "statusCode": 200,
  "headers": {
    "content-type": "application/json"
  },
  "body": "{\"movies\": [{\"title\": \"The BeeKeeper\", \"releaseYear\": \"2024\", \"genre\": \"Action, Drama\", \"coverUrl\": \"https://storage-movie-data.s3.amazonaws.com/beekeeper.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=<access-key>%2F20240813%2Feu-north-1%2Fs3%2Faws4_request&X-Amz-Date=20240813T182817Z&X-Amz-Expires=5000&X-Amz-SignedHeaders=host&X-Amz-Signature=7ceb0b8a3e1a82826d11833c5ec78f171420fd25a4d47fc105337fa2da511915\"}, {\"title\": \"The Equaliser3\", \"releaseYear\": \"2024\", \"genre\": \"Action\", \"coverUrl\": \"https://storage-movie-data.s3.amazonaws.com/theequalizer3.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=<access-key>%2F20240813%2Feu-north-1%2Fs3%2Faws4_request&X-Amz-Date=20240813T182819Z&X-Amz-Expires=5000&X-Amz-SignedHeaders=host&X-Amz-Signature=663049cdda2fd63d2a14b985d5501023fbd20a180c568d9e8e5744c0945cf5b8\"}], \"getMoviesByYear\": [\"2024\", \"2024\"]}"
}

```

## Step 6: Create an API Gateway Trigger

After testing your application, you need to create an API Gateway trigger function. To create an API gateway trigger, click on the add trigger button and select the API gateway source in your AWS lambda service.

![trigger-function](/serverless-movies-api/images/lamda-trigger.PNG)

After selecting the API gateway source, click on Create New API gateway, select the HTTP API type, select Open for the security, and click on the Create button to create the API Gateway trigger.

![select-source-api](/serverless-movies-api/images/select-source.PNG)

![api-gateway](/serverless-movies-api/images/api-gateway.PNG)

After creating your API Gateway, you will see your API Gateway URL.

![api-gateway-url](/serverless-movies-api/images/api-click.PNG)

copy and paste the URL into your browser and you will see an output that looks like this:

![output-2](/serverless-movies-api/images/output-2.PNG)

## Conclusion

Congratulation! You have successfully been able to build a serverless movie API using AWS, Python, and AWS SDK for Python (boto3).
