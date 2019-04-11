import random
import itertools

redball_list = [1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46]
greenball_list = [5,6,11,16,17,21,22,27,28,32,33,38,39,43,44,49]
blueball_list = [3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48]

latest_number = [8,21,34,37,41,45,49]

new_red = list(set(redball_list) - set(latest_number))
new_green = list(set(greenball_list) - set(latest_number))
new_blue = list(set(blueball_list) - set(latest_number))
new_red.sort()
new_green.sort()
new_blue.sort()

red_count = 3
blue_count = 3
green_count = 2

buy_list = [];

for x in range(red_count):
    rand_number = random.choice(new_red)
    buy_list.append(rand_number)
    new_red.remove(rand_number)

for x in range(green_count):
    rand_number = random.choice(new_green)
    buy_list.append(rand_number)
    new_green.remove(rand_number)

for x in range(blue_count):
    rand_number = random.choice(new_blue)
    buy_list.append(rand_number)
    new_blue.remove(rand_number)

buy_list.sort()
random.shuffle(buy_list)
cut = 4
banker = buy_list[:cut]
leg = buy_list[cut:]

print(banker)
print(leg)

leg_combination = list(itertools.combinations(leg, 2))

for x in leg_combination:
    new_banker = banker.copy()
    new_banker.append(x[0])
    new_banker.append(x[1])
    new_banker.sort()
    print(new_banker)