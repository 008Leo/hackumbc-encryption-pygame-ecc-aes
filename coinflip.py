# flip a coin
import random

if __name__ == "__main__":
    list =["h","t"]
    my_points = 0
    system_points = 0
    decision = True
    while decision:
        flip = ""
        system = ""
        bet = input(str("Heads or tails? "))
        if bet == "h":
            system = "t"
        elif bet == "t":
            system = "h"
        elif flip != ("h" or "t"):
            print("invalid input")
        flip = list[random.randint(0,1)]
        if flip == bet:
            my_points += 1
            print(f"its {bet}, you win the bet!")
        elif system == flip:
            system_points += 1
            print(f"its not {bet}, system wins the bet!")
        elif bet == "stop":
            decision = False


        print("points below are: -->")
        print(f"you: {my_points}, system: {system_points}")


    print("Game ends with: -->>")
    print(f"you: {my_points}, system: {system_points}")










