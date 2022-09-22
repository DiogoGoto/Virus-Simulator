from turtle import *
from random import *
from time import *
import csv

tracer(0, 0)
hideturtle()
bgcolor('black')


# Desenha a pessoa
def pessoa(cor):
    p = pos()
    width(3)
    color(cor)
    begin_fill()
    if cor == 'red':
        setheading(180)
    else:
        setheading(0)

    # corpo
    right(90)
    fd(12)

    backward(9)

    # braço direito
    left(35)
    fd(8)

    backward(8)
    right(35)

    # Braço esquerdo
    right(35)
    fd(8)

    backward(8)
    left(35)
    fd(12)

    # perna direita
    left(25)
    fd(10)

    backward(10)
    right(25)

    # Perna Esquerda
    right(25)
    fd(10)

    up()
    lt(25 + 90)
    goto(p)
    down()

    # cabeça

    circle(3, 360)

    end_fill()


# Gerador de chance
def gerador_chance(x):
    if randint(1, 100) <= x:
        return True
    return False


# Infecta as primeiras pessoas da simulação
def paciente_0(j):
    global people
    global d
    for i in range(1, j + 1):
        people[i][2] = True
        people[i][3] = 0
        people[i][4] = 'red'


# Conta quantos infectados tem
def n_infectado(d):
    cont = 0
    for i in d:
        if d[i][2]:
            cont += 1
    return cont


# Conta quantos saudaveis tem
def n_saudaveis(d):
    cont = 0
    for i in d:
        if not (d[i][2]) and d[i][1] == 0:
            cont += 1
    return cont


# Conta quantos imunes tem
def n_imunes(d):
    cont = 0
    for i in d:
        if d[i][4] == 'gray':
            cont += 1
    return cont

def n_vacinated(d):
    cont = 0
    for i in d:
        if d[i][4] == 'blue':
            cont += 1
    return cont

# decide se a pessoa morre ou vive
def morrer_ou_curar(d, c, a):
    global n_mortos,n_curados
    mortos = []
    for i in d:
        # Cada pessoa vive no máximo 50 anos
        if d[i][0] == 50 * 52:
            # print(i, "morreu de velhice")
            mortos.append(i)
        if d[i][3] > a:  # if tempo infectado > duração da infeção
            # Morte pela Doença
            if d[i][2] and gerador_chance(c):
                mortos.append(i)
                n_mortos+=1
            # Pessoa foi curada
            else:
                d[i][1] = 52
                d[i][2] = False
                d[i][3] = 0
                d[i][4] = 'gray'
                n_curados+=1

    # apaga as pessoas do dicionario
    for i in mortos:
        del (d[i])


# Depois de um ano a pessoa perde a imunidade
def passou_imunidade(d):
    for i in d:
        if d[i][1] == 0 and d[i][4] == 'gray':
            d[i][4] = 'green'


# Cada individuo saudavel tem a chance tem 1% de gerar um filho até a população atigir 300 pessoas
def crescimento_pop():
    global people
    NL = []
    LPeople = []
    for i in people:
        LPeople.append(i)

    for i in people:
        if not (people[i][2]) and gerador_chance(1) and NL == [] and len(people) <= 300:
            NL.append(LPeople[-1] + 1)
        if not (people[i][2]) and gerador_chance(1) and NL != [] and len(people) <= 300:
            NL.append(NL[-1] + 1)

    for i in NL:
        #
        people[i] = [0, 0, False, 0, 'green', randint(-300, 300), randint(-300, 300), 0]
        #            idade,imunidade restante, está doente?,tempo doente, cor, pos x, pos y


# Movimenta a pessoa
def mover(v):
    global people
    for i in people:
        x = people[i]
    # faz um loop com o numero de passos para cada semana como range
    for k in range(100 - v):
        clear()

        # desenha as pessoas apos andar de 6-10 pixels em um angulho aleatorio
        for i in people:
            x = randint(5, 10)
            if k == 0:
                people[i][7] = people[i][7] + int(randint(-90, 90))
            # vai para a posição da pessoa
            up()
            goto(people[i][5], people[i][6])
            down()
            # gira em um angulo aleatorio
            right(people[i][7])
            # da um numero de 'passos' x
            up()
            fd(x)
            down()
            # reajusta o angulo da turtle para 0, em um contexto global
            setheading(0)
            # coleta as cordenadas de cada pessoa
            ln = pos()
            # compara as posições para ver se saiu da tela, se sim manda de volta para (-300,300)
            if ln[0] > 400 or ln[0] < -400 or ln[1] > 325 or ln[1] < -325:
                up()
                if ln[0] > 400:
                    people[i][7] = 180
                if ln[0] < -400:
                    people[i][7] = 0
                if ln[1] > 325:
                    people[i][7] = 90
                if ln[1] < -325:
                    people[i][7] = -90
                down()
                ln = pos()
            # atualiza as cordenadas de x e y no dicionario
            people[i][5] = ln[0]
            people[i][6] = ln[1]

            # desenha a pessoa[i] com a cor de [4]
            pessoa(people[i][4])

            # chama a função infectar que compara as posições dentro de um raio, para assim infectar
            infectar(i, l, a)
            vacinated(people)
        update()


# Infecta as pessoas
def infectar(i, l, b):
    global people, n_casostotais
    for j in people:
        # se uma pessoa está perto o suficente de outra pessoa doente para ser infectada
        a = people[i][5] - l <= people[j][5] <= people[i][5] + l and people[i][6] - l <= people[j][6] <= people[i][
            6] + l
        chance = gerador_chance(b)
        if people[i][4] == 'green' and people[j][2] and a and j != i and chance:
            people[i][2] = True
            people[i][3] = 0
            people[i][4] = 'red'
            n_casostotais += 1


