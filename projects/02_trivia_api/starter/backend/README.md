# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints

GET '/categories'
    - Description
        - Fetches a dictionary of categories which contains (id and type) and total number of categoriest
    - Parameter: None
    - Returns: 
        An object of categories and total_categories. 
        {
            'success' : true,
            'categories' : [
                {
                    'id' : 1,
                    'type' : 'science'
                },
                {
                    'id' : 2,
                    'type' : 'art'
                }
            ]
        }
    - Responses:
        200:
            Description: objects successfuly returned


GET '/questions'
    Description
        - Fetches a dictionary of questions with answers and all categories provided with the total number of questions available.
    - Parameters: None
    - Returns: 
        An object of questions which contains list of (question, answer, category, difficulty), all categories and total_questions. 
        {
            'success':True,
            'questions':{
                "id":1,
                "questions":{
                    "question" : "how are you1",
                    "answer" : "fine",
                    "category" : "1",
                    "difficulty" : 2
                    },
                    {
                    "question" : "how old are you",
                    "answer" : "15",
                    "category" : "1",
                    "difficulty" : 4
                    },
                "total_questions":50,
                "catgeories":[science, art, history]
            }
            
        }
    - Responses:
        200:
            Description: objects successfuly returned
        404:
            Description: no questions found

POST '/questions'
    - Description 1:
        - Searches for a specific questions
    - Parameters:
        searchTerm: contains a string to filter questions wit
    - Returns: 
        An object of questions which contains list of (question, answer, category, difficulty), all categories and total_questions. 
        {
            'success':True,
            'questions':{
                "id":1,
                "questions":{
                    "question" : "how are you1",
                    "answer" : "fine",
                    "category" : "1",
                    "difficulty" : 2
                    },
                    {
                    "question" : "how old are you",
                    "answer" : "15",
                    "category" : "1",
                    "difficulty" : 4
                    },
                "total_questions":50,
                "catgeories":[science, art, history]
            }
            
        }
    - Responses:
        200:
            Description: objects successfuly returned
        404:
            Description: no questions found for this search

    - Description 2:
        - Adds new question with answer, category and difficulty
    - Parameters:
        question: question to add
        answer: answer to question
        category: category id of the question
        difficulty: difficulty level
    - Returns:
        { 
            "success": true
        }
    - Responses:
        200:
            Description: object successfuly added
        400:
            Description: object failed to be added


DELETE '/questions/<id>'
    - Description:
        -Deletes a question
    - Parameters:
        id: question's id
    - Returns:
        {
            "success" : true,
            "id" : 5
        }
    - Responses:
        200:
            Description: object successfuly deleted
        422:
            Description: object failed to be deleted

GET '/categories/<cat_id>/questions'
    - Description:
        -Get questions for specific category
    - Parameters:
        cat_id: id of the category
    - Returns
        An object of questions which contains list of (question, answer, category, difficulty), all categories and total_questions. 
        {
            'success':True,
            'questions':{
                "id":1,
                "questions":{
                    "question" : "how are you1",
                    "answer" : "fine",
                    "category" : "1",
                    "difficulty" : 2
                    },
                    {
                    "question" : "how old are you",
                    "answer" : "15",
                    "category" : "1",
                    "difficulty" : 4
                    },
                "total_questions":50,
                "catgeories":[science, art, history]
            }
            
        }
    - Responses:
        200:
            Description: object successfuly returned
        404:
            Description: category not found or there's no questions in the current category

POST '/quizzes'
    - Description
        - get random questions from specific category if selected
    - Parameters:
        previous_questions: list of ids for previous questions
        quiz_category: object of category contains type and its id
    - Returns:
        {
            "success" : true,
            "question" : {
                "question" : "how are you1",
                "answer" : "fine",
                "category" : "1",
                "difficulty" : 2
            }
        }
    - Responses:
        200:
            Description: objects successfuly returned
        404:
            Description: category not found


```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```