from django import template

register = template.Library()

@register.simple_tag
def get_companion(usr_prf, chat):
    for u in chat.Contacts.all():
        # alleen de eerste wordt hier gereturnd
        if u != usr_prf:
            return u
    return None