import random
from time import sleep as wait

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
alphabetLower = [x.lower() for x in alphabet]

defaultWeapons = {
    "Basic Sword" : { "Slash" : ["random", 30], "Slice" : ["min", 15], "Spear" : ["max", 60] }
}

# nline - Creates specified amount of new lines (default 1)

def nline(amnt = 1):
    for x in range(amnt):
        print('')

# decorate - Decorates a specified string
# Types:
# line - makes two lines centered above and below text

def decorate(string, type = 'line'):
    if type == 'line':
        whiteSpace = int((len(string)/2)-3)
        spacer = ''
        
        for x in range(whiteSpace):
            spacer = spacer + ' ' 

        print(spacer + '------' + spacer)
        print(str(string))
        print(spacer + '------' + spacer)


# checkForFile - checks for specified fileName, if fileName doesn't exist,
# creates the file.

def checkForFile(fileName):
    try:
        with open('SAVEFILE.txt', 'x') as file:
            file.write('Placeholder|1')
        
        print('No save data found.\nCreating new save file')
        wait(1)
    except:
        print('Save file found.')
        wait(1)


# ---------
# savedStat
# ---------
# Creates a dynamic saved value

# The value in savedStat can be accessed and changed using savedStat.Value
# but should only be changed with savedStat.change(value) or saveStat.set(value) if autoSave is set to True

# .load() sets the value to the value from the saveFile

# Keyword arguments:
# autoSave = True/False (if True, saves to file every time a change is made through .set() or .change()),
# defaults to False

# file = name of file to save in, defaults to SAVEFILE.txt

class savedStat:
    def __init__(self, saveName, initialValue = 0, autoSave = False, saveFile = "SAVEFILE.txt"):
        """Creates a dynamic saved value.

        Args:
            saveName (str): Key for save file.
            initialValue (int, optional): _description_. Defaults to 0.
            autoSave (bool, optional): Should value be autosaved? Defaults to False.
            saveFile (str, optional): Name of file to save to. Defaults to "SAVEFILE.txt".
        """
        self.saveName = saveName
        self.Value = initialValue
        
        self.autoSave = autoSave
        self.saveFile = saveFile
        
        try:
            with open(self.saveFile, 'x') as file:
                file.write('Placeholder#0')
        except: pass
        
    def change(self, val = 0):
        """Change value of stat.

        Args:
            val (int): Value to add.
        """
        self.Value += val
        if self.autoSave: self.save()
        
    def set(self, val):
        """Set value of stat

        Args:
            val (int): Value to set.
        """
        self.Value = val
        if self.autoSave: self.save()
        
    def save(self):
        """Save the current value.
        """
        with open(self.saveFile, "r") as file:
            raw = file.read()
            
        rawContents = raw.split('|')
        contents = {}
        for item in rawContents:
            contents[item.split('#')[0]] = item.split('#')[1]
            
        contents[self.saveName] = self.Value
        
        stringToSave = ''
        
        for name in contents.keys():
            stringToSave += str(name) + '#' + str(contents[name]) + '|'
        
        with open(self.saveFile, 'w') as file:
            file.write(stringToSave[:-1])
            
    def load(self, set = True):
        """Loads Value from save file.

        Arguments:
            set (bool, optional): Set self.Value to loaded value? Defaults to True.

        Returns:
            (str): loaded value
        """
        with open(self.saveFile, "r") as file:
            raw = file.read()
            
        rawContents = raw.split('|')
        contents = {}
        
        for item in rawContents:
            contents[item.split('#')[0]] = item.split('#')[1]
            
        if self.saveName in contents.keys():
            self.Value = int(contents[self.saveName])
        
        return int(contents[self.saveName])

class createAttack: # [name, dmg, description]
    def __init__(self, name, dmg = 10, description = False):
        self.Data = [name, dmg, description]
        print(self.Data)
    
class groupAttacks:
    def __init__(self, *args):
        self.Data = []
        
        for attack in args:
            self.Data.append(attack.Data)
    
    def makePlayerWeapon(self, name):
        newData = [name]
        newData.append(self.Data)
        self.Data = newData

