#!/usr/bin/env python3

import graph as gr

import calc as c

import numpy as np

import sys


# maksymalna liczba pakietow jaka moze zostac wyslana
MAX = 12
# szansa na polaczenie, w %
CONNECTED = 90

T_MAX = 0.01

def run(option, Max=12, MAX_T=0.01, p=90):
    global MAX, T_MAX
    MAX = Max
    MAX_T = T_MAX

    nodes = 20
    edges = 30
    graph = gr.create_graph()

    if len(graph.edges()) > edges or len(graph.nodes) != nodes:
        print("Invalid number of edges or nodes! ")
        return

    N = c.init(graph, MAX, CONNECTED, p, option)

    if N != None:
        g = gr.draw_graph(graph)
        c.simulation(N, graph, T_MAX, option, 100)




def main():
    args = sys.argv
    if len(args) < 2:
        print("Argument --option is required! Use --option [N] [C] [T] [none]")
    else:
        if args[1] != "--option":
            print("--option is required!")
        else:
            option = args[2]
            if len(args) > 3:
                print("Remember the order! --option [param] _  MAX _ T_MAX _ p")
                try:
                    MAX = int(args[3])
                    T_MAX = float(args[4])
                    p = int(args[5])
                except ValueError:
                    print("That's not correct value! MAX, p -  int, T_MAX - float")
                run(option, MAX, T_MAX, p)
            else:
                run(option)

if __name__ == "__main__":
    main()
