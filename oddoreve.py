# odd or even
import random


def odd_even(player,game):
    if (int(player)+int(game)) % 2 == 0:
        return "even"
    elif (int(player)+int(game)) % 2 == 1:
        return "odd"
def sum(a,b):
    return int(a) + int(b)

if __name__ == "__main__":
    decision = ""
    num_list = [1,2,3,4,5,6]
    user_num = 0
    system = 0
    user_point = 0
    system_point = 0
    while decision != "stop":
        decision = input(str("odd or even? "))
        if decision == "odd":
            user_num = 1
            system = random.randint(0,len(num_list)-1)
            x = odd_even(user_num,system)
            if x == decision:
                user_point += 1
            if x != decision:
                system_point += 1
            print("the sum is: ", sum(user_num,system))


        elif decision == "even":
            user_num = 2
            system = random.randint(0, len(num_list) - 1)
            x = odd_even(user_num, system)
            if x == decision:
                user_point += 1
            if x != decision:
                system_point += 1
            print("the sum is: ", sum(user_num, system))
        print(f"your score : {user_point} , game: {system_point}")

    print(f"your score : {user_point} , game: {system_point}")


