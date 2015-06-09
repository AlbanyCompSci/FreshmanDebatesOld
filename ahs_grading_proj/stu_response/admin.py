from stu_response.models import Lesson, Response, Question, Class
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import escape


def get_num_completed(obj):
    return obj.questions.all().count()
get_num_completed.short_description = "Total Questions"


def get_full_name_display(obj):
    return obj.creator.get_full_name() + " (" + obj.creator.username + ")"
get_full_name_display.short_description = "Creator"


class LessonAdmin(admin.ModelAdmin):
    # filter_horizontal = ('questions',)
    date_hierarchy = 'last_edit_date'
    exclude = ('recorded_responses', 'questions', )
    list_display = ("name", get_full_name_display, "last_edit_date", get_num_completed)
    readonly_fields = ('questions_display', "key", 'responses_display',)
    search_fields = ['name', 'creator__username', 'creator__first_name', 'creator__first_name', 'questions__text']

    def questions_display(self, instance):
        questions = mark_safe("<ul>")
        for q in instance.questions.all().order_by('q_num'):
            questions += mark_safe("<li>") + escape(q.__unicode__()) + mark_safe("</li>")
        questions += mark_safe("</ul>")
        return questions
    questions_display.short_description = "Questions"
    questions_display.allow_tags = True

    def responses_display(self, instance):
        responses = ""
        for question in instance.getResponses():
            responses += mark_safe("<ul>")
            for r in question:
                responses += mark_safe("<li>") + escape(r.__unicode__()) + mark_safe("</li>")
            responses += mark_safe("</ul>")
        return responses

    responses_display.short_description = "Responses"
    responses_display.allow_tags = True

admin.site.register(Lesson, LessonAdmin)


class ResponseAdmin(admin.ModelAdmin):
    date_hierarchy = 'edit_date'

admin.site.register(Response, ResponseAdmin)


class QuestionAdmin(admin.ModelAdmin):

    def get_parent_lesson(self, instance):
        return instance.lesson_set.all()[0]
    get_parent_lesson.short_description = "Parent Lesson"
    list_display = ("text", "get_parent_lesson", "q_num")

admin.site.register(Question, QuestionAdmin)


class ClassAdmin(admin.ModelAdmin):
    filter_horizontal = ("students", "teachers", "lessons")
    list_display = ("name", get_full_name_display, "description")
    readonly_fields = ("uid", "creator")
    search_fields = ['name', 'creator__username', 'creator__first_name', 'creator__first_name', 'description']

admin.site.register(Class, ClassAdmin)
