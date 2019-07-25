from django import template

register = template.Library()

@register.filter
def deneme(isim1, isim2):
    print(isim1, isim2)
    return True
