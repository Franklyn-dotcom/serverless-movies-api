import boto3
import botocore
import json
import uuid



# create a simple list of movie data request

movie_data = [
    {
        "title": "The Equaliser3",
        "releaseYear": "2024",
        "genre": "Action, Drama",
        "coverImage" : "beekeeper.jpg"
    },
    {
        "title": "The BeeKeeper",
        "releaseYear": "2024",
        "genre": "Action",
        "coverImage" : "theequalizer3.jpg"
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
				"s3:GetObject",
			],
			"Resource": [
				"arn:aws:s3:::storage-movie-data/*"
			]
		}
	]
}

policy_json = json.dumps(bucket_policy)

#generate a unique id

movie_id = str(uuid.uuid4())


# create a function that create an aws s3 sdk

def store_s3():
    s3_client = boto3.client('s3')
    try:
        print(s3_client.create_bucket(Bucket='storage-movie-data', CreateBucketConfiguration={
    'LocationConstraint': 'eu-north-1'}))
        
        s3_client.delete_public_access_block(
            Bucket = 'storage-movie-data'
        )
        
        print(s3_client.put_bucket_policy(
            Bucket = 'storage-movie-data',
            Policy = policy_json
        ))
    
    except Exception as e:
        print(f"Bucket exist!. {e}")
    
    # create a bucket name intriguing and located at eu-north-1
    # print(s3_client.create_bucket(Bucket='storage-movie-date', CreateBucketConfiguration={
    # 'LocationConstraint': 'eu-north-1'}))

# create a function that create an aws dynamodb sdk, located at same region 

def db_nosql():   
    db_client = boto3.client('dynamodb')
    try:
        db_create = db_client.create_table(
            AttributeDefinitions = [
                {
                    'AttributeName' : 'moviesID',
                    'AttributeType' : 'S'
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
                    'Key' : 'project',
                    'Value' : 'serverless'
                }
            ],
            
            TableClass = 'STANDARD',
            
            DeletionProtectionEnabled = False
            
        )
        
        print(db_create)
    except Exception as e:
        print(e)


# Create a function that create an aws lambda sdk

def serverless_func():

    # call the aws lambda sdk api 

    lambda_client = boto3.client('lambda')

    # Create a zip archive

    try:
        
        
        # Create the lambda function with the zip file 

        with open('new-main.zip', 'rb') as zip_data:
            lambda_client.create_function(
            FunctionName ='serverless-api-app',
            Runtime = "python3.12", 
            Role = 'arn:aws:iam::885668376128:role/service-role/firstLambda-role-hp1zb8sr',
            Handler = 'new_main.getMovies',
            Code={
                'ZipFile': zip_data.read()
            }
        )
            
            # return new_main.getMovies()
            
    except Exception as e:
        print(e)
        
        

#create a new empty list to append the presigned s3 object url 

# new_presigned_url_list = []

# storing movie cover image in s3 bucket using s3PutObject 

def put_objects_s3_db():
    
    s3_client = boto3.client('s3')
    dynamo_add_item = boto3.client('dynamodb')
    try:
        
        list_search = movie_data
        for item in list_search:
            
            DATA_KEY = item['coverImage']
            s3_client.upload_file(
                DATA_KEY, 'storage-movie-data', DATA_KEY
            )
            
            # generate a presigned url for the s3 bucket
            presigned_url = s3_client.generate_presigned_url(
            ClientMethod = 'get_object',
            Params = {
               'Bucket' : 'storage-movie-data',
               'Key' : DATA_KEY,
            },
            ExpiresIn = 5000
            )
            
            # new_presigned_url_list.append(presigned_url)
            
            print(dynamo_add_item.put_item(
            TableName = 'Movies',
            Item = {
                'moviesID' : {
                    "S" : movie_id
                },
                'title' : {
                    "S" : item['title']
                },
                'releaseYear' : {
                    "S" : item['releaseYear']
                },
                
                'genre' : {
                    "S" : 'Action'
                },
                
                'coverUrl' : {
                    "S" : presigned_url
                }
            }
        ))
        # return new_presigned_url_list
    except Exception as e:
        print(e)



store_s3()
db_nosql()
serverless_func()
put_objects_s3_db()
# generate_pre_signed_url()