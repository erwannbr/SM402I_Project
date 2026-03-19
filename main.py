from file_parser import read_automaton
from automaton import display_automata, recognize_word
from operation import *

def menu():
    print("\n" + "="*30)
    print("      Automaton Menu")
    print("="*30)
    print("1. Display Automaton")
    print("2. Standardize")
    print("3. Determinize")
    print("4. Complete")
    print("5. Minimize")
    print("6. Test a word")
    print("7. Reload another automaton")
    print("0. Exit")
    print("="*30)
    return input("Choose an option: ")

def main():
    try:
        print("\n")
        current_fa = read_automaton()
    except Exception as e:
        print(f"error loading file: {e}")
        return

    while True:
        choice = menu()

        if choice == "1":
            display_automata(current_fa) 

        elif choice == "2":
            current_fa = standardization(current_fa)
            display_automata(current_fa)

        elif choice == "3":
            current_fa = determinize(current_fa)
            display_automata(current_fa)

        elif choice == "4":
            current_fa = completion(current_fa)
            display_automata(current_fa)

        elif choice == "5":
            current_fa = minimization(current_fa)
            display_automata(current_fa)

        elif choice == "6":
            word = input("Enter the word to test: ")
            if recognize_word(current_fa, word): 
                print(f"The word '{word}' is accepted.")
            else:
                print(f"The word '{word}' is rejected.")

        elif choice == "7":
            current_fa = read_automaton()


if __name__ == "__main__":
    main()
    