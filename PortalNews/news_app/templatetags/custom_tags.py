from django import template

register = template.Library()

#Создаем специальный тег, для того чтобы пагинация и фильтр (по любому полю), работали вместе
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy() #позволяет скопировать все параметры текущего запроса.
    for k, v in kwargs.items():      #просто устанавливаем новые значения, которые нам передали при использовании тега
        d[k] = v
    return d.urlencode()

