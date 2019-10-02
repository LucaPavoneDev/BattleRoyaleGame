x = int(30);
y = int(12);

print(x / y);

fruits = ["Apple", "Banana", "Orange", "Melon", "Pear", "Strawberry", "Snoffleberry"];
print(fruits);

person = {"name":"Mr. Pibb","age":47,"occupation":"Soft Drink Mascot"}
print(str(person["age"])+", "+person["occupation"]);

addup = [6, 7, 2, 4, 9, 1, 5];
addup_total = 0;

for i in addup:
    addup_total = addup_total+i;

print("The addup total is... "+str(addup_total));

#Quick dice function.
def dice(sides, mod):
    from random import randint;
    total = randint(1,sides)+mod;
    return total;

print(dice(6,0));
