import boto3
import main

# serverless.movie_data contains a list of movies
list_search = main.movie_data

# Initialize DynamoDB client
db_client = boto3.client('dynamodb')

def getMovies(event, context):
    # List to store retrieved items
    movies = []

    # create a variable that store the dynamo batch_get_item 
    response = db_client.batch_get_item(
            RequestItems = {
                'Movies' : {
                    'Keys' : [
                        {
                            'moviesID' : {'S' : '0dfe1a8c-30f5-4cb7-a626-5732fde5d776'}
                        },
                        {
                            'moviesID' : {'S' : 'd94ef58b-f867-4fea-80d4-ad202ef5aeea'}
                        }
                        ],
                    'ProjectionExpression': 'title, genre, coverUrl, releaseYear',
                }
            }
        )
    
    movies.append(response['Responses'])
    
    

    # Construct a response dictionary
    return {
           'statusCode': 200,
           'body': f"{movies}, getMoviesByYear: {getMoviesByYear()}"
        }

    # Return the response


def getMoviesByYear():
    movies_year = []
    
    # loop through the list of movies 
    for item in list_search:
        
        # append the movie years to the movies_year list
        movies_year.append(item['releaseYear'])
    
    # return the movies_year
    
    return movies_year
   