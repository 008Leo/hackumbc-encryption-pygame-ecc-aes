
host = "Host"
guest = "Guest"
def game(user1, user2):
    if user1 == user2:
        print(f"It's a tie, {guest} entered {user2}")
        return 0
    elif user1 == "r":
        if user2 == "s":
            print(f"{user1} win! {guest} entered {user2}")
            return 1
        elif user2 == "p":
            print(f"{user1} lose! {guest} entered {user2}")
            return -1
    elif user1 == "p":
        if user2 == "r":
            print(f"{user1} win! {guest} entered {user2}")
            return 1
        elif user2 == "s":
            print(f"{user1} lose! {guest} entered {user2}")
            return -1
    elif user1 == "s":
        if user2 == "p":
            print(f"{user1} win! {guest} entered {user2}")
            return 1
        elif user2 == "r":
            print(f"{user1} lose! {guest} entered {user2}")
            return -1
    else:
        print("Invalid entry!")
        return 0

if __name__ == "__main__":
    HostUser = 0
    guestUser = 0
    user_list = ["r", "p", "s"]

    my_choice = "Host Input"
    guest_choice = "Guest input"
    
        my_choice = input("ROCK(r) PAPER(p) SCISSORS(s), SHOOT! (or 'stop' to quit): ").lower()

        if my_choice == "stop":
            break
        elif my_choice in user_list:
            result = game(my_choice, guest_choice)
            if result == 1:
                HostUser += 1
            elif result == -1:
                guestUser += 1
        else:
            print("Invalid entry!")
    
        print(host +" score: {HostUser}," + guest + " score: {guestUser}.")
