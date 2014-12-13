from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from hackEdukate.questions.models import Question, Answer
from hackEdukate.questions.forms import QuestionForm, AnswerForm
from hackEdukate.activities.models import Activity
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from hackEdukate.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from hackEdukate.questions.bing_search import run_query
from django.template import RequestContext
from django.shortcuts import render_to_response

@login_required
def _questions(request, questions, active):
    paginator = Paginator(questions, 10)
    page = request.GET.get('page')

    context_dict = {'questions': questions, 'active': active}

    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        #query = request.POST['query'].strip()
        query = request.POST.get('query')
        if query:
            result_list = run_query(query)
            context_dict['result_list'] = result_list

    return render(request, 'questions/questions.html', context_dict)

@login_required
def questions(request):
    return unanswered(request)

@login_required
def answered(request):
    questions = Question.get_answered()
    return _questions(request, questions, 'answered')

@login_required
def unanswered(request):
    questions = Question.get_unanswered()
    # questions = Question.order_by('-favorites').get_unanswered()    
    return _questions(request, questions, 'unanswered')

@login_required
def all(request):
    questions = Question.objects.order_by('-favorites').all()
    # questions = Question.objects.all()    
    return _questions(request, questions, 'all')

@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
           question = Question()
           question.user = request.user
           question.title = form.cleaned_data.get('title')
           question.description = form.cleaned_data.get('description')
           question.save()
           urls = form.cleaned_data.get('urls')
           question.create_urls(urls)
           return redirect('/questions/')
        else:
            return render(request, 'questions/ask.html', {'form': form})        
    else:
        form = QuestionForm()
    return render(request, 'questions/ask.html', {'form': form})

@login_required
def question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    form = AnswerForm(initial={'question': question})
    return render(request, 'questions/question.html', {'question': question, 'form': form})

@login_required
def answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            user = request.user
            answer = Answer()
            answer.user = request.user
            answer.question = form.cleaned_data.get('question')
            answer.description = form.cleaned_data.get('description')
            answer.save()
            user.profile.notify_answered(answer.question)
            return redirect(u'/questions/{0}/'.format(answer.question.pk))
        else:
            question = form.cleaned_data.get('question')
            return render(request, 'questions/question.html', {'question': question, 'form': form})
    else:
        return redirect('/questions/')

@login_required
@ajax_required
def accept(request):
    answer_id = request.POST['answer']
    answer = Answer.objects.get(pk=answer_id)
    user = request.user
    try:
        user.profile.unotify_accepted(answer.question.get_accepted_answer()) # answer.accept cleans previous accepted answer
    except Exception, e:
        pass
    if answer.question.user == user:
        answer.accept()
        user.profile.notify_accepted(answer)
        return HttpResponse()
    else:
        return HttpResponseForbidden()

@login_required
@ajax_required
def vote(request):
    answer_id = request.POST['answer']
    answer = Answer.objects.get(pk=answer_id)
    vote = request.POST['vote']
    user = request.user
    activity = Activity.objects.filter(Q(activity_type=Activity.UP_VOTE) | Q(activity_type=Activity.DOWN_VOTE), user=user, answer=answer_id)
    if activity:
        activity.delete()
    if vote in [Activity.UP_VOTE, Activity.DOWN_VOTE]:
        activity = Activity(activity_type=vote, user=user, answer=answer_id)
        activity.save()
    return HttpResponse(answer.calculate_votes())

@login_required
@ajax_required
def favorite(request):
    question_id = request.POST['question']
    question = Question.objects.get(pk=question_id)
    user = request.user
    activity = Activity.objects.filter(activity_type=Activity.FAVORITE, user=user, question=question_id)
    if activity:
        activity.delete()
        user.profile.unotify_favorited(question)
    else:
        activity = Activity(activity_type=Activity.FAVORITE, user=user, question=question_id)
        activity.save()
        user.profile.notify_favorited(question)
    return HttpResponse(question.calculate_favorites())

# @login_required
# @ajax_required
def isearch(request):
    context = RequestContext(request)
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render_to_response('questions/isearch.html', {'result_list': result_list}, context)  
    # return render_to_response('questions/questions.html', {'result_list': result_list}, context)

def auto_add_page(request):
    context = RequestContext(request)
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET['description']
        url = request.GET['url']
        title = request.GET['title']        
        # title = request.GET['title'][0 :10]
        print cat_id
        print url
        print title
        print 909       
        # if cat_id:
            # category = Category.objects.get(id=int(cat_id))
        # p = Page.objects.get_or_create(category=category, title=title, url=url)
        p = Question.objects.get_or_create(description=cat_id, title=title, user_id=1)
            # pages = Page.objects.filter(category=category).order_by('-views')

            # Adds our results list to the template context under name pages.
        context_dict['questions'] = questions

    return render_to_response('questions/questions.html', context_dict, context)  

