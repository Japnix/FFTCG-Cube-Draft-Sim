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
        pack = []
        if len(self.cards) >= CARDS_PER_PACK:
            for x in range(0, CARDS_PER_PACK):
                pack.append(self.cards[0])
                self.cards.pop(0)

        return pack

    def makeAllPacks(self):
        for x in range(0,TOTAL_PACKS):
            self.packs.append(self.makePack())

    def getAllPacks(self):
        return self.packs


class Player:
    def __init__(self, name):
        self.name = name
        self.packs = []

    def addPack(self, pack):
        self.packs.append(pack)


class Game:
    def __init__(self, cube, players):
        self.players = []

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


game = Game(cube=Cube(), players=PLAYERS)
game.prepareGame()

if DEBUG is True:
    ## Debug JSON Export:
    json_export = {}
    for player in game.players:
        json_export[player.name] = {'packs' : player.packs}

    with open('draft.json', 'w+') as outfile:
        json.dump(json_export, outfile)




