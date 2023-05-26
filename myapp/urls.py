from django.urls import path, include
from .views import base_views, question_views, answer_views, topic_views

app_name = "myapp"

urlpatterns = [
    # topic_views.py
    path("topics/", topic_views.index, name="topics"),
    path("topics/read/<int:id>", topic_views.read),
    path("topics/create/", topic_views.create),
    path("topics/delete/", topic_views.delete),
    path("topics/update/<int:id>", topic_views.update),
    # new_topic_views.py    
    
    # base_views.py
    path("questions/", base_views.questionsIndex, name="questions"),
    path("questions/<int:question_id>/", base_views.questionDetail, name="questionDetail"),
    # question_views.py
    path("question/create/", question_views.questionCreate, name="questionCreate"),
    path('question/modify/<int:question_id>/', question_views.questionModify, name='questionModify'),
    path('question/delete/<int:question_id>/', question_views.questionDelete, name='questionDelete'),
    path('question/vote/<int:question_id>/', question_views.questionVote, name='questionVote'),
    # answer_views.py
    path("answer/create/<int:question_id>/", answer_views.answerCreate, name="answerCreate"),
    path('answer/modify/<int:answer_id>/', answer_views.answerModify, name='answerModify'),
    path('answer/delete/<int:answer_id>/', answer_views.answerDelete, name='answerDelete'),
    path('answer/vote/<int:answer_id>/', answer_views.answerVote, name='answerVote'),
    
]
