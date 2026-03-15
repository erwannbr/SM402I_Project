from automaton import *
from file_parser import read_automaton
from operation import *

def main():
    automaton = read_automaton()
    #automaton = determinize(automaton)
    #automaton = completion(automaton)
    #automaton = standardization(automaton)

    display_automata(automaton)

if __name__ == "__main__":
    main()

    