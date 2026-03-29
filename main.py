from file_parser import read_automaton
from automaton import display_automata, recognize_word, read_word, is_standard, is_deterministic, is_complete
from operation import standardization, determinize, completion, minimization, complement

# this is function for the menu to choose option from
def menu():
    print("\n" + "=" * 35)
    print("        Automaton Menu")
    print("=" * 35)
    print("1. Display automaton")
    print("2. Check properties (std / det / complete)")
    print("3. Standardize")
    print("4. Determinize & complete")
    print("5. Minimize")
    print("6. Complement")
    print("7. Test a word")
    print("8. Load another automaton")
    print("0. Exit")
    print("=" * 35)
    return input("Choose an option: ").strip()


#this is the function to check the properties
def check_properties(fa):
    print(f"  Standard    : {'yes' if is_standard(fa) else 'no'}")
    print(f"  Deterministic: {'yes' if is_deterministic(fa) else 'no'}")
    print(f"  Complete    : {'yes' if is_complete(fa) else 'no'}")


#this is the main function
def main():
    try:
        current_fa = read_automaton() #to read the automaton
    except Exception as e:
        print(f"Error loading file: {e}")   #handle errors when reading the automaton
        return

    #main loop
    while True:
        choice = menu()

        #frist choice, to exit
        if choice == "0":
            print("Goodbye.")
            break
        
        #second choice, to display the automaton
        elif choice == "1":
            display_automata(current_fa)

        #third choice, to check the properties, using the functions previoulys created
        elif choice == "2":
            check_properties(current_fa)

        #fourth choice, to standardize, check if its already done or not
        elif choice == "3":
            if is_standard(current_fa):
                print("Automaton is already standard — skipping.")
            else:
                current_fa = standardization(current_fa)
                display_automata(current_fa)

        #fifth choice, to determinize and complete, handle the errors when hte automaton is already deterministic ro complete
        elif choice == "4":
            if is_deterministic(current_fa):
                if is_complete(current_fa):
                    print("Automaton is already a complete DFA — nothing to do.")
                else:
                    print("Automaton is deterministic but not complete → completing.")
                    current_fa = completion(current_fa)
                    display_automata(current_fa)
            else:
                print("Automaton is non-deterministic → determinizing & completing.")
                current_fa = determinize(current_fa)
                display_automata(current_fa)

        #sixth choice, to minimize, handle the errors when hte automaton is already minimize
        elif choice == "5":
            if not is_deterministic(current_fa) or not is_complete(current_fa):
                print("Please obtain a complete deterministic FA first (option 4).")
            else:
                current_fa = minimization(current_fa)
                display_automata(current_fa)

        #seventh choice, to complement, handole the fact that the automaton must be deterministic and complete
        elif choice == "6":
            if not is_deterministic(current_fa) or not is_complete(current_fa):
                print("Please obtain a complete deterministic FA first (option 4).")
            else:
                comp_fa = complement(current_fa)
                display_automata(comp_fa)

        #eighth choice, to test a word, by entering a word and checking if it is accepted or rejected, exit when typed 'end'
        elif choice == "7":
            word = read_word()
            while word != "end":
                if recognize_word(current_fa, word):
                    print(f"  '{word}' is accepted.")
                else:
                    print(f"  '{word}' is rejected.")
                word = read_word()

        #ninth choice, to load another automaton, return to the main menu, and the start of the first loop
        elif choice == "8":
            try:
                current_fa = read_automaton()
            except Exception as e:
                print(f"Error loading file: {e}")

        else:
            print("Unknown option — please try again.")

#main
if __name__ == "__main__":
    main()
