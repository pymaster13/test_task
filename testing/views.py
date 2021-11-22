from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .models import Test, Question, Answer, Link, UserTest

def SelectTest(request):
    """
    Function for rendering of tests list
    """

    tests = Test.objects.all()
    pages = Paginator(tests, 3)
    context = {'tests_on_page': pages.get_page((request.GET.get('page')))}

    return render(request, 'select_test.html', context)

def TestInfo(request, test_id):
    """
    Function for rendering of information about test
    """

    questions = Link.objects.filter(test_id=test_id)
    test = Test.objects.get(id = test_id)

    user_test, ss = UserTest.objects.get_or_create(user_id = request.user, test_id = test)
    first_question = questions[0].question_id_id
    all_points = test.max_points()
    context = {'test': test, 'count': len(questions), 'first_question': first_question, 'user_test': user_test, 'max_points': all_points}

    return render(request, 'test_info.html', context)

def Testing(request, test_id, question_id):
    """
    Function for passing of test
    """

    if request.method == 'POST':
        if not 'answer' in request.POST:
            return redirect('/test/'+test_id+'/'+question_id+'/')

        test = Test.objects.get(id = test_id)
        user_test, ss = UserTest.objects.get_or_create(user_id = request.user, test_id = test)
        question = Question.objects.get(id = question_id)
        question_right_answers = question.count_right_answers()
        answers_in_request = request.POST.getlist('answer')

        answers = []
        count_right_answers = 0

        if (len(answers_in_request) != 1):
            for answer in answers_in_request:
                 answers.append(Answer.objects.get(id = answer))
        else:
            answer = Answer.objects.get(id = request.POST['answer'])

        miss_answer_points = 0

        if (len(answers_in_request) != 1):
            for ans in answers:
                if ans.correct == True:
                    user_test.point += ans.point
                    miss_answer_points += ans.point
                    count_right_answers += 1
                    user_test.save()

                else:
                    user_test.point -= miss_answer_points
                    user_test.save()

            if count_right_answers == question_right_answers:
                user_test.right_answer +=1
            else:
                user_test.wrong_answer +=1

            user_test.save()

            return redirect('/test/'+test_id+'/'+str(int(question_id)+1)+'/')

        else:

            if answer.correct == True:

                if question_right_answers == 1:
                    user_test.right_answer +=1
                else:
                    user_test.wrong_answer +=1
                user_test.point += answer.point

            else:
                user_test.wrong_answer +=1

            user_test.save()

            return redirect('/test/'+test_id+'/'+str(int(question_id)+1)+'/')

    elif int(question_id) > len(Link.objects.filter(test_id=test_id)):

        links = Link.objects.filter(test_id = test_id)
        test = Test.objects.get(id = test_id)
        user_test = UserTest.objects.get(user_id = request.user, test_id = test)
        all_points = test.max_points()

        if(0.5 <= user_test.point/all_points and user_test.point/all_points < 0.7):
            user_test.mark = 3
            user_test.save()

        elif(0.7 <= user_test.point/all_points and user_test.point/all_points < 0.9):
            user_test.mark = 4
            user_test.save()

        elif(user_test.point/all_points >= 0.9):
            user_test.mark = 5
            user_test.save()

        else:
            user_test.mark = 2
            user_test.save()

        user_test.count_attempts += 1
        user_test.save()

        return redirect('/test/'+test_id+'/result/')

    else:

        test = Test.objects.get(id = test_id)
        user_test, ss = UserTest.objects.get_or_create(user_id = request.user, test_id = test)
        
        if (question_id == '1'):
            user_test.right_answer = 0
            user_test.wrong_answer = 0
            user_test.point = 0
            user_test.mark = 2
            user_test.save()

        questions = Link.objects.filter(test_id = test_id)
        test = Test.objects.get(id = test_id)
        current_question = questions[int(question_id)-1].question_id_id
        name_question = Question.objects.get(id = current_question)
        answers = Answer.objects.filter(question_id = current_question)

        count_correct_answers = 0
        for answer in answers:
            if(answer.correct):
                count_correct_answers = count_correct_answers + 1
        
        context = {'test': test, 'question_id': int(question_id)+1,
            'question': current_question, 'answers': answers, 
            'name_question': name_question, 'count':count_correct_answers}
        
        return render(request, 'testing.html', context)

def TestResult(request, test_id):
    """
    Function for rendering of result information after testing
    """

    test = Test.objects.get(id = test_id)
    user_test = UserTest.objects.get(user_id = request.user, test_id = test)
    all = user_test.right_answer + user_test.wrong_answer
    
    context = {'all':all,'test_name': test, 'right_answer':user_test.right_answer, 
        'point':user_test.point, 'mark':user_test.mark}
    
    return render(request, 'test_result.html', context)
