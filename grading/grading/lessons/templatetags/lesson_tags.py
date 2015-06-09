from django import template
from lessons.models import Response

register = template.Library()


@register.filter
def response_text(question, user):
    try:
        return question.response_set.get(answerer=user).text
    except Response.DoesNotExist:
        return ''


@register.filter
def response_comment(question, user):
    try:
        return question.response_set.get(answerer=user).comment
    except Response.DoesNotExist:
        return None


@register.filter
def response_is_seen(question, user):
    try:
        return question.response_set.get(answerer=user).seen
    except Response.DoesNotExist:
        return False


@register.filter
def response_id(question, user):
    try:
        return question.response_set.get(answerer=user).id
    except Response.DoesNotExist:
        return None


@register.filter
def only_responses_in_class(responses, lesson):
    return [r for r in responses if r.lesson == lesson]
