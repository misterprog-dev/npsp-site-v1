# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from django.shortcuts import render
from django.conf import settings
from django.views.generic import TemplateView
from commande.models import CommandeModel, DetailsCommandeModel
from medicament.models import Medicament

from geopy import distance
import requests
import json
import os
import io
import fnmatch
from json import load, dump
from deap import base, creator, tools
import random
import time

################### METHODE UTILES POUR LES APPELS DE TRAITEMENT ################## 

def make_dirs_for_file(path):
    '''gavrptw.uitls.make_dirs_for_file(path)'''
    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass


def guess_path_type(path):
    '''gavrptw.uitls.guess_path_type(path)'''
    if os.path.isfile(path):
        return 'File'
    if os.path.isdir(path):
        return 'Directory'
    if os.path.islink(path):
        return 'Symbolic Link'
    if os.path.ismount(path):
        return 'Mount Point'
    return 'Path'


def exist(path, overwrite=False, display_info=True):
    '''gavrptw.uitls.exist(path, overwrite=False, display_info=True)'''
    if os.path.exists(path):
        if overwrite:
            if display_info:
                print(f'{guess_path_type(path)}: {path} exists.')
            os.remove(path)
            return False
        if display_info:
            print(f'{guess_path_type(path)}: {path} existes.')
        return True
    if display_info:
        print(f'{guess_path_type(path)}: {path} n''existe pas.')
    return False


def load_instance(json_file):
    if exist(path=json_file, overwrite=False, display_info=True):
        with io.open(json_file, 'rt', newline='') as file_object:
            return load(file_object)
    return None


def calculate_distance(customer1, customer2):
    '''gavrptw.uitls.calculate_distance(customer1, customer2)'''
    return ((customer1['coordinates']['x'] - customer2['coordinates']['x'])**2 + \
        (customer1['coordinates']['y'] - customer2['coordinates']['y'])**2)**0.5


################## METHODE GENETIQUE ###########################


def ind2route(individual, instance):
    '''gavrptw.core.ind2route(individual, instance)'''
    route = []
    vehicle_capacity = instance['vehicle_capacity']
    depart_due_time = instance['depart']['due_time']
    # Initialize a sub-route
    sub_route = []
    vehicle_load = 0
    elapsed_time = 0
    last_customer_id = 0
    for customer_id in individual:
        # Update vehicle load
        demand = float(instance[f'customer_{customer_id}']['demand'])
        updated_vehicle_load = vehicle_load + demand
        # Update elapsed time
        service_time = instance[f'customer_{customer_id}']['service_time']
        return_time = instance['distance_matrix'][customer_id][0]
        updated_elapsed_time = elapsed_time + \
            instance['distance_matrix'][last_customer_id][customer_id] + float(service_time) + return_time
        # Validate vehicle load and elapsed time
        if (updated_vehicle_load <= vehicle_capacity) and (updated_elapsed_time <= depart_due_time):
            # Add to current sub-route
            sub_route.append(customer_id)
            vehicle_load = updated_vehicle_load
            elapsed_time = updated_elapsed_time - return_time
        else:
            # Save current sub-route
            route.append(sub_route)
            # Initialize a new sub-route and add to it
            sub_route = [customer_id]
            vehicle_load = demand
            elapsed_time = instance['distance_matrix'][0][customer_id] + float(service_time)
        # Update last customer ID
        last_customer_id = customer_id
    if sub_route != []:
        # Save current sub-route before return if not empty
        route.append(sub_route)
    return route


def print_route(route, merge=False):
    '''gavrptw.core.print_route(route, merge=False)'''
    #print(route)
    #print("\n\n")    
    route_str = '0'
    sub_route_count = 0
    for sub_route in route:
        sub_route_count += 1
        sub_route_str = '0'
        for customer_id in sub_route:
            sub_route_str = f'{sub_route_str} - {customer_id}'
            route_str = f'{route_str} - {customer_id}'
        sub_route_str = f'{sub_route_str} - 0'
        if not merge:
            print(f'  Vehicle {sub_route_count} route: {sub_route_str}')
        route_str = f'{route_str} - 0'
    if merge:
        print(route_str)


