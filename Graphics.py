import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np

'''
Parte inspirada no video https://www.youtube.com/watch?v=Ercd-Ip5PfQ
'''
fig = plt.figure()
popu = plt.subplot(211)
stat = plt.subplot(212)
fig.suptitle('Statistics')

barwidth = 0.25
n_mortos=[0]
n_casostotais=[0]
n_curados=[0]

counterweek = 0
lastweek = 0

# Função que plota o grafico
def grafico(i):
    global barwidth, n_mortos, n_casostotais, n_curados ,counterweek, lastweek
    
    # Puxa os dados para esse arquivo
    dados = pd.read_csv('dados_simulacao.csv')
    dados_infectados = dados['dados_infectados']
    dados_saudaveis = dados['dados_saudaveis']
    dados_imunes = dados['dados_imunes']
    dados_total = dados['dados_total']
    dados_duracao = dados['dados_duracao']
    atual_mortos = dados['n_mortos']
    atual_casostotais = dados['n_casostotais']
    atual_curados = dados['n_curados']
    dados_vacinated = dados['dados_vacinated']

    
    #get the data to the bars graph


    
    
    if counterweek > 3:
        if len(n_curados) == 13:
            n_mortos=[0]
            n_casostotais=[0]
            n_curados=[0]
        n_mortos.append(abs(atual_mortos.iloc[-4]-atual_mortos.iloc[-1])),
        n_casostotais.append(abs(atual_casostotais.iloc[-4]-atual_casostotais.iloc[-1]))
        n_curados.append(abs(atual_curados.iloc[-4]-atual_curados.iloc[-1]))
        counterweek = 0
  

    if dados_duracao.iloc[-1] != lastweek:       
        counterweek +=1

    lastweek = dados_duracao.iloc[-1]
  

    # Set position of bar on X axis
    br1 = np.arange(len(n_mortos))
    br2 = [x-0.25 + barwidth for x in br1]
    br3 = [x + barwidth for x in br2]

    

    '''
    #Get the data to the line graph
    n_mortos, n_casostotais, n_curados = atual_mortos, atual_casostotais, atual_curados
    '''    

    # Limpa os eixos
    popu.cla()
    stat.cla()


    # Plota o grafico
    popu.set_title('Populations')
    popu.plot(dados_duracao, dados_infectados,'red', label='Infected')
    popu.plot(dados_duracao, dados_saudaveis, 'green',linestyle='dotted', label='Healthy')
    popu.plot(dados_duracao, dados_imunes, 'gray', label='Imunes')
    popu.plot(dados_duracao, dados_vacinated, 'blue', label='Vacinated')
    popu.plot(dados_duracao, dados_total, 'gold', label='Total')
    popu.set_ylim(0,310)
    popu.set_xlabel("Weeks")
    popu.set_ylabel("# of people")

    for var in (dados_imunes,dados_saudaveis, dados_total, dados_infectados):
        popu.annotate('%0.2f' % var.max(), xy=(1, var.max()), xytext=(8, 0), 
                 xycoords=('axes fraction', 'data'), textcoords='offset points')

    
    popu.legend(loc='upper left')


    stat.set_title('+ Data')


    #Plot the data as line graph
    stat.bar(br1-0.25 , n_mortos, color='orange', width = barwidth , label = '# of Deads')    
    stat.bar(br2, n_casostotais,color='black', width = barwidth, label = '# of new cases')
    stat.bar(br3, n_curados, color='purple', width = barwidth , label = '# of recovered')
    stat.set_xlim([0,13])
    #stat.set_xticklabels("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec",)
    stat.set_xlabel("Month")
    stat.set_ylabel("# of People")
    #stat.set_xticks([r + barwidth for r in range(len(n_mortos)-1)], ['january','february', 'march','april','may', 'june','july', 'august', 'september', 'october', 'november', 'december'])


    '''
    #plot the data in line graph
    stat.plot(dados_duracao,n_mortos,'red', label = 'Número de mortos')
    stat.plot(dados_duracao,n_casostotais,'gray', label = 'Número de casos totais')
    stat.plot(dados_duracao,n_curados,'green',linestyle='dashed', label = 'Número de casos curados')
    '''

    stat.legend(loc='upper left')

# executa a animação
ani = FuncAnimation(fig , grafico, interval=100)
plt.show()
