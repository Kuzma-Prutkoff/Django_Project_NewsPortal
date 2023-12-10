from django import template
import string

register = template.Library()
bad_words = ['война', 'войны', 'войне', 'войной', 'войну', 'мир', 'МИР', 'миром', 'миру', 'миры']

@register.filter()
def censor(text):
    text_list = text.split()
    censored_text_list = []
    for word in text_list:
        clean_word = ''.join(s for s in word if s not in string.punctuation)
        if clean_word.lower() in bad_words:
            censored_word = clean_word[0] + (len(clean_word) - 2) * '*' + clean_word[-1]
            censored_text_list.append(word.replace(clean_word, censored_word))
        else:
            censored_text_list.append(word)
    return ' '.join(censored_text_list)
