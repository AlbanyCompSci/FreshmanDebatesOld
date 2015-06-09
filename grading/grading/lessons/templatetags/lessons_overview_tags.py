from django import template
from lessons.models import Response

register = template.Library()


@register.filter
def answered_count(questions, user):
    count = 0
    for q in questions:
        r = Response.objects.filter(question=q, answerer=user)
        if len(r) > 0:
            count += 1
    return count
