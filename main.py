import requests
import random
import json

class Cube:
    def __init__(self, cardsperpack, totalpacks):
        self.cubeurl = 'http://dev.tawa.wtf:8000/api/cube/?api_key=lolbbq'
        self.cards = requests.get(self.cubeurl).json()
        self.packs = []
        self.cardsperpack = cardsperpack
        self.totalpacks = totalpacks

    def getPack(self, index):
        return self.packs[index]

    def removePack(self, index):
        return self.packs.pop(index)

    def getCards(self):
        return self.cards

    def shuffleCube(self):
        random.shuffle(self.cards)

    def makePack(self):
        pack = Pack()
        if len(self.cards) >= self.cardsperpack:
            for x in range(0, self.cardsperpack):
                pack.addCard(self.cards[0])
                self.cards.pop(0)

        return pack

    def makeAllPacks(self):
        for x in range(0,self.totalpacks):
            self.packs.append(self.makePack())

    def getAllPacks(self):
        return self.packs

    def addCard(self, card):
        self.cards.appen(card)

    def removeCard(self, index):
        self.cards.pop(index)


class Pack:
    def __init__(self):
        self.cards = []

    def displayPack(self):
        count = 1
        if self.cards:
            for card in self.cards:
                print(f"{count}.) {card['Code']} - {card['Name_EN']}")
                count += 1
        else:
            print(f"There are no cards in this pack")

    def addCard(self, card):
        self.cards.append(card)

    def removeCard(self, index):
        self.cards.pop(index)

    def numCardsLeft(self):
        return len(self.cards)

    def getCard(self, index):
        return self.cards[index]


class Player:
    def __init__(self, name):
        self.name = name
        self.packs = []
        self.currentpack = Pack()
        self.queuedpack = Pack()
        self.selectedcards = []

    def addPack(self, pack):
        self.packs.append(pack)

    def addSelectedCard(self, card):
        self.selectedcards.append(card)

    def removePack(self, index):
        self.packs.pop(index)

    def getPack(self,index):
        return self.packs[index]

    def openPack(self):
        self.currentpack = self.getPack(0)
        self.removePack(0)

    def setQueuedToCurrent(self):
        self.currentpack = self.queuedpack

class Game:
    def __init__(self, numofplayers, debug=False):
        self.players = []
        self.numofplayers = numofplayers
        self.round = 1
        self.packsperplayer = 5
        self.cardsperpack = 12
        self.totalpacks = self.packsperplayer * self.numofplayers
        self.cube = Cube(cardsperpack=self.cardsperpack, totalpacks=self.totalpacks)
        self.debug = debug

    def addPlayer(self, player):
        self.players.append(player)

    def giveAllPacks(self):
        for player in self.players:
            for x in range(0, self.packsperplayer):
                player.addPack(self.cube.getPack(0))
                self.cube.removePack(0)

    def askNumPlayers(self):
        while True:
            try:
                numberofplayers = int(input('How many players will be drafting (1-8)? '))
                while numberofplayers not in range(1,9):
                    print('This is not a valid number of players')
                    numberofplayers = int(input('How many players will be drafting (1-8)? '))

                return numberofplayers
            except:
                print('You did not input an integer')

    def askPlayerNames(self):
        for i in range(0,self.numofplayers):
            name = input(f"What is Player {i+1}'s Name? ")
            self.addPlayer(Player(name))

    def prepareGame(self):
        self.numofplayers = self.askNumPlayers()
        self.askPlayerNames()
        self.cube.shuffleCube()
        self.cube.makeAllPacks()
        self.giveAllPacks()

    def selectionRound(self, player, pack):

        def askForChoice(pack):
            while True:
                try:
                    choice = int(input("Please input your choice: ")) - 1
                    while choice not in range(0, pack.numCardsLeft()):
                        print('This is not an integer in the range of cards available')
                        choice = int(input("Please input your choice: ")) - 1
                    return choice
                except:
                    print('This is not an integer in the range of cards available')

        print(f"{player.name}:")
        print('Please select a card from the following cards:')

        pack.displayPack()

        if self.debug is True:
            choice = 0
        else:
            choice = askForChoice(pack)

        player.addSelectedCard(pack.getCard(choice))
        pack.removeCard(choice)

    def allOpenPack(self):
        for player in self.players:
            player.openPack()

    def allPassLeft(self):
        for player in self.players:
            index = self.getPlayerIndex(player)
            player.queuedpack = game.players[(index + 1) % self.numofplayers].currentpack
            print(f"{player.name} gets {game.players[(index + 1) % self.numofplayers].name}'s pack ")

        for player in self.players:
            player.currentpack = player.queuedpack

    def allPassRight(self):
        for player in self.players:
            index = self.getPlayerIndex(player)
            player.queuedpack = game.players[(index - 1) % self.numofplayers].currentpack
            print(f"{player.name} gets {game.players[(index - 1) % self.numofplayers].name}'s pack ")

        for player in self.players:
            player.setQueuedToCurrent()

    def getPlayer(self, index):
        return self.players[index]

    def getPlayerIndex(self, player):
        return self.players.index(player)

    def startGame(self):
        for round in range(0, 5):
            if game.round % 2 != 0:
                print(f"Beginning of Round {game.round} - PASS LEFT")
            else:
                print(f"Beginning of Round {game.round} - PASS RIGHT")
            game.allOpenPack()
            for card in range(0, 12):
                for player in game.players:
                    game.selectionRound(player, player.currentpack)

                if game.round % 2 != 0 and game.round != 5:
                    game.allPassLeft()
                elif game.round % 2 == 0 and game.round != 5:
                    game.allPassRight()
                else:
                    pass
            game.round += 1

        print('Finished Game')

    def finalSelectedToJson(self, filename):
        exportdict = {}

        for player in self.players:
            exportdict[player.name] = {'selectedcards': player.selectedcards}

        with open(filename, 'w+') as outfile:
            json.dump(exportdict, outfile)


game = Game(numofplayers=8, debug=True)
game.prepareGame()
game.startGame()
game.finalSelectedToJson('draft.json')



