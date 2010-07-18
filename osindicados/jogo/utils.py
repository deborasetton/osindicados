import random

def sortearAlternativas(pergunta):
    alternativas = [pergunta.altCorreta, pergunta.altIncorreta1, pergunta.altIncorreta2, pergunta.altIncorreta3, pergunta.altIncorreta4]
    random.shuffle(alternativas)
    return alternativas