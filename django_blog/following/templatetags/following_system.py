from django import template

register = template.Library()


@register.filter
def deneme(isim1, isim2):
    # print(isim1, isim2)
    # return (isim1, isim2)
    pass


@register.filter
def who_is_my_followed(user, my_followed):
    if user.username in my_followed:
        return True
    return False
