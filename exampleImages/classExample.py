import random
def greet(name):
    print("Hello " + name)


#1 3 5 ...
def rollNDS(n,s):
    ret = []
    for i in range(n):
        ret.append(random.randint(1,s))
    return ret
def sumOfList(list):
    sum = 0
    for item in list:
        sum += item
    return sum

result = rollNDS(1000,20)
print(result)
print(sumOfList(result))


class Guy:

    def __init__(self):
        names = ["Abe","Bob","Carl","Doug","Earl","Fred","Greg","Hal","Igor","Jayce","Kayel","Lambda","Mohawk","Ned","Owpen","Peter","Quin","Ryen","Seld","Tae","Ulysses","Victor","Wan","Xan","Yan","Zed"]
        self.name = random.choice(names) + " " + random.choice(names)+ "son"
        self.strength = random.randint(1,6)
        self.speed = random.randint(1,6)
        self.tough = random.randint(1,6)
        self.maxhp = self.tough
    def introduce(self):
        print(self.name + "'s strength = " + str(self.strength))
        print(self.name + "'s tough = " + str(self.maxhp))
        print(self.name + "'s speed = " + str(self.speed))
    def attack(self,victim):
        x = victim.strength
        a = self.strength
        attackRoll = random.randint(1,100)+ victim.speed*2

        if attackRoll <= 10:
            print(self.name + " destroyed " + victim.name+".")
            victim.tough -= 2*self.strength
        elif attackRoll <= 25:
            print(self.name + " hit " + victim.name + ".")
            victim.tough -=self.strength
        elif attackRoll<=50:
            print(self.name + " nicked " + victim.name + ".")
            self.tough -= (1/2)
        else:
            print(self.name + " fails at hitting " + victim.name + ".")


guys = []
for i in range(1000):
    guys.append(Guy())

while guys.__len__() > 1:
    for guy in guys:
        victim = guy
        while guy == victim:
            victim = random.choice(guys)
        guy.attack(victim)
        if victim.tough <0:
            guys.remove(victim)
for guy in guys:
    print("the victor is ")
    guy.introduce()