def eval_vrptw(individual, instance, unit_cost=1.0, init_cost=0, wait_cost=0, delay_cost=0):
    '''gavrptw.core.eval_vrptw(individual, instance, unit_cost=1.0, init_cost=0, wait_cost=0,
        delay_cost=0)'''
    total_cost = 0
    route = ind2route(individual, instance)
    total_cost = 0
    for sub_route in route:
        sub_route_time_cost = 0
        sub_route_distance = 0
        elapsed_time = 0
        last_customer_id = 0
        for customer_id in sub_route:
            # Calculate section distance
            distance = instance['distance_matrix'][last_customer_id][customer_id]
            # Update sub-route distance
            sub_route_distance = sub_route_distance + distance
            # Calculate time cost
            arrival_time = elapsed_time + distance
            time_cost = wait_cost * \
                max(instance[f'customer_{customer_id}']['ready_time'] - arrival_time, 0) + \
                delay_cost * \
                max(arrival_time - instance[f'customer_{customer_id}']['due_time'], 0)
            # Update sub-route time cost
            sub_route_time_cost = sub_route_time_cost + time_cost
            # Update elapsed time
            elapsed_time = arrival_time + \
                float(instance[f'customer_{customer_id}']['service_time'])
            # Update last customer ID
            last_customer_id = customer_id
        # Calculate transport cost
        sub_route_distance = sub_route_distance + instance['distance_matrix'][last_customer_id][0]
        sub_route_transport_cost = init_cost + unit_cost * sub_route_distance
        # Obtain sub-route cost
        sub_route_cost = sub_route_time_cost + sub_route_transport_cost
        # Update total cost
        total_cost = total_cost + sub_route_cost
    fitness = 1.0 / total_cost
    return (fitness, )


def cx_partialy_matched(ind1, ind2):
    '''gavrptw.core.cx_partialy_matched(ind1, ind2)'''
    size = min(len(ind1), len(ind2))
    cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))
    temp1 = ind1[cxpoint1:cxpoint2+1] + ind2
    temp2 = ind1[cxpoint1:cxpoint2+1] + ind1
    ind1 = []
    for gene in temp1:
        if gene not in ind1:
            ind1.append(gene)
    ind2 = []
    for gene in temp2:
        if gene not in ind2:
            ind2.append(gene)
    return ind1, ind2


def mut_inverse_indexes(individual):
    '''gavrptw.core.mut_inverse_indexes(individual)'''
    start, stop = sorted(random.sample(range(len(individual)), 2))
    individual = individual[:start] + individual[stop:start-1:-1] + individual[stop+1:]
    return (individual, )


