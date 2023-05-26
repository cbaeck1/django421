from django.shortcuts import HttpResponse, redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Register your models here.
from ..models import Topics
from ..forms import QuestionForm, AnswerForm

nextId = 4
topics = [
  {"id": 1, "title": "routing", "body": "Routing is ..."},
  {"id": 2, "title": "view", "body": "View is ..."},
  {"id": 3, "title": "model", "body": "Model is ..."},
]


def HTMLtemplate(articleTag, id=None):
    global topics
    contextUI = ""
    if id != None:
        contextUI = f"""
        <li><form action='/myapp/topics/delete/' method='post'>
              <input type='hidden' name='id' value={id}>
              <input type='submit' value='delete'>
            </form>
        </li>
    """
    ol = ""
    for topic in topics:
        ol += (
            f'<li><a href="/myapp/topics/read/{topic["id"]}">{topic["title"]}</a></li>'
        )

    return f"""
    <htmm>
    <body>
      <h1><a href='/myapp/topics/'>Django</a></h1>
      <ol>
        {ol}
      </ol>
      {articleTag}

      <ul>
        <li><a href='/myapp/topics/create'>Create</a></h1></li>
        {contextUI}
        <li><a href='/myapp/topics/update/{id}'>Update</a></h1></li>
      </ul>
    </body>
    </htmm>
  """


# Create your views here.
def index(request):
    article = """
    <h2>Welcome</h2>
      Hello, Django
  """
    return HttpResponse(HTMLtemplate(article))


def read(request, id):
    global topics
    article = ""
    for topic in topics:
        if topic["id"] == int(id):
            article += f'<h2{topic["title"]}"</h2>{topic["body"]}'
    return HttpResponse(HTMLtemplate(article, id))


@csrf_exempt
def create(request):
    # 동일한 URL 요청을 POST, GET 요청 방식에 따라 다르게 처리
    global nextId
    if request.method == "GET":
        article = """
      <form action='/myapp/topics/create/' method='post'>
        <p><input type='text' name='title' placeholder='title'></p>
        <p><textarea name='body' placeholder='body'></textarea></p>
        <p><input type='submit'></p>
      </form>
    """
        return HttpResponse(HTMLtemplate(article))
    # 데이터를 저장
    elif request.method == "POST":
        title = request.POST["title"]
        body = request.POST["body"]
        newTopic = {"id": nextId, "title": title, "body": body}
        topics.append(newTopic)
        url = "/myapp/topics/read/" + str(nextId)
        nextId = nextId + 1
        return redirect(url)


@csrf_exempt
def delete(request):
    global topics
    if request.method == "POST":
        id = request.POST["id"]
        newTopic = []
        for topic in topics:
            if topic["id"] != int(id):
                newTopic.append(topic)
        topics = newTopic
    return redirect("/myapp/topics/")


@csrf_exempt
def update(request, id):
  # 동일한 URL 요청을 POST, GET 요청 방식에 따라 다르게 처리
  global nextId
  selectedTopic = {}
  if request.method == "GET":
    for topic in topics:
      if topic["id"] == int(id):
        selectedTopic = topic
        break

    article = f"""
      <form action='/myapp/topics/update/{id}' method='post'>
        <p><input type='text' name='title' placeholder='title' value={selectedTopic['title']}></p>
        <p><textarea name='body' placeholder='body'>{selectedTopic['body']}</textarea></p>
        <p><input type='submit'></p>
      </form>
    """
    return HttpResponse(HTMLtemplate(article, id))
  # 데이터를 저장 POST
  elif request.method == "POST":
    title = request.POST["title"]
    body = request.POST["body"]
    for topic in topics:
      if topic["id"] == int(id):
        topic["title"] = title
        topic["body"] = body
    return redirect(f"/myapp/topics/read/{id}")

