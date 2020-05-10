import requests
import json
import random

CUBE_URL = 'http://dev.tawa.wtf:8000/api/cube/?api_key=lolbbq'
PLAYERS = ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5', 'Player 6', 'Player 7', 'Player 8']
CARDS_PER_PACK = 12
PACKS_PER_PLAYER = 5
TOTAL_PACKS = len(PLAYERS) * PACKS_PER_PLAYER
DEBUG = True


class Cube:
    def __init__(self):
        self.cards = requests.get(CUBE_URL).json()
        self.packs = []

    def getCards(self):
        return self.cards

    def shuffleCube(self):
        random.shuffle(self.cards)

    def makePack(self):
        pack = Pack()
        if len(self.cards) >= CARDS_PER_PACK:
            for x in range(0, CARDS_PER_PACK):
                pack.addCard(self.cards[0])
                self.cards.pop(0)

        return pack

    def makeAllPacks(self):
        for x in range(0,TOTAL_PACKS):
            self.packs.append(self.makePack())

    def getAllPacks(self):
        return self.packs


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


class Player:
    def __init__(self, name):
        self.name = name
        self.packs = []
        self.currentpack = []
        self.selectedcards = []

    def addPack(self, pack):
        self.packs.append(pack)

    def packstoDict(self):
        packs = []
        for pack in self.packs:
            packs.append(pack.cards)

        return packs

    def addSelectedCard(self, card):
        self.selectedcards.append(card)


class Game:
    def __init__(self, cube, players):
        self.players = []
        self.round = 1
        self.card = 1

        for name in players:
            player = Player(name)
            self.addPlayer(player)

        self.cube = cube

    def addPlayer(self, player):
        self.players.append(player)

    def giveAllPacks(self):
        for player in self.players:
            for x in range(0, PACKS_PER_PLAYER):
                player.addPack(self.cube.packs[0])
                self.cube.packs.pop(0)

    def prepareGame(self):
        self.cube.shuffleCube()
        self.cube.makeAllPacks()
        self.giveAllPacks()
        
    def selectionRound(self, player):

        print(f"{player.name}: Round {self.round} Card {self.card}")
        print('Please select a card from the following cards:')

        index = self.round - 1

        player.packs[index].displayPack()

        choice = input("Please input your choice: ")
        choice = int(choice) - 1
        player.addSelectedCard(player.packs[index].cards[choice])
        player.packs[index].removeCard(choice)
        player.packs[index].displayPack()

        if len(player.packs[index].cards) == 0:
            self.round += 1
        else:
            self.card += 1
        

game = Game(cube=Cube(), players=PLAYERS)
game.prepareGame()

while game.round < PACKS_PER_PLAYER + 1:
    game.selectionRound(game.players[0])

print(game.players[0].selectedcards)




if DEBUG is True:
    ## Debug JSON Export:
    json_export = {}
    for player in game.players:
        json_export[player.name] = {'packs' : player.packstoDict()}

    with open('draft.json', 'w+') as outfile:
        json.dump(json_export, outfile)