# atuliza os dados do grafico
def dados(d):
    global dados_infectados, dados_saudaveis, dados_imunes, dados_total, dados_duracao, n_mortos, dados_vacinated
    dados_infectados = n_infectado(d)
    dados_saudaveis = n_saudaveis(d)
    dados_imunes = n_imunes(d)
    dados_vacinated = n_vacinated(d)
    dados_total = dados_imunes + dados_infectados + dados_saudaveis + dados_vacinated
    dados_duracao += 1

def vacinated(d):
    for i in d:
        if posx-25 <= d[i][5] <= posx+25 and posy-25 <= d[i][6] <= posy+25 and not(d[i][2]) and d[i][4] != 'blue':
            print(i,"está imunizada")
            d[i][4] = 'blue'
            d[i][1] = 52 * 50

def vacine_tent(posx, posy):
    up()
    goto(posx+25,posy+25)
    down()
    rt(90)
    color('white')
    begin_fill()
    for _ in range(4):
        fd(50)
        rt(90)
    end_fill()

    color('red')
    up()
    goto(posx+2,posy)
    down()

    begin_fill()
    for _ in range(4):
        rt(90)
        fd(15)
        rt(90)
        fd(5)
        rt(90)
        fd(15)
    end_fill()

'''
Código do grafico copiado do video https://www.youtube.com/watch?v=Ercd-Ip5PfQ
'''

# define o nome dos dados a serem salvos
fieldnames = ['dados_infectados', 'dados_saudaveis', 'dados_imunes', 'dados_total', 'dados_duracao','n_mortos', 'n_casostotais','n_curados', 'dados_vacinated']

# Define onde vai ser salvos os dados
with open('dados_simulacao.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

# pre-set dos parametros a serem abordados
resp = textinput('Presets', 'Want to load a pre-sets? (y or n)')

if resp == 'y':
    n = 150  # Número de pessoas
    j = 10  # Número de pacientes 0s
    c = 40  # Quão mortal é o virus (0 <= x <=100)
    a = 80  # Chance de ser contaminado (0 <= x <=100)
    l = 20  # Distancia para infecção
    d = 35  # Duração da infeção (0 <= x <=100)
    v = 97  # Velocidade da simulação (1 <= x <=99)
    m = True

# Parametros de imput variado
else:
    # numinput(title, prompt, default=None, minval=None, maxval=None)
    n = int(numinput('Number of people','Number of people in the simulation: ', maxval=300))
    j = int(numinput('Number of pacients 0s','Number of pacients 0s: '))
    c = numinput("How deadly is the virus", " How deadly is the virus? (0 <= x <=1): ") * 100
    a = numinput('infectiousness ', 'What is the chance of being infected? (0 <= x <=1): ') * 100
    l = numinput('Infection Distance','What is the distace to get infected: ')
    d = numinput('Infection Durantion', ' For How long a person stay infected ? (0 <= x <=100 days): ')
    v = int(numinput('Simulation Speed', ' How fast is the Simulation ?(1 <= x <=99): '))
    m = bool(numinput("Vacine Settings","Is there a Vacine? (1 or 0):"))

# cria o dicionario que contém os dados das pessoas
people = {}

for i in list(range(1, n)):
    people[i] = [0, 0, False, 0, 'green', randint(-300, 300), randint(-300, 300), 0]
    #           idade,imunidade restante, está doente?,tempo doente, cor, pos x, pos y

# Infecta os primeiros pacientes
paciente_0(j)

posx = 0
posy = 0

if m:
    posx = randint(-250,250)
    posy = randint(-250,250)
print(posx,posy)

    

# cria as variaveis que irão salvar os dados para o gráfico
dados_infectados = n_infectado(people)
dados_saudaveis = n_saudaveis(people)
dados_imunes = n_imunes(people)
dados_vacinated = n_vacinated(people)
dados_total = dados_saudaveis + dados_imunes + dados_infectados + dados_vacinated
n_mortos = 0
n_casostotais = j
n_curados = 0
dados_duracao = 0

# loop que executa a simulação
while True:

    # salva os dados em um arquivo .csv
    with open('dados_simulacao.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Define que dados serão salvos e com quais nomes
        info = {
            'dados_infectados': dados_infectados,
            'dados_saudaveis': dados_saudaveis,
            'dados_imunes': dados_imunes,
            'dados_total': dados_total,
            'dados_duracao': dados_duracao,
            'n_mortos': n_mortos,
            'n_casostotais': n_casostotais,
            'n_curados' : n_curados,
            'dados_vacinated' : dados_vacinated

        }

        csv_writer.writerow(info)
        dados(people)


    # Aumenta a idade, diminui o tempo de imunidade e aumenta o tempo decorrido da infecção
    for i in people:
        people[i][0] += 1
        if people[i][4] == 'gray':
            people[i][1] -= 1
        if people[i][2]:
            people[i][3] += 1
    # limpa a tela e mostra as semanas
    clear()
    print('semana: ', dados_duracao)
    print(len(people))

 


    # move todas as pessoas, com suas atualizações de status
    mover(v)

    morrer_ou_curar(people, c, d)
    passou_imunidade(people)
    crescimento_pop()

    # verifica se o numero de infectados é igual a 0 ou se passaram + de 5000 ciclos para parar  a simulação
    if n_infectado(people) == 0:
        clear()
        if m:
            vacine_tent(posx,posy)

        for i in people:
            mover(v)
            print(i, people[i])
        print('a doença foi erradicada na semana', dados_duracao)
        update()
        break
    update()
    sleep(0.1)

done()