class Menu:
    def __init__(self, title = "", body = "", statsToShow = None, **kwargs):
        self.Title = title.upper()
        self.Body = body
        self.Stats = statsToShow
        self.kwargs = kwargs
    
    def decorate(self, string, type = 'line'):
        if type == 'line':
            whiteSpace = int((len(string)/2)-3)
            spacer = ''
            
            for x in range(whiteSpace):
                spacer = spacer + ' ' 

            print(spacer + '------' + spacer)
            print(str(string))
            print(spacer + '------' + spacer)
    
    def showText(self):
        if self.Title != '':
            self.decorate(self.Title)
        nline()
        print(self.Body)
        nline()
        print('Options:')
        for arg in self.kwargs:
            print(' ', arg, '-', self.kwargs[arg])
            
        print('\n')
    
    def open(self):
        option = ''
        
        while option not in self.kwargs.keys():
            nline(100)
            self.showText()
            option = input('Type an option\n-->  ')
        
        return self.kwargs[option]
        
class Player:
    def __init__(self):
        self.health = 100
        
    def get_health(self):
        return self.health

    def set_health(self, val, add = False):
        if add:
            self.health += val
        else:
            self.health = val

class Battle:
    def __init__(self, name = "default", desc = "defaultdesc", weapon = "Sword", health = 100, lowDmg = 5, highDmg = 10, attackData = []):
        self.name = name
        self.desc = desc
        self.weapon = weapon
        self.startHealth = health
        self.lowDmg = lowDmg
        self.highDmg = highDmg
        self.health = self.startHealth

        self.Attacks = attackData

    def startBattle(self, plrWeaponData, playerHealth): # "plr" is short for player
        self.health = self.startHealth
        self.playerHealth = playerHealth
        nline(100)
        battleActive = True
        while battleActive:
            self.battleUI(plrWeaponData, self.playerHealth)
            entryActive = True
            while entryActive: # catch for invalid input
                actionChoice = input('\nYour turn! Type a weapon action or type "x" to quit...\n--> ')
                try: actionID = alphabetLower.index(actionChoice)
                except: print('Invalid input...\n')
                
            self.displayAttack(plrWeaponData, actionID)
            self.battleUI(plrWeaponData, self.playerHealth)
            input('\nTap enter to continue...\n')
            actionID = random.randint(0, (len(self.Attacks.Data) - 1))
            self.displayAttack(self.Attacks, actionID)
            
        return playerHealth
    
    def battleUI(self, weaponData, playerHealth):
        weaponData = weaponData.Data
        weaponName = weaponData[0]
        weaponAttacks = weaponData[1]
        
        # a lot of fun unreadable code is below
        # i honestly forgot how this works pls dont break
        nline(100)
        print('Opponent:\n- ' + str(self.name) + ' -\n---\n', str(self.desc) + '')
        print('---\nCurrently using [' + str(weaponName) + ']\nWeapon Actions:')
        for x, attack in enumerate(weaponAttacks):
            print(alphabet[x].lower(), '-', attack[0], '|', str(attack[1]), 'Dmg')
        nline()
        print('Your Health:', playerHealth,' | ', 'Opponent Health:', self.health)
    
    def displayAttack(self, attackData, actionID):
        attackData = attackData.Data
        print(attackData)
        
        if len(attackData) == 2:
            dmgDone = attackData[1][actionID][1]
            oppositeInst = 'You'
            instigator = self.name
            print(dmgDone)
            self.playerHealth -= dmgDone
        else:
            print(attackData[actionID][1])
            dmgDone = attackData[actionID][1]
            oppositeInst = self.name
            instigator = 'You'
            print(dmgDone)
            self.health -= dmgDone
        
        nline(100)
        if instigator == self.name:
            print('%s used "%s" (%s)\n'% (oppositeInst, attackData[1][actionID][0], attackData[0]))
            if attackData[1][actionID][2] != False:
                print(attackData[1][actionID][2])
        else:
            print('%s used "%s" (%s)\n'% (oppositeInst, attackData[actionID][0], self.weapon))
            if attackData[actionID][2] != False:
                print(attackData[actionID][2])
        
        print('\n%s lost %s health.' % (instigator, dmgDone))
        input('\nTap enter to continue...\n')
    
# Comment this out if you don't want this popping up at the start, though it will likely get quickly hidden by a newline function
print('using Adventure Toolkit v0.1')