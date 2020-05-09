import requests
import json
import random

CUBE_URL = 'http://dev.tawa.wtf:8000/api/cube/?api_key=lolbbq'
PLAYERS = 8
CARDS_PER_PACK = 12
PACKS_PER_PLAYER = 4
TOTAL_PACKS = PLAYERS * PACKS_PER_PLAYER

class Cube:
    def __init__(self, players):
        self.cards = requests.get(CUBE_URL).json()
        self.players = players

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


cube = Cube(players=8)

list_of_packs = []

for x in range(0, TOTAL_PACKS):
    list_of_packs.append(cube.makePack())
    print(list_of_packs[x])



