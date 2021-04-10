from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.core import serializers

from .models import Question, Choice

def index(request) :
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {
        'latest_question_list' : latest_question_list
    })

def details(request, question_id) :
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/details.html', {
        'question' : question
    })

def results(request, question_id) :
    question = Question.objects.get(pk = question_id)
    return render(request, 'polls/results.html', {
        'question' : question
    })

def vote(request, question_id) :
    question = get_object_or_404(Question, pk = question_id)
    try :
        selected_choice = question.choice_set.get(pk = int(request.POST['choice']))
    except (KeyError, Choice.DoesNotExist) :
        return render(request, 'polls/details.html', {
            'question' : question,
            'error_message' : "You didn't select a Choice."
        })
    else :
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args = [question_id]))
# Create your views here.