def run_gavrptw(instance_name, unit_cost, init_cost, wait_cost, delay_cost, ind_size, pop_size, \
    cx_pb, mut_pb, n_gen):
    '''gavrptw.core.run_gavrptw(instance_name, unit_cost, init_cost, wait_cost, delay_cost,
        ind_size, pop_size, cx_pb, mut_pb, n_gen, export_csv=False, customize_data=False)'''
    
    json_data_dir = os.path.join('livraison', 'data')

    json_file = os.path.join(json_data_dir, f'{instance_name}.json')
    instance = load_instance(json_file=json_file)
    if instance is None:
        return
    creator.create('FitnessMax', base.Fitness, weights=(1.0,))
    creator.create('Individual', list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    # Attribute generator
    toolbox.register('indexes', random.sample, range(1, ind_size + 1), ind_size)
    # Structure initializers
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    # Operator registering
    toolbox.register('evaluate', eval_vrptw, instance=instance, unit_cost=unit_cost, \
        init_cost=init_cost, wait_cost=wait_cost, delay_cost=delay_cost)
    toolbox.register('select', tools.selRoulette)
    toolbox.register('mate', cx_partialy_matched)
    toolbox.register('mutate', mut_inverse_indexes)
    pop = toolbox.population(n=pop_size)
   
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # Begin the evolution
    for gen in range(n_gen):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cx_pb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        for mutant in offspring:
            if random.random() < mut_pb:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        # The population is entirely replaced by the offspring
        pop[:] = offspring

    best_ind = tools.selBest(pop, 1)[0]
    print_route(ind2route(best_ind, instance))

    """ resultat = {}
    vehicule = 1
    for route in ind2route(best_ind, instance):
        resultat[vehicule] = route
        vehicule = vehicule + 1 """
    return ind2route(best_ind, instance)
    

 
######################################################################################################
######################################################################################################
######################################################################################################


def get_data_for_maps(request, **kwargs):    
    # Create Routing Model    
    init_point = {
        "0":{
            "adresse": "La Nouvelle PSP Cote D'Ivoire, Abidjan, Côte d'Ivoire",
            "x": "-3,9964039",
            "y": "5,291346000000001"
        },
    }
    commandes = CommandeModel.objects.filter(etat_commande = 1)

    if request.method == "POST":
        nbre_vehicule = request.POST.get("vehicule_number")
        vehicule_capacite = request.POST.get("vehicule_capacite")
        depot_initial = request.POST.get("depot_initial")        
        nom_projet = request.POST.get("nom_projet")

        #depôt initial
        dep = init_point.get(depot_initial)   
        #print(dep) 

        #Graphe
        tableau_ville = {
                "depart": {
                    "adresse": "La Nouvelle PSP Cote D'Ivoire, Abidjan, Côte d'Ivoire",
                    "coordinates":{
                        "x": str(-3.9964039),
                        "y": str(5.291346000000001)
                    },
                    "demand": 0,
                    "due_time": time.time(),
                    "ready_time": 0,
                    "service_time": 0                                                          
                }
            }        
        #Graphe
        tableau_v = {
                0: {
                    "adresse": "La Nouvelle PSP Cote D'Ivoire, Abidjan, Côte d'Ivoire",
                    "x": -3.9964039,
                    "y": 5.291346000000001
                },
            }
        j = 1
        i = 1
        for c in commandes:
            client = c.client  

            #Pour la quantité
            details_c = DetailsCommandeModel.objects.filter(id_commande = c)
            somme_quantite = 0
            for d in details_c:
                med = Medicament.objects.get(id = d.id_medicament.id)
                somme_quantite = somme_quantite + d.quantite_med * med.kilo_paquet
                    
            data = {
                    "adresse": client.ville,
                    "coordinates":{
                        "x": str(client.x),
                        "y": str(client.y)
                    },
                    "demand": str(somme_quantite),
                    "due_time": time.mktime(c.date_livraison.timetuple()),
                    "ready_time": time.mktime(c.date_commande.timetuple()),
                    "service_time": str(c.client.service_time)
                }

            temp = {
                    "adresse": client.ville,
                    "x": client.x,
                    "y":  client.y
                }            
            tableau_v[j] = temp
            j = j + 1        
            
            tableau_ville["customer_"+str(i)] = data
            i = i + 1

        distance_matrix = []

        for ville_i in tableau_v:
            tab = []            
            #print(tableau_ville[ville_i]["x"] + " " + tableau_ville[ville_i]["y"])
            c_1 = (tableau_v[ville_i]["x"], tableau_v[ville_i]["y"])
            #print(c_1)
            originPoint = tableau_v[ville_i]["adresse"]
            for ville_j in tableau_v:
                c_2 = (tableau_v[ville_j]["x"], tableau_v[ville_j]["y"])
                #tab.append(great_circle(c_1, c_2).miles)
                destinationPoint = tableau_v[ville_j]["adresse"]
                r = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?' + 'origins=' + originPoint + '&destinations=' + destinationPoint + '&key=' + 'AIzaSyAemZJQVlVR_26cPHZBSKaC0PoyHcCdboM')
                #print(r.json())
                #print(r.json()['rows'][0]['elements'][0].get('distance'))
                if r.json()['rows'][0]['elements'][0].get('distance'):
                    val = r.json()['rows'][0]['elements'][0].get('distance').get('value')
                    tab.append(val)
                else:
                    tab.append(distance.distance(c_1, c_2).miles * 1000)
            distance_matrix.append(tab)
        
        tableau_ville["distance_matrix"] = distance_matrix
        tableau_ville["max_vehicle_number"] = int(nbre_vehicule)
        tableau_ville["vehicle_capacity"] = int(vehicule_capacite)
        tableau_ville["instance_name"] = nom_projet

        with open('livraison/data/'+ nom_projet +'.json', 'w') as f:           
            json.dump(tableau_ville, f)

        """
        On effectue l'optimisation 
        """      
        random.seed(64)

        instance_name = nom_projet

        unit_cost = 8.0
        init_cost = 100.0
        wait_cost = 1.0
        delay_cost = 1.5

        ind_size = i-1
        pop_size = 100
        cx_pb = 0.85
        mut_pb = 0.02
        n_gen = 100

        resultat = run_gavrptw(instance_name=instance_name, \
            unit_cost=unit_cost, init_cost=init_cost, wait_cost=wait_cost, delay_cost=delay_cost, \
            ind_size=ind_size, pop_size=pop_size, cx_pb=cx_pb, mut_pb=mut_pb, n_gen=n_gen)
        
        donnees_maps = []
        print("\n\n")
        print(tableau_v)
        print("\n\n")
        #print(tableau_v[0]['adresse'])
        #print("\n\n")
        #print(resultat)
        for elt in resultat:
            #print(elt)
            donnee = []
            for i in elt:
                donnee.append(tableau_v[i]['adresse'])
                #print(tableau_v[i]['adresse'])        
            donnees_maps.append(donnee)   

        #print(donnees_maps)
                

    return render(request, 'gestionnaire/itineraire.html', {'donnees_maps' : donnees_maps, 'init_point' : tableau_v[0]['adresse']})

