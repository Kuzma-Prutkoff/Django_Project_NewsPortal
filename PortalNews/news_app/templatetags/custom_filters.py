from django import template

register = template.Library()
bad_words = ['война', 'Война', 'войны', 'войне', 'войной', 'войну', 'мир', 'Мир', 'МИР', 'миром', 'миру', 'миры']

@register.filter()
def censor(text):
    text_list = text.split()
    for word in text_list:
        if word in bad_words:
            text = text.replace(word, word[0] + (len(word) - 1) * '*')
    return text


