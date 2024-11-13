import copy
from .models import Question, Answer, Profile, Tag
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

QUESTIONS = [
    {
        'title': f'title {i}',
        'id': i,
        'text': f'This is text for question {i}',
        'tags': ['python', 'django']
    } for i in range(30)
]

def paginate(objects_list, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)

    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page
def index(request):
    questions = Question.objects.all()
    page = paginate(questions, request, per_page=5)
    return render(
        request, 'index.html',
        context={'questions': page.object_list, 'page_obj': page}
    )

def hot(request):
    best_questions = Question.objects.hot()
    page = paginate(best_questions, request, per_page=5)

    return render(
        request, 'hot.html',
        context={'questions': page.object_list, 'page_obj': page}
    )
def login(request):
    return render(
        request, 'login.html',
        context={'questions': None}
    )

def signup(request):
    return render(
        request, 'signup.html',
        context={'questions': None}
    )

def ask(request):
    return render(
        request, 'ask.html',
        context={'questions': None}
    )

def settings(request):
    return render(
        request, 'settings.html',
        context={'questions': None}
    )

def question(request, question_id):
    one_question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=one_question)
    return render(
        request, 'one_question.html',
        context={'item': one_question, 'answers': answers}
    )

def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    filtered_questions = Question.objects.filter(tags=tag)

    # Пагинация
    page = paginate(filtered_questions, request, per_page=5)

    return render(
        request, 'tag.html',
        context={'tag': tag_name, 'questions': page.object_list, 'page_obj': page}
    )

def new_questions(request):
    questions = Question.objects.order_by('-created_at')
    page = paginate(questions, request, per_page=5)

    return render(
        request, 'new_questions.html',
        context={'questions': page.object_list, 'page_obj': page}
    )
