from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    """
    Fields:
    - name_test - name of test
    - max_attempt - amount of tries for passing test
    Method:
    - max_points() - calculating of maximum of points by passing test
    """

    name_test = models.CharField(max_length = 50)
    max_attempt = models.PositiveIntegerField(default = 3)

    class Meta:
        verbose_name = 'Test'

    def max_points(self):
        questions = Link.objects.filter(test_id=self)
        links = Link.objects.filter(test_id = self)

        id_questions = []
        answers = []
        all_points = 0
        
        for link in links:
            id_questions.append(link.question_id_id)
        
        for id in id_questions:
            answers.append(Answer.objects.filter(question_id = id))

        for answer in answers:
            for ans in answer:
                all_points += ans.point

        return all_points

    def __str__(self):
        return str(self.name_test)


class Question(models.Model):
    """
    Field:
    - question - name of question
    Method:
    - count_right_answers() - calculating of number of right answers for question
    """

    question = models.CharField(max_length = 150)

    class Meta:
        verbose_name = 'Question'

    def count_right_answers(self):
        answers = Answer.objects.filter(question_id = self)
        count = 0

        for ans in answers:
            if ans.correct:
                count += 1

        return count

    def __str__(self):
        return str(self.question)


class Answer(models.Model):
    """
    Fields:
    - question_id - name of question for answers
    - answer - name of answer
    - correct - indicator of answer correctness for question
    - point - number of points of answer
    """

    question_id = models.ForeignKey(Question, on_delete = models.CASCADE)
    answer = models.CharField(max_length = 50)
    correct = models.BooleanField(default = False)
    point = models.FloatField(default = 0)

    class Meta:
        verbose_name = 'Answer'

    def __str__(self):
        return str(self.answer)


class Link(models.Model):
    """
    Fields:
    - test_id - name of tests
    - question - name of question
    """

    test_id = models.ForeignKey(Test, on_delete = models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Link'

    def __str__(self):
        return str(self.test_id)

class UserTest(models.Model):
    """
    Fields:
    - user_id - name of user
    - test_id - name of test
    - right_answer - number of right answers
    - wrong_answer - number of wrong answers
    - point - number of points
    - mark - mark as result of passing test
    - count_attempts - number of passing attempts
    """

    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    test_id = models.ForeignKey(Test, on_delete = models.CASCADE)
    right_answer = models.PositiveIntegerField(default = 0)
    wrong_answer = models.PositiveIntegerField(default = 0)
    point = models.FloatField(default = 0)
    mark = models.PositiveIntegerField(default = 2)
    count_attempts = models.PositiveIntegerField(default = 0)

    class Meta:
        verbose_name = 'User test'

    def __str__(self):
        return str(self.user_id)
