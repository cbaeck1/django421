from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer

@login_required(login_url='common:login')
def answerCreate(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  if request.method == "POST":
    form = AnswerForm(request.POST)
    if form.is_valid():
      answer = form.save(commit=False)
      answer.author = request.user  # author 속성에 로그인 계정 저장
      answer.create_date = timezone.now()
      answer.question = question
      answer.save()
      # 앵커 적용
      # return redirect("myapp:questionDetail", question_id=question.id) 
      return redirect('{}#answer_{}'.format(
        resolve_url('myapp:questionDetail', question_id=question.id), answer.id))
  else:
    # 로그인 시에 전달된 next 파라미터 때문에 로그인 후에 답변등록 URL인 /answer/create가 GET 방식으로 호출되기 때문    
    form = AnswerForm()

  # return HttpResponseNotAllowed("Only POST is possible.")
  context = {"question": question, "form": form}
  return render(request, "myapp/question_detail.html", context)
    # 
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # return redirect('myapp:questionDetail', question_id=question.id)


@login_required(login_url='common:login')
def answerModify(request, answer_id):
  answer = get_object_or_404(Answer, pk=answer_id)
  if request.user != answer.author:
    messages.error(request, '수정권한이 없습니다')
    return redirect('myapp:questionDetail', question_id=answer.question.id)
  
  if request.method == "POST":
    form = AnswerForm(request.POST, instance=answer)
    if form.is_valid():
      answer = form.save(commit=False)
      answer.modify_date = timezone.now()
      answer.save()
      # 앵커 적용
      # return redirect('myapp:questionDetail', question_id=answer.question.id)
      return redirect('{}#answer_{}'.format(
        resolve_url('myapp:questionDetail', question_id=answer.question.id), answer.id))      
    
  else:
    form = AnswerForm(instance=answer)
    
  context = {'answer': answer, 'form': form}
  return render(request, 'myapp/answer_form.html', context)

@login_required(login_url='common:login')
def answerDelete(request, answer_id):
  answer = get_object_or_404(Answer, pk=answer_id)
  if request.user != answer.author:
    messages.error(request, '삭제권한이 없습니다')
  else:
    answer.delete()
  return redirect('myapp:questionDetail', question_id=answer.question.id)

@login_required(login_url='common:login')
def answerVote(request, answer_id):
  answer = get_object_or_404(Answer, pk=answer_id)
  if request.user == answer.author:
    messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
  else:
      answer.voter.add(request.user)
  # 앵커 적용
  # return redirect("myapp:questionDetail", question_id=answer.question.id) 
  return redirect('{}#answer_{}'.format(
    resolve_url('myapp:questionDetail', question_id=answer.question.id), answer.id))
