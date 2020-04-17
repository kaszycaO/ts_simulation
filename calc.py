import graph as gr

from random import randint

from random import uniform

from random import seed

import networkx as nx

import graph as gr

# dictionary z maksymalna przepustowoscia
MAX_CAPACITY = {}

# szansa na nieuszkodzenie lacza
PERCENTAGE = 90


# c
def get_capacity(graph, val1, val2, start, stop):
    if len(MAX_CAPACITY) == 0:
        for el in graph.edges(data = True):
            mul = uniform(start, stop)
            el[2]['capacity'] = int(val1 * val2  * mul)
    else:
        for el in graph.edges(data = True):
            add = uniform(start, stop)
            el[2]['capacity'] = int(el[2]['capacity'] + add)
# a
def route(N, graph):
    a = {}
    copy = graph.copy()

    for i in range(len(N)):
        j = 0
        copy = graph.copy()
        while j < len(N):
            if N[i][j] > 0:
                try:
                    path = nx.shortest_path(copy, i, j)
                except:
                    return -1

                for k in range(len(path) - 1):
                    key = str(path[k]) + "," + str(path[k+1])
                    key_2 = str(path[k+1]) + "," + str(path[k])
                    if a.get(key) == None and a.get(key_2) == None:
                        a.update({key : N[i][j]})
                    else:
                        if(a.get(key) == None):
                            key = key_2
                        old = a.get(key)
                        new = old + N[i][j]

                        if new > MAX_CAPACITY.get(key):
                            copy.remove_edge(path[k], path[k+1])
                            j -= 1
                            break
                        else:
                            a.update({key : new})

                j += 1

            else:
                j+=1
    return a

def add_to_max(el1, el2, capacity):
    key = str(el1) + "," + str(el2)
    MAX_CAPACITY.update({key : capacity})

    key = str(el2) + "," + str(el1)
    MAX_CAPACITY.update({key : capacity})

def max_cap(graph):
    global MAX_CAPACITY
    max_cap = {}
    for el in graph.edges(data=True):
        key = str(el[1]) + "," + str(el[0])
        max_cap.update({key : el[2]['capacity']})

        key = str(el[0]) + "," + str(el[1])
        max_cap.update({key : el[2]['capacity']})

    MAX_CAPACITY = max_cap

def get_cap(i,j):
    key = str(i) + "," + str(j)
    if MAX_CAPACITY.get(key) == None:
        key = str(j) + "," + str(i)

    return MAX_CAPACITY.get(key)

def rand_N(nodes, param, connected):
    my_list = []
    for i in range(nodes):
        helper = []
        for j in range(nodes):
            connection = randint(0, 100)
            if i == j or connection > connected:
                helper.append(0)
            else:
                helper.append(randint(0, param))
        my_list.append(helper)

    return my_list

def modify_N(N, mod):
    for i in range(len(N)):
        for j in range(len(N)):
            if N[i][j] != 0:
                N[i][j] += mod

def init(graph, param, connected, percentage, option):
    """ Inicjalizowanie bazowych wartosci, test macierzy N """
    global PERCENTAGE
    PERCENTAGE = percentage

    nodes = len(graph.nodes())
    N = rand_N(nodes, param, connected)
    mul = sum([max(i) for i in N])
    if option != 'C':
        get_capacity(graph, mul, mul, 2, 3)
    else:
        get_capacity(graph, mul, 1, 2, 3)

    max_cap(graph)
    a = route(N, graph)
    if a == -1:
        return None

    return N

def delay(N, a):
    suma = 0
    helper = 0
    m = 128
    for i in range(len(N)):
        for j in range(len(N)):
            suma += N[i][j]


    for k in a:
        l = k.split(',')
        cap = get_cap(int(l[0]), int(l[1]))
        fload = a[k]
        cap = cap / m
        helper += fload / (cap - fload)
    return (1/suma) * helper

def avg_capacity():
    suma = 0
    for el in MAX_CAPACITY:
        suma += MAX_CAPACITY[el]
    return int(suma/len(MAX_CAPACITY))

def check_if_exists(graph, p):
    seed()
    counter = 0
    for edge in graph.edges():
        percent = randint(0, 100)
        if percent > p:
            graph.remove_edge(edge[0], edge[1])

def simulation(N_tab, graph, T_max, change, experiments):

    if change == 'N':
        mod = 0.01
        for i in range(experiments):
            fail = 0
            passed = 0
            modify_N(N_tab, mod)
            for j in range(10):
                graph_copy = graph.copy()
                check_if_exists(graph_copy, PERCENTAGE)
                a = route(N_tab, graph_copy)
                if a != -1:
                    T = delay(N_tab, a)
                    if T < 0 :
                        fail += 1

                    elif T < T_max:
                        passed += 1
                    else:
                        fail += 1
                else:
                    fail += 1

            print("Niezawodnosc sieci: {}% ".format((passed/10) * 100))
            mod += 0.01

    elif change == 'C':
        start = 0
        stop = 1
        for i in range(experiments):
            fail = 0
            passed = 0
            graph_copy = graph.copy()
            get_capacity(graph_copy, 0, 0, start, stop)
            max_cap(graph_copy)
            for j in range(10):
                inside = graph_copy.copy()
                check_if_exists(inside, PERCENTAGE)
                a = route(N_tab, inside)
                if a != -1:
                    T = delay(N_tab, a)
                    if T < 0 :
                        fail += 1
                    elif T < T_max:
                        passed += 1
                    else:
                        fail += 1
                else:
                    fail += 1

            print("Niezawodnosc sieci: {}% ".format((passed/10) * 100))
            start += 2000
            stop += 2000

    elif change == 'T':
        for i in range(experiments):
            fail = 0
            passed = 0
            while True:
                x = randint(0, 19)
                y = randint(0, 19)
                if (x,y) not in MAX_CAPACITY and x != y:
                    cap = avg_capacity()
                    graph.add_edge(x,y, capacity=cap)
                    add_to_max(x,y,cap)
                    break

            for j in range(10):
                graph_copy = graph.copy()
                check_if_exists(graph_copy, PERCENTAGE)
                a = route(N_tab, graph_copy)
                if a != -1:
                    T = delay(N_tab, a)
                    if T < 0 :
                        fail += 1
                    elif T < T_max:
                        passed += 1
                    else:
                        fail += 1
                else:
                    fail += 1

            print("Niezawodnosc sieci: {}% ".format((passed/10) * 100))

    else:
        fail = 0
        passed = 0
        for i in range(experiments):
            graph_copy = graph.copy()
            check_if_exists(graph_copy, PERCENTAGE)
            a = route(N_tab, graph_copy)
            if a != -1:
                T = delay(N_tab, a)
                if T < 0 :
                    fail += 1
                elif T < T_max:
                    passed += 1
                else:
                    fail += 1
            else:
                fail += 1
        print("Niezawodnosc sieci: {}% ".format((passed/experiments) * 100))
