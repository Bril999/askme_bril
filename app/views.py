import copy

from django.shortcuts import render
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
    page = paginate(QUESTIONS, request, per_page=5)
    return render(
        request, 'index.html',
        context={'questions': page.object_list, 'page_obj': page}
    )

def hot(request):
    hot_questions = list(QUESTIONS)
    hot_questions.reverse()
    page = paginate(hot_questions, request, per_page=5)
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
    one_question = QUESTIONS[question_id]
    return render(
        request, 'one_question.html',
        context={'item': one_question}
    )


def tag(request, tag_name):
    filtered_questions = [
        question for question in QUESTIONS if tag_name in question['tags']
    ]

    return render(
        request, 'tag.html',
        context={'tag': tag_name, 'questions': filtered_questions}
    )
