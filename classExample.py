import random
'''
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
'''
def getInt(prompt,max,min = 1):
    while 1:
        try:
            ret = int(input(prompt))
            if max >= ret >=min:
                return ret
            else:
                print("out of range")
        except:
            print("invalid character... whole numbers only.")
#a = getInt("pick a number the same or less then the number of points you have left")
class Guy:
    def __init__(self, player = False):
        if not player:
            names = ["Abe","Bob","Carl","Doug","Earl","Fred","Greg","Hal","Igor","Jayce","Kayel","Lambda","Mohawk","Ned","Owpen","Peter","Quin","Ryen","Seld","Tae","Ulysses","Victor","Wan","Xan","Yan","Zed"]
            self.name = random.choice(names) + " " + random.choice(names)+ "son"
            self.strength = random.randint(1,4)
            self.speed = random.randint(1,4)
            self.tough = random.randint(1,4)
        else:
            done = False
            pointsRemaining = 7

            while not done:
                self.name = input ("what is your name")
                self.tough = getInt("U have 10 points,"
                                        "use them to upgrade your attributes. How many will u spend on tough",6)
                pointsRemaining-=self.tough-1
                self.speed = getInt ("What will u spend on speed, "
                                    "if u have less then zero at then end u will have to restart.",pointsRemaining+1)
                pointsRemaining-=self.speed-1
                self.strength = getInt("What will u use on strength",pointsRemaining+1)
                pointsRemaining-=self.strength-1
                print(pointsRemaining)
                if pointsRemaining == 0:
                    print("good job")
                    done = True
                else:
                    print("cheater")
        self.maxhp = self.tough

    def introduce(self):
        print(self.name + "'s strength = " + str(self.strength))
        print(self.name + "'s tough = " + str(self.maxhp))
        print(self.name + "'s speed = " + str(self.speed))
    def attack(self,victim):
        x = victim.strength
        a = self.strength
        attackRoll = random.randint(1,100)+ victim.speed*2
        print(self.name + " tough = " + str(self.tough))
        if attackRoll <= 10:
            print(self.name + " destroyed " + victim.name+".")
            victim.tough -= 2*self.strength
        elif attackRoll <= 25:
            print(self.name + " hit " + victim.name + ".")
            victim.tough -=self.strength
        elif attackRoll<=50:
            print(self.name + " nicked " + victim.name + ".")
            victim.tough -= (1/2)
        else:
            print(self.name + " fails at hitting " + victim.name + ".")

def runSimulatedCombat():
    guys = []
    for i in range(1):
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


def killCharacter():
    player = Guy(True)
    kills = 0
    while player.tough > 0:
        enemy = Guy()
        while enemy.tough > 0 and player.tough > 0:
            player.attack(enemy)
            enemy.attack(player)
        if enemy.tough <=0:
            kills +=1
            if player.tough < player.maxhp:
                player.tough += 0.0*(player.maxhp-player.tough)
    print("you have died but you killed " + str(kills) + " enemies.")

killCharacter()