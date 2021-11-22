from django.contrib import admin
from testing.models import Test, Question, Answer, Link, UserTest

admin.site.register(Test)
admin.site.register(Question)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_id', 'answer', 'correct', 'point')

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'test_id', 'question_id')
    list_filter = ('test_id', 'question_id')

@admin.register(UserTest)
class UserTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'test_id', 'right_answer', 'wrong_answer', 'mark')
