import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np

fig = plt.figure()
popu = plt.subplot(211)
stat = plt.subplot(212)
fig.suptitle('Statistics')

barwidth = 0.25

# Stores the informatio from the simulation
info = {
        'num_infected': 0,
        'num_healthy': 0,
        'num_imunes': 0,
        'num_vacinated': 0,
        'total_population': 0,
        'week': 0,
        'total_infected': 0,
        'total_death': 0,
        'total_recovered': 0,
        'total_vacinated':0

}

# Store some the data in a montly and yearly format
data_yearly = {
            'monthly_death': [0,0,0,0],
            'monthy_infected': [0,0,0,0],
            'monthy_recovered': [0,0,0,0],
            'monthy_vacinated': [0,0,0,0],
            'monthly_vacinated': [0,0,0,0],

            'yearly_death': [0,0,0,0,0,0,0,0,0,0,0,0,0],
            'yearly_infected': [0,0,0,0,0,0,0,0,0,0,0,0,0],
            'yearly_recovered': [0,0,0,0,0,0,0,0,0,0,0,0,0],
            'yearly_vacinated': [0,0,0,0,0,0,0,0,0,0,0,0,0]
            }

month = 0
year = 0
last_week = 0

def graph(_):
    global month, year, last_week

    # read the file and saves into into the dictonary
    data = pd.read_csv('dados_simulacao.csv')
    info['num_infected'] = data['num_infected']
    info['num_healthy'] = data['num_healthy']
    info['num_imunes'] = data['num_imunes']
    info['num_vacinated'] = data['num_vacinated']
    info['week'] = data['week']
    info['total_population'] = data['total_population']
    info['total_infected'] = data['total_infected']
    info['total_death'] = data['total_death']
    info['total_recovered'] = data['total_recovered']
    info['total_vacinated'] = data['total_vacinated']

    #saves the data of the month
    if last_week != info['week'].iloc[-1]:

        #resets the yearly data
        if year >= 12:
            data_yearly['yearly_death'] = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            data_yearly['yearly_infected'] = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            data_yearly['yearly_recovered'] = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            data_yearly['yearly_vacinated'] = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            print("Reset")
            year = 0
        
        # add a month to the year and resets the month
        if month >= 4:
            data_yearly['yearly_death'][year] = (sum(data_yearly['monthly_death']))
            data_yearly['yearly_infected'][year] = (sum(data_yearly['monthy_infected']))
            data_yearly['yearly_recovered'][year] = (sum(data_yearly['monthy_recovered']))
            data_yearly['yearly_vacinated'][year] = (sum(data_yearly['monthly_vacinated']))

            data_yearly['monthly_death'] = [0,0,0,0]
            data_yearly['monthly_infected'] = [0,0,0,0]
            data_yearly['monthly_recovered'] = [0,0,0,0]
            data_yearly['monthly_vacinated'] = [0,0,0,0]
            month = 0
            year += 1

        #add a week to the month
        data_yearly['monthly_death'][month] = (info['total_death'].iloc[-1])
        data_yearly['monthy_infected'][month] = (info['total_infected'].iloc[-1])
        data_yearly['monthy_recovered'][month] = (info['total_recovered'].iloc[-1])
        data_yearly['monthy_vacinated'][month] = (info['total_vacinated'].iloc[-1])


        month += 1
    #ensure that the same week is not considered twice in the same month
    last_week = info['week'].iloc[-1]

    #defines the x positions for the bars
    br1 = np.arange(0.75,len(data_yearly['yearly_death']))
    br2 = [x + barwidth for x in br1]
    br3 = [x + barwidth for x in br2]


    # Clears the figures
    popu.cla()
    stat.cla()

    # plots the informations about each population
    popu.set_title('Populations')
    popu.plot(info['week'],info['num_infected'],'red', label='Infected')
    popu.plot(info['week'],info['num_healthy'], 'green',linestyle='dotted', label='Healthy')
    popu.plot(info['week'],info['num_imunes'], 'gray', label='Imunes')
    if info['num_vacinated'].iloc[-1] != 0:
        popu.plot(info['week'],info['num_vacinated'], 'blue', label='Vacinated')
    popu.plot(info['week'],info['total_population'], 'gold', label='Total')
    
    # Writes the number of people of each population
    popu.text(info['week'].iloc[-1]+ 5, info['num_infected'].iloc[-1]+ 10, f'{info["num_infected"].iloc[-1]}', color='red')
    popu.text(info['week'].iloc[-1]+ 5, info['num_healthy'].iloc[-1]+ 10, f'{info["num_healthy"].iloc[-1]}', color='green')
    popu.text(info['week'].iloc[-1]+ 5, info['num_imunes'].iloc[-1]+ 10, f'{info["num_imunes"].iloc[-1]}', color='gray')
    if info['num_vacinated'].iloc[-1] != 0:
        popu.text(info['week'].iloc[-1]+ 5, info['num_vacinated'].iloc[-1]+ 10, f'{info["num_vacinated"].iloc[-1]}', color='blue')

    popu.text(info['week'].iloc[-1]+ 5, info['total_population'].iloc[-1]+ 10, f'{info["total_population"].iloc[-1]}', color='gold')

    for week in range(0,info['week'].iloc[-1],50*52):
        popu.axvline(week,color = 'black')
        popu.text(week+ 5, 250,f'{week/52:.0f} years')
    
    popu.set_ylim(0,310)
    popu.set_xlabel("Weeks")
    popu.set_ylabel("# of people")

    popu.legend(loc='upper left')


    # Plots the yearly data
    stat.set_title('+ Data')

    stat.bar(br1 , data_yearly['yearly_death'], color='black', width = barwidth , label = '# of Deads')    
    stat.bar(br2, data_yearly['yearly_infected'],color='orange', width = barwidth, label = '# of new cases')
    stat.bar(br3, data_yearly['yearly_recovered'], color='teal', width = barwidth , label = '# of recovered')
    stat.set_xlim([0.5,12.5])
    stat.set_xticks(range(1,13))
    stat.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
    stat.set_xlabel("Month")
    stat.set_ylabel("# of People")

    stat.legend(loc='best')


ani = FuncAnimation(fig , graph, interval=1)
plt.show() 