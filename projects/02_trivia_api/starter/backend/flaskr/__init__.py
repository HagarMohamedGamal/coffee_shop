import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy.sql.expression import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def handle_paginate(req, selections):
  page = req.args.get("page", 1, int)
  selected = selections[
    ((page-1)*QUESTIONS_PER_PAGE) : (page)*QUESTIONS_PER_PAGE
    ]
  return [quest.format() for quest in selected]

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/*": {"origins": "*"}})
  
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", 'Content-Type')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    return jsonify({
      "success" : True,
      "categories" : [cat.type for cat in categories],
      "total_categories" : len(categories)
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route("/questions", methods=['POST', 'GET'])
  def get_questions():
    if request.method == "GET":
      questions = Question.query.order_by(Question.id).all()
      categories = Category.query.all()
      questions_paginated = handle_paginate(request, questions)
      if len(questions_paginated)>0:
        return jsonify({
          "success" : True,
          "questions" : questions_paginated,
          "total_questions" : len(questions),
          "categories" : [cat.type.lower() for cat in categories],
          "current_category" : "hh"
        })
      else:
        abort(404)
    elif request.method == "POST":
      data = request.get_json(force=True)
      if "searchTerm" in data:
        searchTerm = data["searchTerm"]
        questions = Question.query.filter(Question.question.ilike("%{}%".format(searchTerm))).all()
        categories = Category.query.all()
        questions_paginated = handle_paginate(request, questions)
        if len(questions_paginated)>0:
          return jsonify({
            "success" : True,
            "questions" : questions_paginated,
            "total_questions" : len(questions),
            "categories" : [cat.type.lower() for cat in categories],
            "current_category" : "hh"
          })
        else:
          abort(404)
      else:
        question = data["question"]
        answer = data["answer"]
        difficulty = data["difficulty"]
        category = data["category"]
        if(question=="" or answer=="" or difficulty=="" or category==""):
          abort(400)
        try:
          q = Question(question, answer, category, difficulty)
          q.insert()
          return jsonify({
            "success" : True
          })
        except:
          abort(400)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/questions/<int:quest_id>", methods=['DELETE'])
  def DELETE_question(quest_id):
    question = Question.query.filter_by(id=quest_id).first()
    if question is None:
      abort(422)
    else:
      question.delete()
      return jsonify({
        "success" : True,
        "id" : quest_id
      })

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:cat_id>/questions')
  def get_questions_by_categories(cat_id):
    category = Category.query.filter_by(id=cat_id).first()
    
    if category is None:
      abort(404)
    questions = Question.query.filter_by(category=cat_id).all()
    if questions is None:
      abort(404)
    else:
      return jsonify({
        "success" : True,
        "questions" : [ques.format() for ques in questions],
        "total_questions" : len(questions),
        "current_category" : category.type
      })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=["POST"])
  def play_quizzes():
    data = request.get_json(force=True)
    previous_questions = data["previous_questions"]
    quiz_category = data["quiz_category"]
    
    if quiz_category["id"]!=0:
      category = Category.query.filter(Category.id==quiz_category["id"]).first()
    
    if quiz_category["id"]==0:
      question = Question.query.filter(~Question.id.in_(previous_questions)).order_by(func.random()).first()
    elif category is None:
      abort(404)
    else:
      question = Question.query.filter(~Question.id.in_(previous_questions)).filter(Question.category==category.id).order_by(func.random()).first()
      
    if question is None:
      return jsonify({
        "success" : False
      })
    else:
      return jsonify({
        "success" : True,
        "question" : question.format()
      })
      
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success" : False,
      "message" : "not found",
      "error" : 404
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success" : False,
      "message" : "unprocessable",
      "error" : 422
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success" : False,
      "message" : "bad request",
      "error" : 400
    }), 400

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success" : False,
      "message" : "internal server error",
      "error" : 500
    }), 500
  
  return app

    