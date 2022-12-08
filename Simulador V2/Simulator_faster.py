from turtle import *
from random import *
from time import *
import csv

#Tutle Configurations
tracer(0, 0)
hideturtle()
bgcolor('black')

def person(person):
    """Draws all people in the simulation
       infected: red and upsidedown (colorblind people)
       healthy: green
       imune: gray
       vacinated: Blue"""
    
    xloc = people[person]['xloc']
    yloc = people[person]['yloc']
    up()
    goto(xloc,yloc)
    down()
    width(3)
    color(people[person]['color'])
    begin_fill()
    if people[person]['color'] == 'red':
        setheading(180)
    else:
        setheading(0)

    #body
    right(90)
    fd(12)

    backward(9)

    #right arm
    left(35)
    fd(8)

    backward(8)
    right(35)

    #left arm
    right(35)
    fd(8)

    backward(8)
    left(35)
    fd(12)

    #right leg
    left(25)
    fd(10)

    backward(10)
    right(25)

    #right leg
    right(25)
    fd(10)

    up()
    lt(25 + 90)
    goto(xloc,yloc)
    down()

    #head

    circle(3, 360)

    end_fill()
   
def chance_generator(x):
    """ determine if something will happen or not based on the chance"""
    if randint(1, 100) <= x:
 
        return True
    return False

def first_infected(num_infected):
    """infect the first people"""
    for _ in range(num_infected):
        person = randint(1,num_people)
        people[person]["infected"] = True
        people[person]['color'] = 'red'

def die_or_recover(chance_of_death, infection_duration,person):
    """Kills or recover
       Death Conditions:
       - age > 50 years
       - infected"""
    if people[person]['age'] >= 50 * 52: #died of age
        lists['death_list'].append(person)
        data['total_death'] =+1
    if people[person]['time_infected'] >= infection_duration and chance_generator(chance_of_death): #died to the infection
        lists['death_list'].append(person)
        data['total_death'] =+1
    elif people[person]['time_infected'] >= infection_duration: #recovered
        people[person]['remaining_imunity'] = 52
        people[person]['infected'] = False
        people[person]['time_infected'] = 0
        people[person]['color'] = 'gray'
        data['total_recovered'] += 1


def time_pass(person):
    """Updates some stats such as age, time infected, remaming immunity"""
    people[person]['age'] += 1
    if people[person]['color'] == 'gray':
        people[person]['remaining_imunity'] -= 1
    if people[person]['infected']:
        people[person]['time_infected'] += 1

def remove_imunity(person):
    """Removes a person imunity when her remaning time imunes get to zero"""
    if people[person]['color'] == 'gray' and people[person]['remaining_imunity'] <= 0:
        people[person]['remaining_imunity'] = 0
        people[person]['color'] = 'green'    

def infect(chance_of_infection, distance_to_infection,person):
    """for every healthy person check if there is someone infected nearby
       if there is someone infected try to infect the person """

    for infected in people:
        if people[person]['color'] == 'green' and people[infected]['infected']:
            healthy_xloc = people[person]['xloc']
            healthy_yloc = people[person]['yloc']
            infected_xloc = people[infected]['xloc']
            infected_yloc = people[infected]['yloc']
            
            xrange = healthy_xloc - distance_to_infection <= infected_xloc <= healthy_xloc + distance_to_infection
            yrange = healthy_yloc - distance_to_infection <= infected_yloc <= healthy_yloc + distance_to_infection

            if xrange and yrange and chance_generator(chance_of_infection):
                lists['infected_list'].append(person)


def move_person(person):
    """Make the people walk"""
    people[person]['angle'] += randint(-90,90)
    xloc = people[person]['xloc'] 
    yloc = people[person]['yloc'] 

    up()
    goto(xloc,yloc)
    right(people[person]['angle'])
    fd(randint(5,10))
    people[person]['xloc'] = pos()[0]
    people[person]['yloc'] = pos()[1]


    while (people[person]['xloc'] > 300 or people[person]['xloc'] < -300 
            or people[person]['yloc'] > 300  or people[person]['yloc'] < -300):
        if people[person]['xloc'] > 300:
            setheading(180)
        elif people[person]['xloc'] < -300:
            setheading(0)
        elif people[person]['yloc'] > 300:
            setheading(270)
        elif people[person]['yloc'] < -300:
            setheading(90)
        fd(30)
        people[person]['xloc'] = pos()[0]
        people[person]['yloc'] = pos()[1]
    setheading(0)
    down()

def pop_growth(person):
    """evey healthy person has 1% chance of leaving decendents until populations caps at 300"""
    if len(people) >= 300:
        return
    elif not(people[person]['infected']) and len(lists['newborn_list']) == 0 and chance_generator(1):
           lists['newborn_list'].append(sorted(list(people.keys()))[-1] + 1)
    elif not(people[person]['infected']) and len(lists['newborn_list']) != 0 and chance_generator(1):
            lists['newborn_list'].append(lists['newborn_list'][-1] + 1)

def vacinated(tent_location):
    """Vacinates a person if they are on top of the vacine tent"""
    if vacine:

        for person in people:
            person_xloc = people[person]['xloc']
            person_yloc = people[person]['yloc']

            if (tent_location[0] - 25 <= person_xloc <= tent_location[0] + 25 and
                tent_location[1] - 25 <= person_yloc <= tent_location[1] + 25 and
                (people[person]['color'] == 'green' or people[person]['color'] == 'gray')):
                people[person]['color'] = 'blue'
                people[person]['remaining_imunity'] = 10**10
                
                data['total_vacinated'] += 1
            
