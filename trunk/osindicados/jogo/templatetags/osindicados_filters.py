from django import template

register = template.Library()

@register.filter
def faltam(value):
    """
    Recebe o valor de perguntas ja respondidas e retorna
    a quantidade de perguntas que faltam para finalizar 
    a partida. Por enquanto, sao 5 perguntas para terminar.
    """
    return (5 - int(value))