def vacine_tent(tent_location):
    """Draws the vacine tent"""
    up()
    goto(tent_location[0] + 25, tent_location[1] + 25)
    setheading(0)
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
    goto(tent_location[0]+2,tent_location[1])
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

    up()
    goto(tent_location[0] - 25,tent_location[1] - 25 )
    down()
    goto(tent_location[0] - 25,tent_location[1] + 25 )
    goto(tent_location[0] + 25,tent_location[1] + 25 )
    goto(tent_location[0] + 25,tent_location[1] - 25 )

def datagatherer():
    """Updates the data that will be saved for the graphs"""
    data['num_infected'] = 0
    data['num_healthy'] = 0
    data['num_vacinated'] = 0
    data['num_imunes'] = 0

    for person in people:
        if people[person]['color'] == 'red':
            data['num_infected'] +=1
        if people[person]['color'] == 'green':
            data['num_healthy'] +=1
        if people[person]['color'] == 'blue':
            data['num_vacinated'] +=1
        if people[person]['color'] == 'gray':
            data['num_imunes'] +=1

    data['total_death'] = 0
    data['total_population'] = data['num_infected'] + data['num_healthy'] + data['num_vacinated'] + data['num_imunes']
    data['total_vacinated'] =  0 #data obtained on vacinated functions
    data['total_recovered'] = 0
    data['total_infected'] = 0
    data['week'] += 1

def update_people():
    
    data['total_infected'] = len(lists['infected_list'])
    for person in lists['infected_list']:
        people[person]['infected'] = True
        people[person]['color'] = 'red'
        data['total_infected'] += 1
    
    for baby in lists['newborn_list']:
        people[baby] = {'age': 0, 'remaining_imunity': 0, "infected": False, "time_infected": 0, 'color':'green', 'xloc': randint(-300, 300), 'yloc': randint(-300, 300), 'angle':0}

    for person in lists['death_list']:
        del people[person]  

    lists['death_list'] = []
    lists['infected_list'] = []
    lists['newborn_list'] = []

fieldnames = ['num_infected', 'num_healthy', 'num_imunes', 'num_vacinated', 'total_population',
              'week', 'total_infected', 'total_death', 'total_recovered', 'total_vacinated'
              ]

with open('dados_simulacao.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()


#obtaing parameters for the simulation
resp = textinput('Presets', 'Want to load a pre-sets? (y or n)')

if resp == 'y':
    num_people = 150  #number of people in the begin
    num_first_infected = 10  #how many people are initially infected
    chance_of_death = 80  #how deadly is the virus (0 <= x <=100)
    infectiousness = 90  #chance of being infected (0 <= x <=100)
    distance_to_infection  = 35  #distance to get infected
    infection_duration = 90  #for how long the person stays infected (0 <= x <=100)
    vacine = True # is there a vacinned in the simulation

# Parameters set by input
else:
    num_people = int(numinput('Number of people','Number of people in the simulation: ', maxval=300))
    num_first_infected = int(numinput('Number of pacients 0s','Number of pacients 0s: '))
    chance_of_death = numinput("How deadly is the virus", " How deadly is the virus? (0 <= x <=1): ") * 100
    infectiousness = numinput('infectiousness ', 'What is the chance of being infected? (0 <= x <=1): ') * 100
    distance_to_infection = numinput('Infection Distance','What is the distace to get infected: ')
    infection_duration = numinput('Infection Durantion', ' For How long a person stay infected ? (0 <= x <=100 days): ')
    vacine = bool(numinput("Vacine Settings","Is there a Vacine? (1 or 0):"))


#simulation
people = {}
for person_code in list(range(1, num_people + 1)):
    people[person_code] = {'age': 0, 'remaining_imunity': 0, "infected": False, "time_infected": 0, 'color':'green', 'xloc': randint(-300, 300), 'yloc': randint(-300, 300), 'angle':0}

data = {
        'num_infected': 0,
        'num_healthy': 0,
        'num_imunes': 0,
        'num_vacinated': 0,
        'total_population': 0,
        'week': 0,
        'total_infected': 0,
        'total_death': 0,
        'total_recovered': 0,
        'total_vacinated':0,


}
lists = {
        'death_list':[],
        'infected_list':[],
        'newborn_list':[]
}
first_infected(num_first_infected)

if vacine:
    tent_location = (randint(-250,250),randint(-250,250))

while len(people) > 0:
    clear()
    if vacine:
        vacine_tent(tent_location)
        vacinated(tent_location)
    for person_num in people:
        move_person(person_num)
        infect(chance_of_death,distance_to_infection,person_num)
        time_pass(person_num)
        die_or_recover(chance_of_death,infection_duration,person_num)
        remove_imunity(person_num)
        pop_growth(person_num)
        person(person_num)
    update_people()
    update()
    with open('dados_simulacao.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writerow(data)
        datagatherer()
    
    if data['num_infected'] == 0 and data['total_population'] != 0:
        break
else:
    print("The disease killed everyone")
if data['num_infected'] == 0 and data['total_population'] != 0:
    print("The disease was erradicated")
done()